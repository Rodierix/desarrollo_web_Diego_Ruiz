
import csv
import os
from pathlib import Path

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, TIMESTAMP, create_engine, func
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, joinedload, relationship, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL") or URL.create(
    "mysql+pymysql", username="cc5002", password="programacionweb",
    host="localhost", port=3306, database="tarea2", query={"charset": "utf8mb4"},
)
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

with Path(__file__).with_name("tipos-por-especie.csv").open(encoding="utf-8", newline="") as archivo:
    TIPOS_POR_ESPECIE = {fila["nombre"].casefold(): fila["tipo"] for fila in csv.DictReader(archivo)}


class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)


class Comuna(Base):
    __tablename__ = "comuna"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    region = relationship("Region")


class Voluntario(Base):
    __tablename__ = "voluntario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(80), nullable=False)
    telefono = Column(String(15), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    direccion = Column(String(200), nullable=True)
    comuna = relationship("Comuna")


class Ave(Base):
    __tablename__ = "ave"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)

    @property
    def tipo(self):
        return TIPOS_POR_ESPECIE.get(self.nombre.strip().casefold(), "otro")


class Avistamiento(Base):
    __tablename__ = "avistamiento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    voluntario_id = Column(Integer, ForeignKey("voluntario.id"), nullable=False)
    ave_id = Column(Integer, ForeignKey("ave.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    lugar = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    # Datos que ya se pedían en el formulario de la tarea 1.
    tipo_ave = Column(String(20), nullable=False, default="otro", server_default="otro")
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=True)
    voluntario = relationship("Voluntario")
    ave = relationship("Ave")
    comuna = relationship("Comuna")
    registros = relationship("Registro", back_populates="avistamiento", order_by="Registro.id")


class Registro(Base):
    __tablename__ = "registro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    avistamiento_id = Column(Integer, ForeignKey("avistamiento.id"), nullable=False)
    avistamiento = relationship("Avistamiento", back_populates="registros")


class Comentario(Base):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    avistamiento_id = Column(Integer, ForeignKey("avistamiento.id"), nullable=False, index=True)


def get_catalogos():
    with SessionLocal() as session:
        return {
            "regiones": session.query(Region).order_by(Region.id).all(),
            "comunas": session.query(Comuna).order_by(Comuna.nombre).all(),
            "aves": session.query(Ave).order_by(Ave.nombre).all(),
            "voluntarios": session.query(Voluntario).order_by(Voluntario.nombre).all(),
        }


def create_voluntario(datos):
    with SessionLocal.begin() as session:
        voluntario = Voluntario(**datos)
        session.add(voluntario)
        session.flush()
        return voluntario.id


def get_voluntario(id):
    with SessionLocal() as session:
        return session.get(Voluntario, id)


def create_avistamiento(datos, registros):
    # Avistamiento y todos sus registros se confirman en una sola transacción.
    with SessionLocal.begin() as session:
        avistamiento = Avistamiento(**datos)
        session.add(avistamiento)
        session.flush()
        for registro in registros:
            session.add(Registro(avistamiento_id=avistamiento.id, **registro))
        return avistamiento.id


def consulta_avistamientos(session):
    return session.query(Avistamiento).options(
        joinedload(Avistamiento.ave),
        joinedload(Avistamiento.comuna).joinedload(Comuna.region),
        joinedload(Avistamiento.voluntario).joinedload(Voluntario.comuna).joinedload(Comuna.region),
        joinedload(Avistamiento.registros),
    )


def get_ultimos_avistamientos():
    with SessionLocal() as session:
        return consulta_avistamientos(session).order_by(Avistamiento.id.desc()).limit(2).all()


def get_avistamientos(pagina=1, tipo="todos", orden="fecha-desc", page_size=5):
    with SessionLocal() as session:
        query = consulta_avistamientos(session)
        if tipo != "todos":
            query = query.filter(Avistamiento.tipo_ave == tipo)
        ordenes = {
            "fecha-desc": Avistamiento.fecha_hora.desc(),
            "fecha-asc": Avistamiento.fecha_hora.asc(),
            "lugar-asc": Avistamiento.lugar.asc(),
            "lugar-desc": Avistamiento.lugar.desc(),
        }
        total = query.count()
        paginas = max(1, (total + page_size - 1) // page_size)
        pagina = max(1, min(pagina, paginas))
        datos = query.order_by(ordenes[orden], Avistamiento.id.desc()).offset(
            (pagina - 1) * page_size
        ).limit(page_size).all()
        return datos, total, pagina, paginas


def get_avistamiento(id):
    with SessionLocal() as session:
        return consulta_avistamientos(session).filter(Avistamiento.id == id).first()


def get_comentarios(id):
    with SessionLocal() as session:
        if session.get(Avistamiento, id) is None:
            return None
        return session.query(Comentario).filter_by(avistamiento_id=id).order_by(
            Comentario.fecha.desc(), Comentario.id.desc()
        ).all()


def create_comentario(id, nombre, texto, fecha):
    with SessionLocal.begin() as session:
        if session.get(Avistamiento, id) is None:
            return None
        comentario = Comentario(avistamiento_id=id, nombre=nombre, texto=texto, fecha=fecha)
        session.add(comentario)
        session.flush()
        return comentario.id


def get_estadisticas():
    dia = func.date(Avistamiento.fecha_hora)
    with SessionLocal() as session:
        dias = session.query(dia, func.count(Avistamiento.id)).group_by(dia).order_by(dia).all()
        tipos = session.query(Avistamiento.tipo_ave, func.count(Avistamiento.id)).group_by(
            Avistamiento.tipo_ave
        ).order_by(Avistamiento.tipo_ave).all()
        comunas = session.query(Comuna.nombre, func.count(Voluntario.id)).join(
            Voluntario, Voluntario.comuna_id == Comuna.id
        ).group_by(Comuna.id, Comuna.nombre).order_by(Comuna.nombre, Comuna.id).all()
    return dias, tipos, comunas
