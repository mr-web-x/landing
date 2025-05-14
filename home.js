let modalGame = document.querySelector(".modal-game");
let modalGameClose = document.querySelector(".modal-game-close");

setTimeout(() => {
  modalGame.classList.add("active");
}, 5000);

modalGameClose.addEventListener("click", () => {
  console.log("close");
  modalGame.classList.remove("active");
});
