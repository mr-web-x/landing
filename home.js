let modalGame = document.querySelector(".modal-game");
let modalGameClose = document.querySelector(".modal-game-close");
let score = localStorage.getItem("score");

if (!score) {
  setTimeout(() => {
    modalGame.classList.add("active");
  }, 5000);
}

modalGameClose.addEventListener("click", () => {
  console.log("close");
  modalGame.classList.remove("active");
});
