const formulario = document.getElementById("form-voluntario");

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const email = document.getElementById("email").value.trim();
    const celular = document.getElementById("celular").value.trim();

    let errores = [];

    if (nombre.length < 2) {
        errores.push("El nombre debe contener al menos 2 caracteres.");
    }

    if (apellido.length < 2) {
        errores.push("El apellido debe contener al menos 2 caracteres.");
    }

    const expresionEmail =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!expresionEmail.test(email)) {
        errores.push("Debe ingresar un correo electrónico válido.");
    }

    const expresionCelular =
        /^\+?56?9\d{8}$/;

    if (!expresionCelular.test(celular.replace(/\s/g, ""))) {
        errores.push("Debe ingresar un número de celular válido.");
    }

    if (errores.length > 0) {
        mostrarErrores(errores);
        return;
    }

    alert("Voluntario registrado correctamente.");
});