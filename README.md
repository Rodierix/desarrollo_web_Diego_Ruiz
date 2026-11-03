# Tarea 3 · Avistamientos de aves en Chile

Aplicación Flask. Desde la portada se puede abrir **Estadísticas** o seleccionar un avistamiento para leer y agregar comentarios.

## Ejecutar

Desde esta carpeta, con Python 3.10 o superior:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe -m flask --app app run
```

Abrir <http://127.0.0.1:5000>. La configuración predeterminada usa el usuario `cc5002` de la base MySQL `tarea2` en `localhost:3306`. Si es una instalación nueva, ejecutar primero `database/create_db.sql` con una cuenta administradora. Si la base ya tiene registros, basta con ejecutar `init-db` antes de iniciar Flask. Este comando aplica `tabla-comentario.sql` y conserva los datos. El archivo histórico `tarea2.sql` contiene una instrucción que elimina la base completa.

Se puede elegir otra conexión con `DATABASE_URL` y fijar la clave de sesión con `SECRET_KEY`.

## Estadísticas y comentarios

El formulario comprueba que la especie corresponda al tipo seleccionado. [Criterios de clasificación](Clasificacion-de-aves.md).

La fecha del gráfico de líneas es la del avistamiento. La barra de cada comuna cuenta a los voluntarios registrados allí, aunque hayan observado aves en otra comuna. Los gráficos usan Highcharts 12.4.0, como en el Auxiliar 8. Los archivos de la biblioteca y su módulo de accesibilidad se sirven desde `static/vendor/`. [Uso educativo de Highcharts](https://www.highcharts.com/education/).

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan SQLite temporal. Cubren el registro y listado de la Tarea 2 y verifican los conteos, los límites del comentario, el token CSRF y la separación de comentarios por avistamiento.
