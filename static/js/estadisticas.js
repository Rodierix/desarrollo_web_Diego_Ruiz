const estado = document.getElementById("estado-estadisticas");
const urlDatos = document.getElementById("estadisticas").dataset.url;

function mostrarDias(dias) {
    if (!dias.length) {
        document.getElementById("grafico-dias").textContent = "Aún no hay avistamientos registrados.";
        return;
    }
    const puntos = [];
    const unDia = 24 * 60 * 60 * 1000;
    for (const dia of dias) {
        const [anio, mes, numero] = dia.fecha.split("-").map(Number);
        const fecha = Date.UTC(anio, mes - 1, numero);
        if (puntos.length) {
            for (let i = puntos[puntos.length - 1][0] + unDia; i < fecha; i += unDia) {
                puntos.push([i, 0]);
            }
        }
        puntos.push([fecha, dia.total]);
    }
    Highcharts.chart("grafico-dias", {
        chart: { type: "line" },
        title: { text: null },
        xAxis: { type: "datetime", minTickInterval: unDia, title: { text: "Día del avistamiento" } },
        yAxis: { min: 0, allowDecimals: false, title: { text: "Cantidad de avistamientos" } },
        tooltip: { shared: true, crosshairs: true, xDateFormat: "%d-%m-%Y" },
        series: [{ name: "Avistamientos", data: puntos, lineWidth: 1,
                   marker: { enabled: true, radius: 4 }, color: "#245c45" }]
    });
}

function mostrarTipos(tipos) {
    if (!tipos.length) {
        document.getElementById("grafico-tipos").textContent = "Aún no hay avistamientos registrados.";
        return;
    }
    Highcharts.chart("grafico-tipos", {
        chart: { type: "pie" },
        title: { text: null },
        series: [{ name: "Avistamientos", data: tipos.map(item => ({ name: item.tipo, y: item.total })) }]
    });
}

function mostrarComunas(comunas) {
    if (!comunas.length) {
        document.getElementById("grafico-comunas").textContent = "Aún no hay voluntarios registrados.";
        return;
    }
    Highcharts.chart("grafico-comunas", {
        chart: { type: "column", scrollablePlotArea: { minWidth: comunas.length * 65 } },
        title: { text: null },
        xAxis: { categories: comunas.map(item => item.comuna), title: { text: "Comuna" } },
        yAxis: { min: 0, allowDecimals: false, title: { text: "Cantidad de voluntarios" } },
        series: [{ name: "Voluntarios", data: comunas.map(item => item.total), color: "#528064" }]
    });
}

fetch(urlDatos)
    .then(response => {
        if (!response.ok) throw new Error("No se pudieron cargar las estadísticas.");
        return response.json();
    })
    .then(data => {
        Highcharts.setOptions({ lang: { locale: "es-CL" } });
        mostrarDias(data.dias);
        mostrarTipos(data.tipos);
        mostrarComunas(data.comunas);
        estado.textContent = "";
    })
    .catch(() => {
        estado.textContent = "No se pudieron cargar las estadísticas. Vuelva a intentar.";
    });
