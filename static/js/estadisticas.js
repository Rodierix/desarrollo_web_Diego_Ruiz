

// DATOS DE EJEMPLO


const voluntarios = [

    {
        nombre: "Ana",
        region: "Metropolitana"
    },

    {
        nombre: "Pedro",
        region: "Valparaíso"
    },

    {
        nombre: "María",
        region: "Metropolitana"
    },

    {
        nombre: "Carlos",
        region: "Los Lagos"
    },

    {
        nombre: "Javiera",
        region: "Metropolitana"
    },

    {
        nombre: "Tomás",
        region: "La Araucanía"
    },

    {
        nombre: "Sofía",
        region: "Valparaíso"
    },

    {
        nombre: "Diego",
        region: "Coquimbo"
    },

    {
        nombre: "Camila",
        region: "Los Ríos"
    },

    {
        nombre: "Felipe",
        region: "Metropolitana"
    }

];


const avistamientos = [

    {
        nombre: "Cóndor andino",
        tipo: "rapaz",
        region: "Metropolitana"
    },

    {
        nombre: "Pelícano",
        tipo: "marina",
        region: "Valparaíso"
    },

    {
        nombre: "Cisne de cuello negro",
        tipo: "acuatica",
        region: "Los Ríos"
    },

    {
        nombre: "Chucao",
        tipo: "terrestre",
        region: "Los Lagos"
    },

    {
        nombre: "Águila mora",
        tipo: "rapaz",
        region: "Metropolitana"
    },

    {
        nombre: "Gaviota dominicana",
        tipo: "marina",
        region: "Valparaíso"
    },

    {
        nombre: "Tagua",
        tipo: "acuatica",
        region: "Metropolitana"
    },

    {
        nombre: "Carpintero negro",
        tipo: "terrestre",
        region: "La Araucanía"
    },

    {
        nombre: "Halcón peregrino",
        tipo: "rapaz",
        region: "Metropolitana"
    },

    {
        nombre: "Pingüino de Humboldt",
        tipo: "marina",
        region: "Coquimbo"
    },

    {
        nombre: "Garza grande",
        tipo: "acuatica",
        region: "Valparaíso"
    },

    {
        nombre: "Loica",
        tipo: "terrestre",
        region: "Ñuble"
    }

];



// ELEMENTOS HTML


const totalVoluntarios =
    document.getElementById("total-voluntarios");

const totalAvistamientos =
    document.getElementById("total-avistamientos");

const totalEspecies =
    document.getElementById("total-especies");

const totalRegiones =
    document.getElementById("total-regiones");

const graficoTipos =
    document.getElementById("grafico-tipos");

const graficoVoluntarios =
    document.getElementById("grafico-voluntarios");

const graficoRegiones =
    document.getElementById("grafico-regiones");



// NOMBRES DE LOS TIPOS DE AVE


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



// INDICADORES GENERALES


function mostrarIndicadores() {

    // Total de voluntarios

    totalVoluntarios.textContent =
        voluntarios.length;


    // Total de avistamientos

    totalAvistamientos.textContent =
        avistamientos.length;


    // Obtener especies diferentes

    const especies = [];

    for (const avistamiento of avistamientos) {

        if (!especies.includes(avistamiento.nombre)) {

            especies.push(avistamiento.nombre);

        }

    }

    totalEspecies.textContent =
        especies.length;


    // Obtener regiones diferentes

    const regiones = [];

    for (const avistamiento of avistamientos) {

        if (!regiones.includes(avistamiento.region)) {

            regiones.push(avistamiento.region);

        }

    }

    totalRegiones.textContent =
        regiones.length;

}


// CONTAR AVISTAMIENTOS POR TIPO


function contarPorTipo() {

    const cantidades = {};

    for (const avistamiento of avistamientos) {

        const tipo = avistamiento.tipo;

        if (cantidades[tipo] === undefined) {

            cantidades[tipo] = 1;

        } else {

            cantidades[tipo]++;

        }

    }

    return cantidades;

}



// CONTAR VOLUNTARIOS POR REGIÓN

function contarVoluntariosPorRegion() {

    const cantidades = {};

    for (const voluntario of voluntarios) {

        const region = voluntario.region;

        if (cantidades[region] === undefined) {

            cantidades[region] = 1;

        } else {

            cantidades[region]++;

        }

    }

    return cantidades;

}



// CONTAR AVISTAMIENTOS POR REGIÓN


function contarAvistamientosPorRegion() {

    const cantidades = {};

    for (const avistamiento of avistamientos) {

        const region = avistamiento.region;

        if (cantidades[region] === undefined) {

            cantidades[region] = 1;

        } else {

            cantidades[region]++;

        }

    }

    return cantidades;

}



// CREAR GRÁFICO DE BARRAS


function crearGrafico(contenedor, datos, cambiarNombreTipo) {

    // Vaciar el gráfico antes de dibujarlo

    contenedor.innerHTML = "";


    // Encontrar el valor más alto

    let maximo = 0;

    for (const clave in datos) {

        if (datos[clave] > maximo) {

            maximo = datos[clave];

        }

    }


    // Crear una barra por cada elemento

    for (const clave in datos) {

        const cantidad = datos[clave];


        // Porcentaje relativo al mayor valor

        const porcentaje =
            (cantidad / maximo) * 100;


        // Elemento de la lista

        const elemento =
            document.createElement("li");


        // Nombre

        const nombre =
            document.createElement("span");

        nombre.classList.add("nombre-barra");


        if (cambiarNombreTipo) {

            nombre.textContent =
                obtenerNombreTipo(clave);

        } else {

            nombre.textContent =
                clave;

        }


        // Contenedor de la barra

        const barraExterior =
            document.createElement("span");

        barraExterior.classList.add(
            "barra-exterior"
        );


        // Barra

        const barraInterior =
            document.createElement("span");

        barraInterior.classList.add(
            "barra-interior"
        );

        barraInterior.style.width =
            porcentaje + "%";


        // Número

        const valor =
            document.createElement("span");

        valor.classList.add("valor-barra");

        valor.textContent = cantidad;


        barraExterior.appendChild(
            barraInterior
        );


        elemento.appendChild(nombre);

        elemento.appendChild(
            barraExterior
        );

        elemento.appendChild(valor);


        contenedor.appendChild(
            elemento
        );

    }

}


// CREAR TODOS LOS GRÁFICOS


function mostrarGraficos() {

    const tipos =
        contarPorTipo();

    const voluntariosRegion =
        contarVoluntariosPorRegion();

    const avistamientosRegion =
        contarAvistamientosPorRegion();


    crearGrafico(
        graficoTipos,
        tipos,
        true
    );


    crearGrafico(
        graficoVoluntarios,
        voluntariosRegion,
        false
    );


    crearGrafico(
        graficoRegiones,
        avistamientosRegion,
        false
    );

}



// INICIAR PÁGINA


mostrarIndicadores();

mostrarGraficos();