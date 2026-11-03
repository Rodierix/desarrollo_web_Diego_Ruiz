"""Validaciones del servidor, siguiendo utils/validations.py de los ejemplos."""
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import filetype

TIPOS_AVES = {
    "rapaz": "Ave rapaz", "marina": "Ave marina", "acuatica": "Ave acuática",
    "terrestre": "Ave terrestre", "otro": "Otro",
}
MAX_ARCHIVO = 20 * 1024 * 1024
MAX_ARCHIVOS = 10
FORMATOS = {
    "image/jpeg": {".jpg", ".jpeg"}, "image/png": {".png"},
    "image/webp": {".webp"}, "video/mp4": {".mp4"}, "video/webm": {".webm"},
}


def ahora_chile():
    return datetime.now(ZoneInfo("America/Santiago")).replace(tzinfo=None)


def entero(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def validate_comentario(form):
    errores = []
    nombre = form.get("nombre", "").strip()
    texto = form.get("texto", "").replace("\r\n", "\n").strip()
    if not 3 <= len(nombre) <= 50:
        errores.append("El nombre debe tener entre 3 y 50 caracteres.")
    if not 5 <= len(texto) <= 300:
        errores.append("El comentario debe tener entre 5 y 300 caracteres.")
    return errores, nombre, texto


def validar_comuna(form, catalogos, errores):
    region = entero(form.get("region"))
    comuna = entero(form.get("comuna"))
    if not any(r.id == region for r in catalogos["regiones"]):
        errores.append("Debe seleccionar una región válida.")
    if not any(c.id == comuna and c.region_id == region for c in catalogos["comunas"]):
        errores.append("Debe seleccionar una comuna perteneciente a la región indicada.")
    return comuna


def validate_voluntario(form, catalogos):
    errores = []
    nombre = form.get("nombre", "").strip()
    apellido = form.get("apellido", "").strip()
    email = form.get("email", "").strip()
    telefono = re.sub(r"\s", "", form.get("celular", ""))
    direccion = form.get("direccion", "").strip()
    if len(nombre) < 2:
        errores.append("El nombre debe contener al menos 2 caracteres.")
    if len(apellido) < 2:
        errores.append("El apellido debe contener al menos 2 caracteres.")
    if len(nombre + " " + apellido) > 255:
        errores.append("El nombre y apellido juntos no pueden superar los 255 caracteres.")
    if len(email) > 80 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        errores.append("Debe ingresar un correo electrónico válido de hasta 80 caracteres.")
    if not re.fullmatch(r"(?:\+?56)?9\d{8}", telefono):
        errores.append("Debe ingresar un número de celular válido (por ejemplo, +56 9 1234 5678).")
    if len(direccion) > 200:
        errores.append("La dirección no puede superar los 200 caracteres.")
    comuna = validar_comuna(form, catalogos, errores)
    return errores, {
        "nombre": nombre + " " + apellido, "email": email, "telefono": telefono,
        "direccion": direccion or None, "comuna_id": comuna, "fecha_registro": ahora_chile(),
    }


def validate_archivos(archivos):
    errores, formatos = [], []
    if not archivos:
        errores.append("Debe agregar al menos una fotografía o video.")
    if len(archivos) > MAX_ARCHIVOS:
        errores.append("Puede adjuntar como máximo 10 archivos por avistamiento.")
    for archivo in archivos:
        archivo.stream.seek(0, 2)
        size = archivo.stream.tell()
        archivo.stream.seek(0)
        tipo = filetype.guess(archivo.stream.read(8192))
        archivo.stream.seek(0)
        if size == 0 or size > MAX_ARCHIVO:
            errores.append(f'El archivo "{archivo.filename}" debe pesar entre 1 byte y 20 MB.')
        if (tipo is None or tipo.mime not in FORMATOS
                or Path(archivo.filename).suffix.lower() not in FORMATOS.get(tipo.mime, set())):
            errores.append(f'El archivo "{archivo.filename}" no tiene un formato permitido o su contenido no coincide.')
        if len(archivo.filename) > 300:
            errores.append("El nombre de cada archivo debe tener hasta 300 caracteres.")
        formatos.append(tipo)
    return errores, formatos


def validate_avistamiento(form, archivos, catalogos):
    errores = []
    voluntario = entero(form.get("voluntario"))
    ave = entero(form.get("nombre-ave"))
    tipo = form.get("tipo-ave", "")
    lugar = form.get("lugar", "").strip()
    descripcion = form.get("descripcion", "").strip()
    if not any(v.id == voluntario for v in catalogos["voluntarios"]):
        errores.append("Debe seleccionar un voluntario registrado.")
    especie = next((a for a in catalogos["aves"] if a.id == ave), None)
    if especie is None:
        errores.append("Debe seleccionar un ave del catálogo.")
    if tipo not in TIPOS_AVES:
        errores.append("Debe seleccionar un tipo de ave válido.")
    elif especie is not None and tipo != especie.tipo:
        errores.append(f'Para {especie.nombre}, seleccione «{TIPOS_AVES[especie.tipo]}».')
    comuna = validar_comuna(form, catalogos, errores)
    if not 3 <= len(lugar) <= 200:
        errores.append("El lugar debe tener entre 3 y 200 caracteres.")
    if len(descripcion) > 500:
        errores.append("La descripción no puede superar los 500 caracteres.")
    fecha_hora = None
    try:
        fecha_hora = datetime.strptime(form.get("fecha", "") + " " + form.get("hora", ""), "%Y-%m-%d %H:%M")
        hoy = ahora_chile().date()
        if fecha_hora.date() > hoy:
            errores.append("La fecha del avistamiento no puede estar en el futuro.")
        if fecha_hora.date() < hoy - timedelta(days=30):
            errores.append("El avistamiento no puede tener más de 30 días de antigüedad.")
    except ValueError:
        errores.append("Debe ingresar una fecha y hora válidas.")
    errores_archivos, formatos = validate_archivos(archivos)
    errores.extend(errores_archivos)
    return errores, {
        "voluntario_id": voluntario, "ave_id": ave, "tipo_ave": tipo,
        "comuna_id": comuna, "lugar": lugar, "descripcion": descripcion or None,
        "fecha_hora": fecha_hora,
    }, formatos
