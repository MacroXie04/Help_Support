window.addEventListener('resize', adjustCardHeight);
window.addEventListener('load', adjustCardHeight);

function adjustCardHeight() {
    const card = document.querySelector('.card.card-style.mb-0.bg-transparent.shadow-0.bg-3.mx-0.rounded-0');
    const viewportHeight = window.innerHeight;
    card.style.height = `${viewportHeight}px`;
}