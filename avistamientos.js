
const avistamientos = [

    {
        nombre: "Cóndor andino",
        tipo: "rapaz",
        fecha: "2026-09-05",
        hora: "10:30",
        lugar: "Cajón del Maipo",
        region: "Metropolitana"
    },

    {
        nombre: "Pelícano",
        tipo: "marina",
        fecha: "2026-09-04",
        hora: "15:20",
        lugar: "Viña del Mar",
        region: "Valparaíso"
    },

    {
        nombre: "Cisne de cuello negro",
        tipo: "acuatica",
        fecha: "2026-09-03",
        hora: "09:15",
        lugar: "Santuario Carlos Anwandter",
        region: "Los Ríos"
    },

    {
        nombre: "Chucao",
        tipo: "terrestre",
        fecha: "2026-09-02",
        hora: "08:45",
        lugar: "Parque Nacional Alerce Andino",
        region: "Los Lagos"
    },

    {
        nombre: "Águila mora",
        tipo: "rapaz",
        fecha: "2026-09-01",
        hora: "12:10",
        lugar: "Farellones",
        region: "Metropolitana"
    },

    {
        nombre: "Gaviota dominicana",
        tipo: "marina",
        fecha: "2026-08-31",
        hora: "16:40",
        lugar: "Concón",
        region: "Valparaíso"
    },

    {
        nombre: "Tagua",
        tipo: "acuatica",
        fecha: "2026-08-30",
        hora: "11:05",
        lugar: "Laguna de Batuco",
        region: "Metropolitana"
    },

    {
        nombre: "Carpintero negro",
        tipo: "terrestre",
        fecha: "2026-08-29",
        hora: "13:30",
        lugar: "Parque Nacional Conguillío",
        region: "La Araucanía"
    },

    {
        nombre: "Halcón peregrino",
        tipo: "rapaz",
        fecha: "2026-08-28",
        hora: "17:25",
        lugar: "Cerro Provincia",
        region: "Metropolitana"
    },

    {
        nombre: "Pingüino de Humboldt",
        tipo: "marina",
        fecha: "2026-08-27",
        hora: "14:10",
        lugar: "Isla Damas",
        region: "Coquimbo"
    },

    {
        nombre: "Garza grande",
        tipo: "acuatica",
        fecha: "2026-08-26",
        hora: "07:50",
        lugar: "Humedal Río Maipo",
        region: "Valparaíso"
    },

    {
        nombre: "Loica",
        tipo: "terrestre",
        fecha: "2026-08-25",
        hora: "09:40",
        lugar: "Chillán",
        region: "Ñuble"
    }

];


// --------------------------------------------------
// CONFIGURACIÓN
// --------------------------------------------------

const avistamientosPorPagina = 5;

let paginaActual = 1;


// ELEMENTOS HTML


const tabla =
    document.getElementById("tabla-avistamientos");

const filtroTipo =
    document.getElementById("filtro-tipo");

const orden =
    document.getElementById("orden");

const botonAnterior =
    document.getElementById("boton-anterior");

const botonSiguiente =
    document.getElementById("boton-siguiente");

const informacionPagina =
    document.getElementById("informacion-pagina");

const cantidadResultados =
    document.getElementById("cantidad-resultados");

// NOMBRES DE LOS TIPOS


function obtenerNombreTipo(tipo) {

    const nombres = {
        rapaz: "Ave rapaz",
        marina: "Ave marina",
        acuatica: "Ave acuática",
        terrestre: "Ave terrestre",
        otro: "Otro"
    };

    return nombres[tipo];
}



// FILTRAR


function obtenerAvistamientosFiltrados() {

    const tipoSeleccionado =
        filtroTipo.value;


    if (tipoSeleccionado === "todos") {

        // Creamos una copia del arreglo original.
        return [...avistamientos];

    }


    return avistamientos.filter(
        function (avistamiento) {

            return (
                avistamiento.tipo === tipoSeleccionado
            );

        }
    );

}


// ORDENAR


function ordenarAvistamientos(lista) {

    const tipoOrden = orden.value;


    if (tipoOrden === "fecha-desc") {

        lista.sort(
            function (a, b) {

                return new Date(b.fecha)
                    - new Date(a.fecha);

            }
        );

    }


    else if (tipoOrden === "fecha-asc") {

        lista.sort(
            function (a, b) {

                return new Date(a.fecha)
                    - new Date(b.fecha);

            }
        );

    }


    else if (tipoOrden === "lugar-asc") {

        lista.sort(
            function (a, b) {

                return a.lugar.localeCompare(
                    b.lugar,
                    "es"
                );

            }
        );

    }


    else if (tipoOrden === "lugar-desc") {

        lista.sort(
            function (a, b) {

                return b.lugar.localeCompare(
                    a.lugar,
                    "es"
                );

            }
        );

    }


    return lista;

}



