
import hashlib
import os
import secrets
import uuid
from pathlib import Path

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from database import db
from utils.validations import TIPOS_AVES, ahora_chile, validate_avistamiento, validate_comentario, validate_voluntario

app = Flask(__name__, template_folder="template")
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["UPLOAD_FOLDER"] = str(Path(app.root_path) / "static" / "uploads")
app.config["MAX_CONTENT_LENGTH"] = 201 * 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@app.context_processor
def datos_comunes():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return {"csrf_token": session["csrf_token"], "tipos_aves": TIPOS_AVES}


@app.before_request
def validar_csrf():
    if request.method == "POST":
        esperado = session.get("csrf_token", "")
        recibido = request.form.get("csrf_token", "")
        if not esperado or not secrets.compare_digest(esperado.encode("utf-8"), recibido.encode("utf-8")):
            abort(400, description="El formulario expiró. Vuelva a abrirlo e intente nuevamente.")


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html", avistamientos=db.get_ultimos_avistamientos())


@app.route("/registro-voluntario", methods=["GET", "POST"])
@app.route("/registro-voluntario.html", methods=["GET", "POST"])
def registrar_voluntario():
    catalogos = db.get_catalogos()
    errores = []
    if request.method == "POST":
        errores, datos = validate_voluntario(request.form, catalogos)
        if not errores:
            try:
                id = db.create_voluntario(datos)
                flash("Voluntario registrado correctamente.", "exito")
                return redirect(url_for("voluntario_registrado", id=id))
            except SQLAlchemyError:
                app.logger.exception("No se pudo registrar el voluntario")
                errores.append("No se pudo guardar el voluntario. Intente nuevamente.")
    return render_template("registro-voluntario.html", datos=request.form,
                           errores=errores, **catalogos), (400 if errores else 200)


@app.route("/voluntario/<int:id>/registrado")
def voluntario_registrado(id):
    voluntario = db.get_voluntario(id)
    if voluntario is None:
        abort(404)
    return render_template("voluntario-registrado.html", voluntario=voluntario)


@app.route("/registrar-avistamiento", methods=["GET", "POST"])
@app.route("/registrar-avistamiento.html", methods=["GET", "POST"])
def registrar_avistamiento():
    catalogos = db.get_catalogos()
    errores = []
    datos_formulario = request.form if request.method == "POST" else {
        "voluntario": request.args.get("voluntario", "")
    }
    if request.method == "POST":
        archivos = [archivo for archivo in request.files.getlist("archivo") if archivo.filename]
        errores, datos, formatos = validate_avistamiento(request.form, archivos, catalogos)
        if not errores:
            guardados, registros = [], []
            try:
                Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
                for archivo, formato in zip(archivos, formatos):
                    # Mismo mecanismo del ejemplo: nombre seguro + hash + UUID.
                    nombre_hash = hashlib.sha256(secure_filename(archivo.filename).encode("utf-8")).hexdigest()
                    nombre = f"{nombre_hash}_{uuid.uuid4()}.{formato.extension}"
                    destino = Path(app.config["UPLOAD_FOLDER"]) / nombre
                    guardados.append(destino)
                    archivo.save(destino)
                    registros.append({"ruta_archivo": f"uploads/{nombre}", "nombre_archivo": archivo.filename})
                db.create_avistamiento(datos, registros)
            except (OSError, SQLAlchemyError):
                # Si falla la escritura o la transacción, no dejar archivos huérfanos.
                for destino in guardados:
                    try:
                        destino.unlink(missing_ok=True)
                    except OSError:
                        app.logger.exception("No se pudo retirar un archivo incompleto")
                app.logger.exception("No se pudo registrar el avistamiento")
                errores.append("No se pudo guardar el avistamiento. Intente nuevamente y vuelva a seleccionar los archivos.")
            else:
                flash("El avistamiento fue registrado correctamente.", "exito")
                return redirect(url_for("index"))
    return render_template("registrar-avistamiento.html", datos=datos_formulario,
                           errores=errores, **catalogos), (400 if errores else 200)


@app.route("/avistamientos")
@app.route("/avistamientos.html")
def avistamientos():
    pagina = request.args.get("pagina", 1, type=int)
    tipo = request.args.get("tipo", "todos")
    orden = request.args.get("orden", "fecha-desc")
    if tipo not in {"todos", *TIPOS_AVES}:
        tipo = "todos"
    if orden not in {"fecha-desc", "fecha-asc", "lugar-asc", "lugar-desc"}:
        orden = "fecha-desc"
    datos, total, pagina, paginas = db.get_avistamientos(pagina, tipo, orden)
    return render_template("avistamientos.html", avistamientos=datos, total=total,
                           pagina=pagina, paginas=paginas, tipo=tipo, orden=orden)


@app.route("/avistamiento/<int:id>")
def detalle_avistamiento(id):
    avistamiento = db.get_avistamiento(id)
    if avistamiento is None:
        abort(404)
    return render_template("detalle-avistamiento.html", avistamiento=avistamiento)


@app.route("/estadisticas")
@app.route("/estadisticas.html")
def estadisticas():
    return render_template("estadisticas.html")


@app.get("/api/estadisticas")
def datos_estadisticas():
    dias, tipos, comunas = db.get_estadisticas()
    return jsonify(
        dias=[{"fecha": str(dia), "total": total} for dia, total in dias],
        tipos=[{"tipo": TIPOS_AVES.get(tipo, tipo), "total": total} for tipo, total in tipos],
        comunas=[{"comuna": comuna, "total": total} for comuna, total in comunas],
    )


@app.route("/api/avistamientos/<int:id>/comentarios", methods=["GET", "POST"])
def comentarios(id):
    if request.method == "POST":
        errores, nombre, texto = validate_comentario(request.form)
        if errores:
            return jsonify(errores=errores), 400
        comentario_id = db.create_comentario(id, nombre, texto, ahora_chile())
        if comentario_id is None:
            abort(404)
        return jsonify(id=comentario_id), 201

    lista = db.get_comentarios(id)
    if lista is None:
        abort(404)
    return jsonify([{"fecha": c.fecha.strftime("%d-%m-%Y %H:%M"), "nombre": c.nombre, "texto": c.texto}
                    for c in lista])


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(413)
def error_http(error):
    mensajes = {
        400: error.description,
        404: "No se encontró la página o el registro solicitado.",
        413: "La carga supera el límite total. Use hasta 10 archivos de máximo 20 MB cada uno.",
    }
    if request.path.startswith("/api/"):
        return jsonify(errores=[mensajes[error.code]]), error.code
    return render_template("error.html", codigo=error.code, mensaje=mensajes[error.code]), error.code


@app.errorhandler(SQLAlchemyError)
def error_database(error):
    app.logger.error("Error de conexión o consulta a la base de datos", exc_info=error)
    mensaje = "La base de datos no está disponible. Intente nuevamente más tarde."
    if request.path.startswith("/api/"):
        return jsonify(errores=[mensaje]), 503
    return render_template("error.html", codigo=503, mensaje=mensaje), 503


@app.cli.command("init-db")
def init_db():
    """Crear tablas e importar los catálogos."""
    from database.init_db import inicializar
    inicializar()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
