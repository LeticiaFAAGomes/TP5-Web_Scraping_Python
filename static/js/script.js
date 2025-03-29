function navegar(id) {
  scrollTo({ top: document.getElementById(id).offsetTop - 110 });
  abrirMenu();
}

function scrollTopo() {
  scrollTo({ top: 0 });
}

function abrirMenu() {
  document.querySelector("ul").classList.toggle("active");
}
