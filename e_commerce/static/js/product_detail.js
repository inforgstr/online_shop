const selections = document.querySelectorAll(".img-sections img");
const mainIMG = document.querySelector(".img-main img");

selections.forEach((img) => {
  img.addEventListener("mouseover", () => {
    mainIMG.setAttribute("src", img.getAttribute("src"));
    img.parentElement.classList.add("selected");
  });
  img.addEventListener("mouseout", () => {
    img.parentElement.classList.remove("selected");
  });
});

let btnMinus = document.querySelector(".quantity #minus");
let btnPlus = document.querySelector(".quantity #plus");

let numberInput = document.querySelector(".quantity input");

btnMinus.addEventListener("click", () => {
  if (parseInt(numberInput.value) > 1) {
    numberInput.value = parseInt(numberInput.value) - 1;
  }
});

btnPlus.addEventListener("click", () => {
  if (parseInt(numberInput.value) < 99) {
    numberInput.value = parseInt(numberInput.value) + 1;
  }
});
