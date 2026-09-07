# Sistema de Avistamientos de Aves de Chile

Prototipo web desarrollado para la Tarea 1.  
El objetivo del sistema es permitir el registro y consulta de avistamientos de aves reportados por personas voluntarias en Chile.

## Tecnologías utilizadas

- HTML5
- CSS3
- JavaScript

El proyecto no utiliza servidor web ni base de datos, ya que corresponde a un prototipo de interfaz.

## Funcionalidades

### Registro de voluntarios

Permite ingresar información básica de una persona voluntaria, incluyendo:

- Nombre
- Apellido
- Correo electrónico
- Número de celular
- Región
- Comuna
- Dirección opcional

Las validaciones se realizan mediante JavaScript.

### Registro de avistamientos

Permite registrar:

- Tipo de ave
- Nombre del ave
- Región
- Comuna
- Lugar específico
- Fecha
- Hora
- Fotografía o video
- Descripción opcional

Se exige al menos un archivo de imagen o video.

### Consulta de avistamientos

La página de avistamientos permite:

- Visualizar registros de ejemplo
- Filtrar por tipo de ave
- Ordenar por fecha
- Ordenar por lugar
- Navegar entre páginas de resultados

### Estadísticas

Se muestran indicadores y gráficos simples relacionados con:

- Cantidad de voluntarios
- Cantidad de avistamientos
- Número de especies observadas
- Regiones con avistamientos
- Avistamientos por tipo de ave
- Voluntarios por región
- Avistamientos por región

## Estructura del proyecto

```text
proyecto/
│
├── index.html
├── registro-voluntario.html
├── registrar-avistamiento.html
├── avistamientos.html
├── estadisticas.html
│
├── estilos.css
│
├── voluntario.js
├── avistamiento.js
├── avistamientos.js
├── estadisticas.js
│
└── README.md
```

## Decisiones de implementación

### Validaciones en JavaScript

Las validaciones de los formularios se implementan directamente en JavaScript y no dependen del atributo `required` de HTML.

### Validación de la fecha del avistamiento

Se definió que la fecha de un avistamiento:

- No puede estar en el futuro.
- No puede tener más de 30 días de antigüedad.

Esta regla busca mantener actualizado el registro de avistamientos.

### Archivos multimedia

Cada avistamiento debe incluir al menos una fotografía o video.  
Se validan los tipos de archivo permitidos y se limita el tamaño máximo por archivo.

### Datos de ejemplo

Los avistamientos, voluntarios y estadísticas mostrados corresponden a datos de prueba definidos en JavaScript.

### HTML semántico

Se utilizaron etiquetas HTML semánticas como:

- `header`
- `nav`
- `main`
- `section`
- `article`
- `fieldset`
- `footer`

Esto permite mantener una estructura clara y evitar el uso innecesario de elementos `div`.

### Diseño adaptable

La hoja de estilos incluye reglas responsivas para que las páginas puedan visualizarse correctamente tanto en computadores como en pantallas pequeñas.

## Ejecución

No es necesario instalar dependencias.

Para ejecutar el proyecto basta con abrir:

```text
index.html
```

directamente en un navegador web.

Desde la página principal se puede navegar hacia las distintas funcionalidades del sistema.


