document.addEventListener("DOMContentLoaded", () => {
    const cartCountSpan = document.getElementById("cart-count");
    const carritoIcono = document.getElementById("carrito-icono");

    // Almacenar productos en un array simulado (puedes sustituirlo por lógica del backend)
    let carrito = [];

    // Manejar la lógica de agregar al carrito
    document.querySelectorAll("#boton_carrito").forEach((boton) => {
        boton.addEventListener("click", (event) => {
            event.preventDefault(); // Evitar comportamiento por defecto del formulario

            // Obtener los datos del producto
            const card = boton.closest(".card");
            const producto = {
                id: card.querySelector("#id").value,
                title: card.querySelector("#title").value,
                price: card.querySelector("#price").value,
                image: card.querySelector("#image").value,
                count: card.querySelector("#count").value
            };

            // Agregar al carrito
            carrito.push(producto);
            console.log(producto);


            // Actualizar el contador del carrito
            cartCountSpan.textContent = carrito.length;
            cartCountSpan.style.display = "block";

        });
    });

    // Redirigir al carrito al hacer clic en el ícono
    carritoIcono.addEventListener("click", () => {
        if (carrito.length === 0) {
            alert("El carrito está vacío.");
        } else {
            // Simular redirección al carrito (puedes reemplazar con tu lógica)
            console.log("Productos en el carrito:", carrito);
            //alert("Redirigiendo al carrito...");
            window.location.href = "/carrito"; // Asegúrate de tener esta ruta configurada en Flask
        }
    });
});
