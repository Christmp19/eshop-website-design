
document.addEventListener("DOMContentLoaded", function () {
    // Obtenez l'URL actuelle de la page
    const currentUrl = window.location.pathname;

    // Sélectionnez tous les liens de navigation
    const links = document.querySelectorAll(".header .links .link");

    // Parcourez chaque lien pour vérifier l'URL
    links.forEach((link) => {
        const linkHref = link.getAttribute("href");

        // Comparez l'URL du lien avec l'URL actuelle
        if (linkHref === currentUrl) {
            // Ajoutez la classe 'active' au lien correspondant
            link.classList.add("active");
        }
    });
});
