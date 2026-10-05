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
        /^(?:\+?56)?9\d{8}$/;

    if (!expresionCelular.test(celular.replace(/\s/g, ""))) {
        errores.push("Debe ingresar un número de celular válido.");
    }

    if ((nombre + " " + apellido).length > 255) {
        errores.push("El nombre y apellido juntos no pueden superar los 255 caracteres.");
    }
    if (email.length > 80) {
        errores.push("El correo electrónico no puede superar los 80 caracteres.");
    }
    if (selectorRegion.value === "" || selectorComuna.value === "") {
        errores.push("Debe seleccionar una región y una comuna.");
    }
    if (document.getElementById("direccion").value.trim().length > 200) {
        errores.push("La dirección no puede superar los 200 caracteres.");
    }

    if (errores.length > 0) {
        mostrarErrores(errores);
        return;
    }

    if (window.confirm("¿Confirma el registro del voluntario?")) {
        formulario.submit();
    }
});
