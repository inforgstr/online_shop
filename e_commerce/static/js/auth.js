const pswInput = document.querySelector("p#psw input");
let opened = document.getElementById("svg1");
let closed = document.getElementById("svg2");

closed.addEventListener("click", (ev) => {
  closed.style.display = "none";
  opened.style.display = "block";
  pswInput.type = "text";
});

opened.addEventListener("click", (ev) => {
  opened.style.display = "none";
  closed.style.display = "block";
  pswInput.type = "password";
});
