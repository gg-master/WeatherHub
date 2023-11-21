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

document.querySelector(".addCurrent").addEventListener("click", () => {
  let favorites = [];
  if (localStorage.getItem("favorites") != undefined) {
    favorites = JSON.parse(localStorage.getItem("favorites"));
  }
  let city = document.querySelector(".city").innerText;
  if (favorites.indexOf(city) < 0) {
    favorites.push(city);
    localStorage.setItem("favorites", JSON.stringify(favorites));
  }
  initFavorites();
});

function initFavorites() {
  document.querySelector(".favorites").innerHTML = "";
  if (localStorage.getItem("favorites") != undefined) {
    let favorites = JSON.parse(localStorage.getItem("favorites"));
    for (let favor of favorites) {
      let element = document.createElement("li");
      element.setAttribute("class", "favor");
      element.addEventListener("click", (e) => {
        let text = e.currentTarget.querySelector("p").innerText;
        window.location.href = `forecast?name=${text}`;
      });
      document.querySelector(".favorites").appendChild(element);
      element.innerHTML = `<p>${favor}</p><img class="removeFavor" src="img/minus.svg" alt="">`;
      element.querySelector(".removeFavor").addEventListener("click", (e) => {
        let favorites = [];
        if (localStorage.getItem("favorites") != undefined) {
          favorites = JSON.parse(localStorage.getItem("favorites"));
        }
        const index = favorites.indexOf(e.target.parentElement.innerText);
        if (index > -1) {
          favorites.splice(index, 1);
        }
        e.target.parentElement.style = "display: none;";
        localStorage.setItem("favorites", JSON.stringify(favorites));
      });
    }
  }
}

initFavorites();
