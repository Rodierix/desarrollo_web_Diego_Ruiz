// El listado, los filtros y la paginación ahora se resuelven en Flask y SQLAlchemy.
// El enlace de cada ave también permite abrir el detalle usando el teclado.
document.querySelectorAll(".fila-avistamiento").forEach(function (fila) {
    fila.addEventListener("click", function (event) {
        if (!event.target.closest("a")) {
            window.location.href = fila.dataset.url;
        }
    });
});
