"""Pruebas de integración con una base SQLite temporal; producción usa MySQL."""
import base64
import io
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from werkzeug.datastructures import FileStorage

from app import app
from database import db
from utils.validations import MAX_ARCHIVO, ahora_chile, validate_archivos

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")
# Encabezado MP4 usado para comprobar detección y almacenamiento, no reproducción.
MP4 = bytes.fromhex("000000186674797069736F6D0000020069736F6D69736F32")


class AppTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")

        @event.listens_for(self.engine, "connect")
        def foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

        db.Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.patch = patch.object(db, "SessionLocal", self.sessions)
        self.patch.start()
        self.folder = tempfile.TemporaryDirectory()
        self.config = patch.dict(app.config, {
            "TESTING": True, "SECRET_KEY": "solo-pruebas", "UPLOAD_FOLDER": self.folder.name,
        })
        self.config.start()
        self.client = app.test_client()
        with self.sessions.begin() as session:
            session.add_all([db.Region(id=1, nombre="Metropolitana"), db.Region(id=2, nombre="Valparaíso")])
            session.flush()
            session.add_all([db.Comuna(id=1, nombre="Santiago", region_id=1),
                             db.Comuna(id=2, nombre="Concón", region_id=2), db.Ave(id=1, nombre="Cóndor")])
        self.client.get("/registro-voluntario")
        with self.client.session_transaction() as session:
            self.token = session["csrf_token"]

    def tearDown(self):
        self.config.stop()
        self.patch.stop()
        self.engine.dispose()
        self.folder.cleanup()

    def voluntario(self, **cambios):
        datos = {"csrf_token": self.token, "nombre": "Diego", "apellido": "Ruiz",
                 "email": "diego@example.cl", "celular": "+56 9 1234 5678", "region": "1",
                 "comuna": "1", "direccion": "Beauchef 850"}
        datos.update(cambios)
        return self.client.post("/registro-voluntario", data=datos)

    def avistamiento(self, **cambios):
        datos = {"csrf_token": self.token, "voluntario": "1", "nombre-ave": "1", "tipo-ave": "rapaz",
                 "region": "2", "comuna": "2", "lugar": "Humedal de Concón",
                 "fecha": ahora_chile().strftime("%Y-%m-%d"), "hora": "10:30",
                 "descripcion": "Dos aves", "archivo": [(io.BytesIO(PNG), "ave.png")]}
        datos.update(cambios)
        return self.client.post("/registrar-avistamiento", data=datos, content_type="multipart/form-data")

    def test_paginas_vacias_y_enlaces_anteriores(self):
        for url in ("/", "/index.html", "/registro-voluntario.html", "/registrar-avistamiento.html",
                    "/avistamientos.html", "/estadisticas.html", "/static/css/estilos.css"):
            with self.subTest(url=url):
                with self.client.get(url) as respuesta:
                    self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Aún no hay", self.client.get("/").get_data(as_text=True))

    def test_registro_voluntario_y_seleccion_previa(self):
        respuesta = self.voluntario()
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("Registrar un avistamiento", self.client.get(respuesta.location).get_data(as_text=True))
        with self.sessions() as session:
            v = session.query(db.Voluntario).one()
            self.assertEqual(v.nombre, "Diego Ruiz")
            self.assertEqual(v.telefono, "+56912345678")
            self.assertEqual(v.direccion, "Beauchef 850")
            self.assertLess(abs((ahora_chile() - v.fecha_registro).total_seconds()), 10)
        html = self.client.get("/registrar-avistamiento?voluntario=1").get_data(as_text=True)
        self.assertIn('value="1" selected>Diego Ruiz', html)

    def test_voluntario_invalido_conserva_datos_sin_insertar(self):
        respuesta = self.voluntario(email="invalido", comuna="2")
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('value="Diego"', respuesta.get_data(as_text=True))
        self.assertIn("comuna perteneciente", respuesta.get_data(as_text=True))
        with self.sessions() as session:
            self.assertEqual(session.query(db.Voluntario).count(), 0)

    def test_registro_multimedia_y_detalle(self):
        self.voluntario()
        respuesta = self.avistamiento(archivo=[(io.BytesIO(PNG), "../../ave.png"), (io.BytesIO(MP4), "video.mp4")])
        self.assertEqual(respuesta.status_code, 302)
        with self.sessions() as session:
            self.assertEqual(session.query(db.Avistamiento).count(), 1)
            registros = session.query(db.Registro).all()
            self.assertEqual(len(registros), 2)
            for registro in registros:
                self.assertNotIn("..", registro.ruta_archivo)
                self.assertTrue((Path(self.folder.name) / Path(registro.ruta_archivo).name).is_file())
        self.assertIn("registrado correctamente", self.client.get(respuesta.location).get_data(as_text=True))
        detalle = self.client.get("/avistamiento/1").get_data(as_text=True)
        for texto in ("<img ", "<video ", "Dos aves", "Concón", "Diego Ruiz"):
            self.assertIn(texto, detalle)

    def test_validaciones_avistamiento_sin_javascript(self):
        self.voluntario()
        for cambios in ({"voluntario": "999"}, {"nombre-ave": "1 OR 1=1"}, {"comuna": "1"},
                        {"tipo-ave": "inventado"}, {"fecha": "2026-02-30"}, {"hora": "25:99"},
                        {"fecha": (ahora_chile() + timedelta(days=1)).strftime("%Y-%m-%d")},
                        {"fecha": (ahora_chile() - timedelta(days=31)).strftime("%Y-%m-%d")},
                        {"descripcion": "x" * 501}, {"lugar": "x" * 201}, {"archivo": []}):
            with self.subTest(cambios=cambios):
                respuesta = self.avistamiento(**cambios)
                self.assertEqual(respuesta.status_code, 400)
                self.assertIn('value="Humedal de Concón"' if "lugar" not in cambios else "200 caracteres",
                              respuesta.get_data(as_text=True))
        with self.sessions() as session:
            self.assertEqual(session.query(db.Avistamiento).count(), 0)
        self.assertEqual(list(Path(self.folder.name).iterdir()), [])

    def test_limite_fecha_30_dias_inclusive(self):
        self.voluntario()
        self.assertEqual(self.avistamiento(fecha=(ahora_chile() - timedelta(days=30)).strftime("%Y-%m-%d")).status_code, 302)

    def test_archivos_falsos_vacios_y_cantidad(self):
        self.voluntario()
        for archivos in ([(io.BytesIO(b"<script>alert(1)</script>"), "falsa.png")],
                         [(io.BytesIO(PNG), "foto.exe")], [(io.BytesIO(b""), "vacia.png")],
                         [(io.BytesIO(PNG), f"foto{i}.png") for i in range(11)]):
            self.assertEqual(self.avistamiento(archivo=archivos).status_code, 400)
        self.assertEqual(list(Path(self.folder.name).iterdir()), [])

    def test_limite_tamano_archivos(self):
        archivo = FileStorage(stream=io.BytesIO(PNG + b"0" * MAX_ARCHIVO), filename="grande.png")
        errores, _ = validate_archivos([archivo])
        self.assertTrue(any("20 MB" in error for error in errores))

    def test_paginacion_filtros_y_ultimos_dos_agregados(self):
        self.voluntario()
        for i in range(7):
            respuesta = self.avistamiento(lugar=f"Lugar {i}", **{
                "tipo-ave": "rapaz" if i < 6 else "marina",
                "fecha": (ahora_chile() - timedelta(days=i)).strftime("%Y-%m-%d"),
            })
            self.assertEqual(respuesta.status_code, 302)
        portada = self.client.get("/").get_data(as_text=True)
        self.assertIn("Lugar 6", portada)
        self.assertIn("Lugar 5", portada)
        self.assertNotIn("Lugar 4", portada)
        pagina1 = self.client.get("/avistamientos").get_data(as_text=True)
        self.assertEqual(pagina1.count('class="fila-avistamiento"'), 5)
        pagina2 = self.client.get("/avistamientos?pagina=2").get_data(as_text=True)
        self.assertEqual(pagina2.count('class="fila-avistamiento"'), 2)
        filtrado = self.client.get("/avistamientos?tipo=marina&orden=lugar-asc").get_data(as_text=True)
        self.assertEqual(filtrado.count('class="fila-avistamiento"'), 1)
        self.assertIn("Lugar 6", filtrado)
        for pagina in ("-10", "999999999999999999999", "abc"):
            self.assertEqual(self.client.get("/avistamientos?pagina=" + pagina).status_code, 200)
        self.assertEqual(self.client.get("/avistamientos?tipo=' OR 1=1&orden=DROP TABLE ave").status_code, 200)

    def test_texto_malicioso_se_escapa(self):
        self.voluntario()
        self.assertEqual(self.avistamiento(descripcion="<script>alert('x')</script>").status_code, 302)
        html = self.client.get("/avistamiento/1").get_data(as_text=True)
        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;", html)

    def test_fallo_db_limpia_archivos_y_preserva_formulario(self):
        self.voluntario()
        with patch.object(db, "create_avistamiento", side_effect=SQLAlchemyError("fallo simulado")):
            with self.assertLogs(app.logger, level="ERROR"):
                respuesta = self.avistamiento()
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('value="Humedal de Concón"', respuesta.get_data(as_text=True))
        self.assertEqual(list(Path(self.folder.name).iterdir()), [])

    def test_transaccion_revierte_avistamiento_si_falla_registro(self):
        self.voluntario()
        with self.assertRaises(SQLAlchemyError):
            db.create_avistamiento({"voluntario_id": 1, "ave_id": 1, "fecha_hora": ahora_chile(),
                                    "lugar": "Parque", "tipo_ave": "rapaz", "comuna_id": 1},
                                   [{"ruta_archivo": "uploads/a.png", "nombre_archivo": None}])
        with self.sessions() as session:
            self.assertEqual(session.query(db.Avistamiento).count(), 0)
            self.assertEqual(session.query(db.Registro).count(), 0)

    def test_csrf_y_registro_inexistente(self):
        self.assertEqual(self.client.post("/registro-voluntario", data={}).status_code, 400)
        self.assertEqual(self.client.post("/registro-voluntario", data={"csrf_token": "inválido"}).status_code, 400)
        self.assertEqual(self.client.get("/avistamiento/999").status_code, 404)
        self.assertEqual(self.client.get("/voluntario/999/registrado").status_code, 404)


if __name__ == "__main__":
    unittest.main()
