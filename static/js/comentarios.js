const formulario = document.getElementById("form-comentario");
const lista = document.getElementById("lista-comentarios");
const estadoLista = document.getElementById("estado-lista");
const estadoEnvio = document.getElementById("estado-envio");
const boton = formulario.querySelector('button[type="submit"]');

function mostrarComentarios(comentarios) {
    lista.replaceChildren();
    estadoLista.textContent = comentarios.length ? "" : "Aún no hay comentarios para este avistamiento.";
    for (const comentario of comentarios) {
        const item = document.createElement("li");
        const autor = document.createElement("strong");
        const texto = document.createElement("p");
        autor.textContent = comentario.nombre;
        texto.textContent = comentario.texto;
        item.append(autor, " · " + comentario.fecha, texto);
        lista.append(item);
    }
}

async function cargarComentarios() {
    try {
        const respuesta = await fetch(formulario.action);
        if (!respuesta.ok) throw new Error();
        mostrarComentarios(await respuesta.json());
    } catch {
        estadoLista.textContent = "No se pudo cargar el listado de comentarios. Recargue la página para reintentar.";
    }
}

formulario.addEventListener("submit", async evento => {
    evento.preventDefault();
    if (boton.disabled) return;
    const datos = new FormData(formulario);
    const nombre = Array.from(datos.get("nombre").trim()).length;
    const texto = Array.from(datos.get("texto").trim()).length;
    const errores = [];
    if (nombre < 3 || nombre > 50) errores.push("El nombre debe tener entre 3 y 50 caracteres.");
    if (texto < 5 || texto > 300) errores.push("El comentario debe tener entre 5 y 300 caracteres.");
    if (errores.length) {
        estadoEnvio.textContent = errores.join(" ");
        return;
    }
    boton.disabled = true;
    estadoEnvio.textContent = "Guardando comentario…";
    try {
        const respuesta = await fetch(formulario.action, { method: "POST", body: datos });
        const resultado = await respuesta.json();
        if (!respuesta.ok) {
            estadoEnvio.textContent = resultado.errores.join(" ");
            return;
        }
        formulario.reset();
        estadoEnvio.textContent = "Comentario agregado.";
        await cargarComentarios();
    } catch {
        estadoEnvio.textContent = "No se pudo confirmar el envío. Revise el listado antes de reintentar.";
    } finally {
        boton.disabled = false;
    }
});

boton.disabled = true;
cargarComentarios().finally(() => { boton.disabled = false; });