// FORMATEAR FECHA


function formatearFecha(fecha) {

    const partes = fecha.split("-");

    const anio = partes[0];
    const mes = partes[1];
    const dia = partes[2];

    return dia + "/" + mes + "/" + anio;

}



// CREAR FILA DE LA TABLA


function crearFila(avistamiento) {

    const fila =
        document.createElement("tr");


    const celdaNombre =
        document.createElement("td");

    celdaNombre.textContent =
        avistamiento.nombre;


    const celdaTipo =
        document.createElement("td");

    celdaTipo.textContent =
        obtenerNombreTipo(avistamiento.tipo);


    const celdaFecha =
        document.createElement("td");

    celdaFecha.textContent =
        formatearFecha(avistamiento.fecha);


    const celdaHora =
        document.createElement("td");

    celdaHora.textContent =
        avistamiento.hora;


    const celdaLugar =
        document.createElement("td");

    celdaLugar.textContent =
        avistamiento.lugar;


    const celdaRegion =
        document.createElement("td");

    celdaRegion.textContent =
        avistamiento.region;


    fila.appendChild(celdaNombre);
    fila.appendChild(celdaTipo);
    fila.appendChild(celdaFecha);
    fila.appendChild(celdaHora);
    fila.appendChild(celdaLugar);
    fila.appendChild(celdaRegion);


    return fila;

}



// MOSTRAR TABLA
function mostrarAvistamientos() {

    // Vaciar tabla anterior

    tabla.innerHTML = "";


    // Filtrar

    let lista =
        obtenerAvistamientosFiltrados();


    // Ordenar

    lista =
        ordenarAvistamientos(lista);


    // Cantidad encontrada

    cantidadResultados.textContent =
        "Se encontraron "
        + lista.length
        + " avistamientos.";


    // Número total de páginas

    const totalPaginas =
        Math.ceil(
            lista.length / avistamientosPorPagina
        );


    /*
     * Si después de aplicar un filtro la página
     * actual deja de existir, volvemos a la última
     * página válida.
     */

    if (
        paginaActual > totalPaginas
        && totalPaginas > 0
    ) {

        paginaActual = totalPaginas;

    }


    // Inicio y fin de los elementos de esta página

    const inicio =
        (paginaActual - 1)
        * avistamientosPorPagina;

    const fin =
        inicio + avistamientosPorPagina;


    const avistamientosPagina =
        lista.slice(inicio, fin);


    // Si no existen resultados

    if (avistamientosPagina.length === 0) {

        const fila =
            document.createElement("tr");

        const celda =
            document.createElement("td");

        celda.colSpan = 6;

        celda.textContent =
            "No se encontraron avistamientos.";

        fila.appendChild(celda);

        tabla.appendChild(fila);

    }

    else {

        for (
            const avistamiento
            of avistamientosPagina
        ) {

            const fila =
                crearFila(avistamiento);

            tabla.appendChild(fila);

        }

    }


    // Información de página

    if (totalPaginas === 0) {

        informacionPagina.textContent =
            "Página 0 de 0";

    }

    else {

        informacionPagina.textContent =
            "Página "
            + paginaActual
            + " de "
            + totalPaginas;

    }


    // Habilitar/deshabilitar botones

    botonAnterior.disabled =
        paginaActual <= 1;

    botonSiguiente.disabled =
        paginaActual >= totalPaginas;

}



// EVENTOS DE LOS FILTROS


filtroTipo.addEventListener(
    "change",
    function () {

        paginaActual = 1;

        mostrarAvistamientos();

    }
);


orden.addEventListener(
    "change",
    function () {

        paginaActual = 1;

        mostrarAvistamientos();

    }
);



// BOTÓN ANTERIOR


botonAnterior.addEventListener(
    "click",
    function () {

        if (paginaActual > 1) {

            paginaActual--;

            mostrarAvistamientos();

        }

    }
);



// BOTÓN SIGUIENTE

botonSiguiente.addEventListener(
    "click",
    function () {

        let lista =
            obtenerAvistamientosFiltrados();

        const totalPaginas =
            Math.ceil(
                lista.length
                / avistamientosPorPagina
            );


        if (paginaActual < totalPaginas) {

            paginaActual++;

            mostrarAvistamientos();

        }

    }
);


// CARGAR PÁGINA INICIAL


mostrarAvistamientos();