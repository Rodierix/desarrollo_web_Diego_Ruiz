# Clasificación de aves en el formulario

El archivo del curso `aves.sql` contiene los nombres de las especies. La aplicación les asigna un tipo en `database/tipos-por-especie.csv`. El vínculo usa el nombre completo para que funcione aunque MySQL haya asignado identificadores distintos al importar los datos.

Cada especie tiene una categoría para el gráfico. Se usa «rapaz» para las rapaces diurnas y nocturnas, «marina» para las especies asociadas principalmente al mar, «acuática» para las asociadas al agua o a humedales y «terrestre» para las de ambientes terrestres. Es una agrupación propia de esta tarea. Algunas especies frecuentan varios ambientes. Una especie añadida a MySQL que aún no tiene fila en el CSV queda bajo «Otro».

Por ejemplo, el águila pescadora figura como rapaz y el martín pescador como acuática. Elegir una especie completa su tipo. Elegir primero un tipo filtra las especies disponibles. Flask comprueba la misma correspondencia antes de guardar el avistamiento y sus archivos. La regla se aplica a los nuevos registros. Los conteos históricos reflejan el tipo guardado en cada avistamiento.

## Referencias

- Para el martín pescador se tomó como referencia su asociación con ríos y lagos. [Ficha de la Red de Observadores de Aves y Vida Silvestre de Chile](https://www.redobservadores.cl/wp-content/uploads/2024/09/Martin-pescador.pdf).
- Para las rapaces se consultó la guía del Ministerio del Medio Ambiente, que incluye al águila pescadora. [Aves rapaces de la Región Metropolitana de Santiago](https://mma.gob.cl/wp-content/uploads/2016/02/Libro-Aves-Rapaces-web.pdf).
- Para distinguir hábitats se consultó el atlas de la Red de Observadores. Las categorías del formulario conservan los ejemplos de la Tarea 1, como el pelícano marino, el cisne de cuello negro acuático y el chucao terrestre. [Atlas de las aves nidificantes de Chile](https://estrategia-aves.mma.gob.cl/wp-content/uploads/2023/03/Medrano_etal_2018_Atlas-de-las-aves-nidificantes-de-Chile.pdf).
