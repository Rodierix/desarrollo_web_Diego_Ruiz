# Tarea 2: avistamientos de aves en Chile

Aplicación Flask con MySQL y SQLAlchemy basada en los formularios y estilos de la tarea 1.

## Ejecutar

Se necesita Python 3.10 o superior y un servidor MySQL en `localhost:3306`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En MySQL Workbench o en una consola MySQL con permisos de administrador, ejecutar
`database/create_db.sql`. Crea la base `tarea2` y el usuario `cc5002`, con contraseña
`programacionweb`, sin borrar datos. Si ese usuario ya existe, debe tener esa contraseña.

Luego, desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe -m flask --app app run
```

Abrir <http://127.0.0.1:5000>. Las páginas se abren mediante Flask, no directamente
como archivos HTML. Registrar primero un voluntario; la confirmación ofrece informar
un avistamiento con ese voluntario seleccionado.

`init-db` crea las tablas mediante los modelos SQLAlchemy e importa los catálogos
desde los archivos originales `region-comuna.sql` y `aves.sql`. Cada catálogo se
carga sólo si su tabla está vacía. Se puede repetir el comando sin duplicar los
catálogos completos ni borrar registros. Si ya se importó `tarea2.sql`, el comando
agrega las tres columnas descritas abajo. El archivo original `tarea2.sql` se conserva
sin cambios, pero contiene `DROP SCHEMA`: no ejecutarlo sobre una base con datos que
se deseen conservar.

La conexión usa por defecto las credenciales del enunciado. Opcionalmente se puede
configurar `DATABASE_URL`. `SECRET_KEY` permite fijar la clave de sesión; si no se
define, se genera una al iniciar y los formularios abiertos antes de reiniciar
deben recargarse. `FLASK_DEBUG=1` activa el modo de desarrollo al ejecutar `python app.py`.

## Código reutilizado

- De `Ejemplos/flask_app_6/app.py`: rutas Flask con GET/POST, `request.form`,
  `request.files`, renderizado Jinja, redirecciones y nombres de archivos con
  `secure_filename`, SHA-256 y UUID.
- De `Ejemplos/flask_app_6/database/db.py`: `create_engine`, `SessionLocal`,
  `declarative_base`, clases con columnas y relaciones, y funciones de consulta.
- De `Ejemplos/flask_app_6/utils/validations.py`: módulo separado de validaciones y
  comprobación de tipo de archivo mediante `filetype`.
- De la tarea 1: formularios en `template/`, estilos en `static/css/estilos.css`,
  validaciones JavaScript, filtros, tipos de aves y paginación de cinco resultados.
  El encabezado y pie compartidos se extrajeron a `template/base.html`, siguiendo
  la herencia de plantillas de los ejemplos. Se conserva el nombre `template/`
  que tenía esta carpeta y se configura explícitamente en Flask.

## Decisiones de implementación

- Se conservan las seis tablas del esquema entregado. Se agregan
  `voluntario.direccion` (opcional), `avistamiento.tipo_ave` y
  `avistamiento.comuna_id` para guardar los datos que solicitaba la tarea 1.
  La región se obtiene por la relación con la comuna. La ubicación de un
  avistamiento puede ser distinta de la comuna del voluntario.
- `nombre` y `apellido` se validan por separado y se guardan juntos en
  `voluntario.nombre`. `fecha_registro` se asigna en el servidor con la hora de
  `America/Santiago`. El teléfono se almacena sin espacios.
- Las aves, regiones, comunas y voluntarios se seleccionan desde los catálogos de
  la base. El tipo de ave se informa para cada avistamiento porque el catálogo
  entregado no clasifica las especies por tipo.
- Los registros anteriores a la ampliación del esquema reciben tipo `otro` y,
  si no tienen comuna propia, se muestra la comuna de su voluntario.
- Se mantienen las reglas de la tarea 1: nombres de al menos dos caracteres,
  correo y celular válidos, lugar de al menos tres caracteres, fecha entre hoy
  y los últimos 30 días inclusive, hora obligatoria y al menos un archivo.
  Se corrige la expresión del celular para aceptar `912345678`, `56912345678`
  y `+56912345678`, con o sin espacios. También se verifican longitudes máximas,
  existencia de los identificadores y correspondencia de región y comuna.
- Fotos JPG/PNG/WebP y videos MP4/WebM, hasta 20 MB por archivo y diez archivos
  por avistamiento. Se comprueban tamaño, extensión y firma del contenido;
  no se confía en el MIME declarado por el navegador. La firma identifica el
  formato; no garantiza que un archivo multimedia dañado se pueda reproducir.
- Los archivos se guardan en `static/uploads/`. La tabla `registro` conserva el
  nombre original y la ruta generada. El avistamiento y sus registros se insertan
  en una transacción; si falla, se retiran los archivos guardados en ese intento.
- El servidor repite las validaciones aunque se desactive JavaScript. Los errores
  mantienen el formulario y sus valores; los archivos se deben volver a seleccionar
  por las restricciones del navegador. El éxito usa redirección para evitar
  repetir el POST al recargar.
- La portada muestra los últimos **dos agregados** (ID descendente), aunque la
  fecha observada sea anterior. El listado filtra y pagina en la base de datos,
  con cinco filas por página y desempate por ID. Cada fila abre un detalle con
  los archivos; las fotos se pueden abrir en tamaño original.


## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan una base SQLite temporal con claves foráneas activadas y una
carpeta temporal de archivos; no modifican MySQL ni las cargas del usuario.
Cubren registros, errores de validación sin JavaScript, fechas límite, archivos,
detalle, filtros, paginación, escape de HTML, CSRF y reversión ante fallos.
La configuración normal de la aplicación sigue usando MySQL. Estas pruebas no
sustituyen comprobar la conexión y la inicialización en el MySQL de evaluación.


