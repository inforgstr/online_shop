const dropDown = document.querySelector("li.nav_dropdown");

const dropContent = document.querySelector(".dropdown-main");
const underDrop = document.querySelector(".main_content");

dropDown.addEventListener("mouseover", () => {
  dropContent.style.display = "block";
});

dropDown.addEventListener("mouseout", () => {
  dropContent.style.display = "none";
});
