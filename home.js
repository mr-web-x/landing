document.addEventListener("DOMContentLoaded", function () {
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

  const dictionarySection = document.querySelector(".dictionary-links");
  const allItems = dictionarySection.querySelectorAll("li");
  const itemsPerLoad = 10;
  let currentlyShown = 0;

  // Создаем контейнер с сеткой
  const gridContainer = document.createElement("div");
  gridContainer.className = "dictionary-grid";

  // Перемещаем ul в grid контейнер
  const ul = dictionarySection.querySelector("ul");
  gridContainer.appendChild(ul);

  // Вставляем grid контейнер после заголовка
  const h2 = dictionarySection.querySelector("h2");
  h2.insertAdjacentElement("afterend", gridContainer);

  // Создаем кнопку "Показать больше"
  const showMoreBtn = document.createElement("button");
  showMoreBtn.className = "show-more-btn";
  showMoreBtn.textContent = "Ukáž viac";
  dictionarySection.appendChild(showMoreBtn);

  // Функция показа элементов
  function showItems(count) {
    for (
      let i = currentlyShown;
      i < currentlyShown + count && i < allItems.length;
      i++
    ) {
      allItems[i].classList.remove("hidden");
    }
    currentlyShown += count;

    // Скрываем кнопку если показаны все элементы
    if (currentlyShown >= allItems.length) {
      showMoreBtn.classList.add("hidden");
    }
  }

  // Функция скрытия всех элементов
  function hideAllItems() {
    allItems.forEach((item) => {
      item.classList.add("hidden");
    });
    currentlyShown = 0;
  }

  // Изначально скрываем все элементы
  hideAllItems();

  // Показываем первые 20 элементов
  showItems(itemsPerLoad);

  // Обработчик клика на кнопку
  showMoreBtn.addEventListener("click", function () {
    // Можно выбрать один из вариантов:

    // Вариант 1: Подгружать по +20 слов
    showItems(itemsPerLoad);

    // Вариант 2: Показать все оставшиеся слова сразу
    // showItems(allItems.length - currentlyShown);
  });

  // Альтернативная функция для показа всех слов сразу
  function showAllItems() {
    allItems.forEach((item) => {
      item.classList.remove("hidden");
    });
    showMoreBtn.classList.add("hidden");
    currentlyShown = allItems.length;
  }

  // Если хотите использовать вариант "показать все сразу",
  // замените обработчик события на:
  /*
  showMoreBtn.addEventListener('click', function() {
    showAllItems();
  });
  */
});
