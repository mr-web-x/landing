const cookiesOpenBtn = document.querySelector(".cookies-open-btn");

cookiesOpenBtn.addEventListener("click", () => {
  handleOpenPreferences();
});

function handleOpenPreferences() {
  if (window.cookieconsent) {
    window.cookieconsent.openPreferencesCenter(); // Открывает панель настроек cookies
  } else {
    console.error("CookieConsent script not loaded.");
  }
}
