let alertContent = document.querySelector(".top-alert");
let alertBtn = document.querySelector(".top-alert svg");

if (alertBtn) {
  alertBtn.addEventListener("click", (ev) => {
    alertContent.style.display = "none";
  });
}
