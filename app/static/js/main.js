const MOBILE_MAX_WIDTH = 1000;

// Меню 1-27стр
let buttonMenu = document.querySelector('#menuButton');
let menu = document.querySelector('#menu');

// Показ/Сокрытие меню
const toggleMenu = () => {
  menu.classList.toggle('show');
}

// Открытие меню на кнопку
buttonMenu.addEventListener('click', e => {
  e.stopPropagation();

  toggleMenu();
});

// Проверяем куда нажал пользователь
document.addEventListener('click', e => {
  let target = e.target;
  let its_menu = target == menu || menu.contains(target);
  let its_buttonMenu = target == buttonMenu;
  let menu_is_active = menu.classList.contains('show');
  
  if (!its_menu && !its_buttonMenu && menu_is_active) {
    toggleMenu();
  }
})


// Карточки с погодой
let aside = document.querySelectorAll('aside');


function setMoreDownListener(moreDownSelector, cardSelector, displayMode, maxCount) {
    // Просматриваем события связанные с кнопками moreDown
    let moreDown = document.querySelectorAll(moreDownSelector);
    for (let i = 0; i < moreDown.length; i++) {
        let cards = moreDown[i].parentElement.querySelectorAll(cardSelector);
        if (cards.length > maxCount) {
            for (let j = maxCount; j < cards.length; j++) {
                cards[j].style.display = 'none';
            }
        }
        moreDown[i].isOpened = false;
        moreDown[i].onclick = function() {
            let cards = moreDown[i].parentElement.querySelectorAll(cardSelector);
            let j;
            if (!moreDown[i].isOpened) {
                j = 0;
                style = displayMode;
                transform = "transform: rotate(180deg);";
            } else {
                j = maxCount;
                style = "none";
                transform = "transform: none;";
            }
            for (;j < cards.length; j++) {
                cards[j].style.display = style;
            }
            moreDown[i].isOpened = !moreDown[i].isOpened;
            moreDown[i].style = transform
        }
    }
}


setMoreDownListener(".moreDown", ".card", "inline-block", 3);

const windowInnerWidth = document.documentElement.clientWidth;

if (windowInnerWidth < MOBILE_MAX_WIDTH)
{
    // Просматриваем переход на мобильную версию
    // Удаляем лишние карточки из блоков
    for (let i = 0; i < aside.length; i++)
    {
        const cards = document.querySelectorAll('.card');
        for (let i = 0; i < cards.length; i++)
        {
            if (i != 0 && i != 3 && i != 6)
                cards[i].style.display = "none";
        }
    }
} 
