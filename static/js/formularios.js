// Catálogos servidos por Flask: sólo mostrar comunas de la región seleccionada.
const selectorRegion = document.getElementById("region");
const selectorComuna = document.getElementById("comuna");

function actualizarComunas() {
    for (const opcion of selectorComuna.options) {
        if (opcion.value !== "") {
            const pertenece = opcion.dataset.region === selectorRegion.value;
            opcion.hidden = !pertenece;
            opcion.disabled = !pertenece;
        }
    }
    if (selectorComuna.selectedOptions[0]?.disabled) {
        selectorComuna.value = "";
    }
}

selectorRegion.addEventListener("change", actualizarComunas);
actualizarComunas();

function mostrarErrores(errores) {
    const contenedor = document.getElementById("mensajes-error");
    contenedor.replaceChildren();
    const titulo = document.createElement("p");
    titulo.textContent = "Revise los siguientes datos:";
    const lista = document.createElement("ul");
    for (const error of errores) {
        const elemento = document.createElement("li");
        elemento.textContent = error;
        lista.appendChild(elemento);
    }
    contenedor.append(titulo, lista);
    contenedor.classList.add("mensaje-error");
    contenedor.scrollIntoView({block: "center"});
}

document.querySelector("form").addEventListener("reset", function () {
    // Esperar que el navegador restablezca los valores originales.
    setTimeout(function () {
        actualizarComunas();
        const contenedor = document.getElementById("mensajes-error");
        contenedor.replaceChildren();
        contenedor.classList.remove("mensaje-error");
    }, 0);
});
