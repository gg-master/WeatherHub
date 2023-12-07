// Отображение лент с погодой
// Проходимся по каждому блоку и прослушиваем нажатие на кнопку moreDownLine
let moreDownLine = document.querySelectorAll(".moreDownLine");

setMoreDownListener(".moreDownLine", "article", "block", 2);

const windowInnerWidthLines = document.documentElement.clientWidth;

// Реализация слайдера
slider = document.querySelectorAll(`.slider`);

let sliderItems = [];
for (let i = 0; i < slider.length; i++) {
  sliderItems[i] = Array.from(slider[i].children);
}

const btnNext = document.querySelectorAll(".arrowRight");
const btnPrev = document.querySelectorAll(".arrowLeft");

function displayWindowSize() {
  for (let i = 0; i < slider.length; i++) {
    sliderItems[i].forEach(function (slide, index) {
      const windowInnerWidth = document.documentElement.clientWidth;
      let t = 16;
      if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 3;
      // Скрываем ненужные слайды
      if (index >= t) {
        slide.classList.add("hide");
      } else {
        slide.classList.remove("hide");
      }

      //Добавляем индексы
      slide.dataset.index = index;

      // TODO зачем вообще data-active???
      // Добавляем дата атрибут active для первого / активного слайда
      sliderItems[i][0].setAttribute("data-active", "");
    });
  }
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();

let hourViews = document.querySelectorAll(`.hour-view`);

for (let i = 0; i < btnNext.length; i++) {
  btnNext[i].onclick = function () {
    for (let elem of hourViews[i].querySelectorAll(".slider")) {
      let sliderArray = Array.from(elem.children);
      const currentSlide = elem.querySelector("[data-active]");
      const currentSlideIndex = +currentSlide.dataset.index;
      const windowInnerWidth = document.documentElement.clientWidth;
      // TODO отрефакторить захардкоренные цифры
      let t = 16;
      if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 3;
      // Показываем след слайд
      let nextSlideIndex;
      if (currentSlideIndex + t < sliderArray.length) {
        nextSlideIndex = currentSlideIndex + t;
        let nextActiveIndex = currentSlideIndex + 1;

        // Скрываем текущий слайд
        currentSlide.classList.add("hide");
        currentSlide.removeAttribute("data-active");

        const nextSlide = elem.querySelector(`[data-index="${nextSlideIndex}"`);
        nextSlide.classList.remove("hide");

        const nextActive = elem.querySelector(
          `[data-index="${nextActiveIndex}"]`
        );
        nextActive.setAttribute("data-active", "");
      }
    }
  };
}

for (let i = 0; i < btnPrev.length; i++) {
  btnPrev[i].onclick = function () {
    for (let elem of hourViews[i].querySelectorAll(".slider")) {
      const currentSlide = elem.querySelector("[data-active]");
      const currentSlideIndex = +currentSlide.dataset.index;
      const windowInnerWidth = document.documentElement.clientWidth;
      // TODO отрефакторить весь этот пипец
      let t = 16;
      if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 3;
      // Показываем след слайд
      let nextSlideIndex;
      if (currentSlideIndex - 1 >= 0) {
        nextSlideIndex = currentSlideIndex - 1;

        // Скрываем текущий слайд
        let lastSlideIndex = currentSlideIndex + t - 1;
        let lastSlide = elem.querySelector(`[data-index="${lastSlideIndex}"`);
        lastSlide.classList.add("hide");
        lastSlide.removeAttribute("data-active");

        let nextSlide = elem.querySelector(`[data-index="${nextSlideIndex}"`);

        nextSlide.classList.remove("hide");
        nextSlide.setAttribute("data-active", "");
      }
    }
  };
}
