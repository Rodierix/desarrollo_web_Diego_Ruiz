
from pathlib import Path

from sqlalchemy import inspect

from database.db import Base, engine


def inicializar():
    Base.metadata.create_all(engine)
    # create_all no modifica tablas existentes: adaptar el esquema original.
    campos = {
        "voluntario": {"direccion": "VARCHAR(200) NULL"},
        "avistamiento": {
            "tipo_ave": "VARCHAR(20) NOT NULL DEFAULT 'otro'",
            "comuna_id": "INT NULL REFERENCES comuna(id)",
        },
    }
    with engine.begin() as conexion:
        for tabla, columnas in campos.items():
            existentes = {columna["name"] for columna in inspect(conexion).get_columns(tabla)}
            for nombre, definicion in columnas.items():
                if nombre not in existentes:
                    # Identificadores constantes del programa, nunca datos del formulario.
                    if tabla == "avistamiento" and nombre == "comuna_id":
                        conexion.exec_driver_sql("ALTER TABLE avistamiento ADD COLUMN comuna_id INT NULL")
                        conexion.exec_driver_sql("ALTER TABLE avistamiento ADD CONSTRAINT fk_avistamiento_comuna FOREIGN KEY (comuna_id) REFERENCES comuna(id)")
                    else:
                        conexion.exec_driver_sql(f"ALTER TABLE {tabla} ADD COLUMN {nombre} {definicion}")
        raiz = Path(__file__).resolve().parent.parent
        # Cada catálogo se importa sólo si está vacío. Se usan los SQL entregados.
        vacias = {tabla for tabla in ("region", "comuna", "ave")
                  if conexion.exec_driver_sql(f"SELECT COUNT(*) FROM {tabla}").scalar() == 0}
        for archivo in ("region-comuna.sql", "aves.sql"):
            for linea in (raiz / archivo).read_text(encoding="utf-8-sig").splitlines():
                if any(linea.startswith(f"INSERT INTO {tabla} ") for tabla in vacias):
                    conexion.exec_driver_sql(linea)
    print("Tablas listas y catálogos cargados. No se borraron registros existentes.")


if __name__ == "__main__":
    inicializar()
