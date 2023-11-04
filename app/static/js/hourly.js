// Отображение лент с погодой
// Проходимся по каждому блоку и прослушиваем нажатие на кнопку moreDownLine
let moreDownLine = document.querySelectorAll('.moreDownLine');

setMoreDownListener(".moreDownLine", "article", "block", 2);

const windowInnerWidthLines = document.documentElement.clientWidth;


// Реализация слайдера
slider = document.querySelectorAll(`.slider`);

let sliderItems = [];
for (let i = 0; i < slider.length; i++)
{
    sliderItems[i] = Array.from(slider[i].children);
}

const btnNext = document.querySelectorAll('.arrowRight');
const btnPrev = document.querySelectorAll('.arrowLeft');

function displayWindowSize() {
    for (let i = 0; i < slider.length; i++)
    {
        sliderItems[i].forEach(function (slide, index) {
            const windowInnerWidth = document.documentElement.clientWidth;
            let t = 19;
            if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 4;
            // Скрываем ненужные слайды
            if (index >= t) {
                slide.classList.add('hide');
            } else {
                slide.classList.remove('hide');
            }

            //Добавляем индексы
            slide.dataset.index = index;

            // Добавляем дата атрибут active для первого / активного слайда
            sliderItems[i][0].setAttribute('data-active', '');
        });
    }
}


window.addEventListener("resize", displayWindowSize);

displayWindowSize();

for (let i = 0; i < btnNext.length; i++)
{
    btnNext[i].onclick = function () {
        const currentSlide = slider[i].querySelector('[data-active]');
        const currentSlideIndex = +currentSlide.dataset.index;
        const windowInnerWidth = document.documentElement.clientWidth;
        let t = 19;
        if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 4;
        // Показываем след слайд
        let nextSlideIndex;
        if (currentSlideIndex + t < sliderItems[i].length) {
            nextSlideIndex = currentSlideIndex + t;
            let nextActiveIndex = currentSlideIndex + 1;
            // Скрываем текущий слайд
            currentSlide.classList.add('hide');
            currentSlide.removeAttribute('data-active');
            const nextSlide = slider[i].querySelector(`[data-index="${nextSlideIndex}"`);
            nextSlide.classList.remove('hide');
            const nextActive = slider[i].querySelector(`[data-index="${nextActiveIndex}"]`);
            nextActive.setAttribute('data-active', '');
        }
    }
}

for (let i = 0; i < btnPrev.length; i++)
{
    btnPrev[i].onclick = function() {
        const currentSlide = slider[i].querySelector('[data-active]');
        const currentSlideIndex = +currentSlide.dataset.index;
        const windowInnerWidth = document.documentElement.clientWidth;
        let t = 18;
        if (windowInnerWidth <= MOBILE_MAX_WIDTH) t = 3; 
        // Показываем след слайд
        let nextSlideIndex;
        if (currentSlideIndex - 1 >= 0) {
            nextSlideIndex = currentSlideIndex - 1;
            // Скрываем текущий слайд
            const lastSlideIndex = currentSlideIndex + t;
            const lastSlide = slider[i].querySelector(`[data-index="${lastSlideIndex}"`);
            if (lastSlide) lastSlide.classList.add('hide');
            currentSlide.removeAttribute('data-active');
            const nextSlide = slider[i].querySelector(`[data-index="${nextSlideIndex}"`);
            if (nextSlide) nextSlide.classList.remove('hide');
            nextSlide.setAttribute('data-active', '');
        }
    }
}