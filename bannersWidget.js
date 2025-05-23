import { getCreditConditions } from "./service.js";

getCreditConditions().then((companyList) => {
  renderBanners(companyList.conditions);
});

function renderBanners(companies) {
  let headings = document.querySelectorAll(".article-content h2");
  let count = headings.length;

  if (count < 2) return; // ничего не делать, если меньше 3 заголовков

  const randomNumbers = getUniqueRandomNumbers(0, companies.length - 1, 2);

  // Функция для создания динамического баннера
  function createBanner(company) {
    console.log("company", company);
    const bannerDiv = document.createElement("div");
    bannerDiv.className = "banner-widget";
    bannerDiv.innerHTML = `
                <a class="banner-widget__card" target="_blank" href="${
                  company.link
                }">
					<div class="banner-widget__card-item banner-widget__card-center">
						<img src="/assets/companies/${company.logo}" alt="${
      company.companyName
    }" width="217px" height="73px">
					</div>
					<div class="banner-widget__card-item">
						<span>Úroková sadzba</span>
						<figure>od <span>${((company.yearPercent * 100) / 365).toFixed(
              2
            )}</span>%</figure>
					</div>
					<div class="banner-widget__card-item">
						<span>Lehota</span>
						<figure>do <span>${company.term.to}</span> dní</figure>
					</div>
					<div class="banner-widget__card-item">
						<span>Summ</span>
						<figure>do <span>${company.amount.to}</span> €</figure>
					</div>
					<div class="banner-widget__card-item banner-widget__card-center">
						<span style="background: ${company.color}" class="btn">Viac &#8594;</span>
					</div>
				</a>  <p class="banner-policy">Informácie majú len informatívny charakter. FastCredit.sk nie je poskytovateľom úverov</p>`;
    return bannerDiv;
  }

  // Функция для создания статичной рекламы
  function createStaticAd() {
    const staticAdDiv = document.createElement("div");
    staticAdDiv.className = "static-ad-widget";
    staticAdDiv.innerHTML = `
      <a href="/blog/rychla-pozicka-do-500-eur.html">
        style="
          border: 1px solid #ddd;
          padding: 15px;
          margin: 30px 0;
          border-radius: 8px;
          background-color: white;
          dispay: block;
          text-decoration: none;
        "
      >
        📌<strong>Odporúčame na prečítanie:</strong><br />
        <p
          style="font-weight: bold; color: #007b7f; margin-top: 8px"
        >
          Rýchla pôžička do 500 eur – ako funguje a kto ju môže získať?
        </p>
        <p style="margin-top: 5px; font-size: 14px; color: #555">
          Zistite, kto má nárok a aké sú výhody tejto formy rýchleho
          financovania.
        </p>
      </a>`;
    return staticAdDiv;
  }

  if (count === 1) {
    headings[0].before(createBanner(companies[randomNumbers[0]]));
  }

  // Если 2 заголовка — добавляем первый баннер, статичную рекламу, второй баннер
  if (count === 2) {
    headings[0].before(createBanner(companies[randomNumbers[0]]));
    headings[0].before(createStaticAd());
    headings[1].before(createBanner(companies[randomNumbers[1]]));
  }

  if (count === 3) {
    headings[0].before(createBanner(companies[randomNumbers[0]]));
    headings[1].before(createStaticAd());
    headings[2].before(createBanner(companies[randomNumbers[1]]));
  }

  // Если больше 3 заголовков — делим на 4 части и вставляем баннеры с статичной рекламой между ними
  if (count > 3) {
    let part = Math.floor(count / 4);

    // Индексы после которых вставлять баннеры
    let insertAfter1 = part * 2 - 1;
    let insertMiddle = part * 3 - 1;
    let insertAfter2 = part * 4 - 1;

    if (headings[insertAfter1]) {
      headings[insertAfter1].before(createBanner(companies[randomNumbers[0]]));
      headings[insertMiddle].before(createStaticAd());
    }
    if (headings[insertAfter2]) {
      headings[insertAfter2].before(createBanner(companies[randomNumbers[1]]));
    }
  }
}

function getUniqueRandomNumbers(min, max, count) {
  if (count > max - min + 1) {
    throw new Error(
      "Запрашиваемое количество превышает количество уникальных значений в диапазоне"
    );
  }

  const numbers = [];
  const used = new Set();

  while (numbers.length < count) {
    const rand = Math.floor(Math.random() * (max - min + 1)) + min;
    if (!used.has(rand)) {
      used.add(rand);
      numbers.push(rand);
    }
  }

  return numbers;
}

function injectBannerStyles() {
  if (document.getElementById("banner-widget-styles")) return; // Не добавлять повторно

  const style = document.createElement("style");
  style.id = "banner-widget-styles";
  style.innerHTML = `
.banner-widget__card-item span {
  color: #898989;
  font-size: 14px;
}

.banner-widget__card-item figure {
  color: black;
  font-size: 16px;
  margin-top: 10px;
}

.banner-widget__card-item figure span {
  color: black;
  font-size: 20px;
} 
  
.banner-widget__card-item {
max-height: 73px;
}

.banner-widget__card-item .btn{
    border-radius: 10px;
}

.banner-widget__card-item img {
      object-fit: contain;
      background: white;
}

.banner-widget{
  margin: 30px 0;
}

.static-ad-widget {
  margin: 30px 0;
}

.banner-policy{
    font-size: 8px;
    color: gray;
    text-align:center;
}

.banner-widget__card {

  border-radius: 0px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  box-shadow: 1px 1px 4px gray;
  background: white;
  padding: 5px 10px; 
}

.companies-filter-reset {
  background: none;
  color: black;
  text-decoration: underline;
  display: none;
  border: none;
  cursor: pointer;
  height: 44px;
}

@media all and (max-width: 800px) {
  .banner-widget__card {
    flex-direction: column;
    max-width: 450px;
    width: 100%;
    margin: 0 auto;
    align-items: flex-start;
    justify-content: flex-start;
  }
  .banner-widget__card-item {
    display: flex;
    align-items: center;
  justify-content: space-between;
    gap: 10px;
    width: 100%;
  }
        .banner-widget__card-center{
        justify-content: center; 
    }

  .banner-widget__card-info {
    width: 100%;
  }

  .banner-widget__card-info span {
    display: block;
    width: 50%;
    font-size: 16px;
  }

  .banner-widget__card-item figure {
    margin-top: 0;
    text-align: right;
    width: calc(50% - 10px);
  }
  .banner-widget__card-item figure span {
    display: inline;
  }
  .banner-widget__card-item figure span {
    font-size: 18px;
  }
  .banner-widget__card-logo {
    margin-bottom: 20px;
  }
  .banner-widget__card-link {
    margin-top: 20px;
  }
}
}
  `;
  document.head.appendChild(style);
}

injectBannerStyles();
