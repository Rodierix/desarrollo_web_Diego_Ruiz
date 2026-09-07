const formulario = document.getElementById("form-avistamiento");

const contenedorErrores =
    document.getElementById("mensajes-error");


formulario.addEventListener("submit", function (event) {

  
    event.preventDefault();

    const errores = [];


 
    const tipoAve =
        document.getElementById("tipo-ave").value;

    const nombreAve =
        document.getElementById("nombre-ave").value.trim();

    const region =
        document.getElementById("region").value;

    const comuna =
        document.getElementById("comuna").value.trim();

    const lugar =
        document.getElementById("lugar").value.trim();

    const fecha =
        document.getElementById("fecha").value;

    const hora =
        document.getElementById("hora").value;

    const archivos =
        document.getElementById("archivo").files;


    // Validar tipo de ave


    if (tipoAve === "") {
        errores.push(
            "Debe seleccionar un tipo de ave."
        );
    }



    // Validar nombre del ave


    if (nombreAve === "") {

        errores.push(
            "Debe ingresar el nombre del ave."
        );

    } else if (nombreAve.length < 2) {

        errores.push(
            "El nombre del ave debe tener al menos 2 caracteres."
        );

    } else if (nombreAve.length > 100) {

        errores.push(
            "El nombre del ave no puede superar los 100 caracteres."
        );
    }


    // Validar región
  

    if (region === "") {
        errores.push(
            "Debe seleccionar una región."
        );
    }


    // Validar comuna
   

    if (comuna === "") {

        errores.push(
            "Debe ingresar la comuna del avistamiento."
        );

    } else if (comuna.length < 2) {

        errores.push(
            "La comuna debe tener al menos 2 caracteres."
        );
    }



    // Validar lugar
    

    if (lugar === "") {

        errores.push(
            "Debe indicar el lugar del avistamiento."
        );

    } else if (lugar.length < 3) {

        errores.push(
            "El lugar debe tener al menos 3 caracteres."
        );
    }



    // Validar fecha


    if (fecha === "") {

        errores.push(
            "Debe ingresar la fecha del avistamiento."
        );

    } else {

        validarFecha(fecha, errores);

    }



    // Validar hora


    if (hora === "") {
        errores.push(
            "Debe ingresar la hora del avistamiento."
        );
    }



    // Validar archivos

    validarArchivos(archivos, errores);



    // Mostrar resultado
   

    if (errores.length > 0) {

        mostrarErrores(errores);

    } else {

        mostrarExito();

    }

});


function validarFecha(fechaIngresada, errores) {
    
    
    // Aqui se le agrega una hora para no tener problema
    // con zona horaria
    const fechaAvistamiento =
        new Date(fechaIngresada + "T00:00:00");

    const hoy = new Date();

    hoy.setHours(0, 0, 0, 0);


    // No puede estar en el futuro

    if (fechaAvistamiento > hoy) {

        errores.push(
            "La fecha del avistamiento no puede estar en el futuro."
        );

        return;
    }


    // Solo se permitiran hace máximo 30 días
    const hace30Dias = new Date(hoy);

    hace30Dias.setDate(
        hace30Dias.getDate() - 30
    );


    if (fechaAvistamiento < hace30Dias) {

        errores.push(
            "El avistamiento no puede tener más de 30 días de antigüedad."
        );

    }

}


function validarArchivos(archivos, errores) {

    // Debe existir al menos un archivo

    if (archivos.length === 0) {

        errores.push(
            "Debe agregar al menos una fotografía o video."
        );

        return;
    }


    const tiposPermitidos = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "video/mp4",
        "video/webm"
    ];


    // Máximo 20 MB por archivo

    const tamanoMaximo =
        20 * 1024 * 1024;


    for (const archivo of archivos) {

        if (!tiposPermitidos.includes(archivo.type)) {

            errores.push(
                "El archivo \"" +
                archivo.name +
                "\" no tiene un formato permitido."
            );

        }


        if (archivo.size > tamanoMaximo) {

            errores.push(
                "El archivo \"" +
                archivo.name +
                "\" supera el máximo de 20 MB."
            );

        }

    }

}


function mostrarErrores(errores) {

    contenedorErrores.innerHTML = "";


    const titulo =
        document.createElement("p");

    titulo.textContent =
        "No fue posible registrar el avistamiento:";


    const lista =
        document.createElement("ul");


    for (const error of errores) {

        const elemento =
            document.createElement("li");

        elemento.textContent = error;

        lista.appendChild(elemento);

    }


    contenedorErrores.appendChild(titulo);

    contenedorErrores.appendChild(lista);


    contenedorErrores.classList.remove(
        "mensaje-exito"
    );

    contenedorErrores.classList.add(
        "mensaje-error"
    );

}


function mostrarExito() {

    contenedorErrores.innerHTML = "";


    const mensaje =
        document.createElement("p");


    mensaje.textContent =
        "El avistamiento fue registrado correctamente.";


    contenedorErrores.appendChild(mensaje);


    contenedorErrores.classList.remove(
        "mensaje-error"
    );

    contenedorErrores.classList.add(
        "mensaje-exito"
    );

}