function toggleMenu() {
  // toggle navigation links when user clicks on bar icon
  var elm = document.getElementById("myLinks");
  if (elm.style.display === "block") {
    elm.style.display = "none";
  } else {
    elm.style.display = "block";
  }
}
