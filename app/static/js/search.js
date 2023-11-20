const searchInput = document.querySelector("#inputCity");
const searchOptions = document.querySelector(".options");

function getOptions(word) {
  const lang = "ru_RU"; // TODO изменить жесткое задание локализации
  const url = `/api/findLocation?lang=${lang}&query=${encodeURIComponent(
    word
  )}`;

  return fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Запрос завершился с ошибкой: ${response.status}`);
      }
      return response.json();
    })
    .catch((error) => {
      console.error(`Произошла ошибка при отправке запроса: ${error.message}`);
    });
}

function delay(fn, ms) {
  let timer = 0;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(fn.bind(this, ...args), ms || 0);
  };
}

function displayOptions() {
  if (this.value.replace(/^\s+|\s+$/g, "") == "") {
    searchOptions.innerHTML = "";
    return;
  }
  getOptions(this.value)
    .then((options) => {
      options = options.result;
      const html = options
        .map((city) => {
          return `<li class="placeOption"><span>${city.name}</span></li>`;
        })
        .slice(0, 10)
        .join("");

      searchOptions.innerHTML = this.value ? html : null;
      Array.from(document.querySelectorAll(".placeOption")).map((el) => {
        el.addEventListener("click", selectPlace);
      });
    })
    .catch((error) => {
      console.error(`Произошла ошибка: ${error.message}`);
    });
}

searchInput.addEventListener("keyup", delay(displayOptions, 500));

function selectPlace(event) {
  let element = event.target;
  window.location.href = `/forecast?name=${element.innerText}`;
}
