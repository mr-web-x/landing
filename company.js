import { getCreditConditions } from "./service.js";

let companiesListHtlm = document.querySelector(".companies__list");
let companiesFilterForm = document.querySelector(".companies form");
let companiesSelectSumm = document.getElementById("slct-eur");
let companiesSelectDays = document.getElementById("slct-days");
let companiesArray = [];
let companiesFilterReset = document.querySelector(".companies-filter-reset");

getCreditConditions().then((companyList) => {
  console.log(companyList);
  companiesArray = companyList.conditions;
  renderCompanies(companyList.conditions);
});

companiesFilterForm.addEventListener("submit", (event) => {
  event.preventDefault();

  let fSumm = companiesSelectSumm.value;
  let fDays = companiesSelectDays.value;

  if (!fSumm || !fDays) return;

  let filteredCompanies = companiesArray.filter((company) => {
    let isSummValid = false;
    let isDaysValid = false;

    const maxAmount = company.amount?.to || 0;
    const maxDays = company.term?.to || 0;

    // Фильтрация по сумме займа
    if (fSumm === "do500" && maxAmount <= 500) isSummValid = true;
    if (fSumm === "od500do5000" && maxAmount > 500 && maxAmount <= 5000)
      isSummValid = true;
    if (fSumm === "od5000" && maxAmount > 5000) isSummValid = true;

    // Фильтрация по сроку займа
    if (fDays === "do1month" && maxDays <= 30) isDaysValid = true;
    if (fDays === "od1monthdo12month" && maxDays > 30 && maxDays <= 365)
      isDaysValid = true;
    if (fDays === "od12month" && maxDays > 365) isDaysValid = true;

    return isSummValid && isDaysValid;
  });

  companiesFilterReset.style.display = "block";
  renderCompanies(filteredCompanies);
});

// companiesFilterForm.addEventListener("submit", (event) => {
//   event.preventDefault();

//   let fSumm = companiesSelectSumm.value;
//   let fDays = companiesSelectDays.value;

//   if (!fSumm || !fDays) return;

//   let filteredCompanies = companiesArray.filter((company) => {
//     let isSummValid = false;
//     let isDaysValid = false;

//     // Фильтрация по сумме займа
//     if (fSumm === "do500" && company.summDo <= 500) isSummValid = true;
//     if (
//       fSumm === "od500do5000" &&
//       company.summDo > 500 &&
//       company.summDo <= 5000
//     )
//       isSummValid = true;
//     if (fSumm === "od5000" && company.summDo > 5000) isSummValid = true;

//     // Фильтрация по сроку займа
//     if (fDays === "do1month" && company.daysDo <= 30) isDaysValid = true;
//     if (
//       fDays === "od1monthdo12month" &&
//       company.daysDo > 30 &&
//       company.daysDo <= 365
//     )
//       isDaysValid = true;
//     if (fDays === "od12month" && company.daysDo > 365) isDaysValid = true;

//     return isSummValid && isDaysValid;
//   });

//   companiesFilterReset.style.display = "block";

//   renderCompanies(filteredCompanies);
// });

companiesFilterReset.addEventListener("click", () => {
  renderCompanies(companiesArray);
  companiesSelectSumm.value = "";
  companiesSelectDays.value = "";

  companiesFilterReset.style.display = "none";
});

function renderCompanies(companyList) {
  companiesListHtlm.innerHTML = "";

  companyList
    .sort((a, b) => a.priority - b.priority)
    .forEach((element) => {
      companiesListHtlm.innerHTML += `
                <div class="companies__card">
					<div class="companies__card-item companies__card-logo">
						<img src="/assets/companies/${element.logo}" alt="${
        element.companyName
      }" width="217px" height="73px">
					</div>
					<div class="companies__card-item companies__card-info">
						<span>Úroková sadzba</span>
						<figure>od <span>${(
              (element.yearPercent * 100) /
              365
            ).toFixed()}</span>%</figure>
					</div>
					<div class="companies__card-item companies__card-info">
						<span>Lehota</span>
						<figure>do <span>${element.term.to}</span> dní</figure>
					</div>
					<div class="companies__card-item companies__card-info">
						<span>Summ</span>
						<figure>do <span>${element.amount.to}</span> €</figure>
					</div>
					<div class="companies__card-item companies__card-link">
						<a target="_blank" href="${element.link}" class="btn">Viac &#8594;</a>
					</div>
				</div>
        `;
    });

  // <div class="companies__card-item companies__card-info">
  // 	<span>Vek</span>
  // 	<figure>od <span>${element.years}</span> rokov</figure>
  // </div>

  if (companyList.length < 1) {
    companiesListHtlm.innerHTML = "<p>Netu</p>";
  }
}
