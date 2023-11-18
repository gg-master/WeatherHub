const searchInput = document.querySelector('#inputCity');
const searchOptions = document.querySelector('.options');

function getOptions(word) {
    const lang = "ru_RU"; // TODO изменить жесткое задание локализации
    const url = `/api/suggest-geo?lang=${lang}&part=${encodeURIComponent(word)}`;

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Запрос завершился с ошибкой: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error(`Произошла ошибка при отправке запроса: ${error.message}`);
        });
}

function displayOptions() {
    getOptions(this.value)
        .then(options => {
            options = options.options;
            const html = options.map(city => {

            //     // Проверяем наличие выделенных фрагментов (hl) и создаем соответствующий HTML
            //     const highlightedName = city.hl
            //         ? city.hl.reduce((acc, hl) => {
            //             const start = hl[0];
            //             const end = hl[1];
            //             return acc + city.name.substring(start, end);
            //         }, '')
            //         : city.name;

            //     // Заменяем подстроку, соответствующую значению, на HTML с выделением
            //     const regex = new RegExp(this.value, 'gi');
            //     const cityName = highlightedName.replace(
            //         regex,
            //         `<span class="hl">${this.value}</span>`
            //     );

                return `<li><span>${city.name}</span></li>`;
            })
                .slice(0, 10)
                .join('');

            searchOptions.innerHTML = this.value ? html : null;
        })
        .catch(error => {
            console.error(`Произошла ошибка: ${error.message}`);
        });
}

searchInput.addEventListener('change', displayOptions);
searchInput.addEventListener('keyup', displayOptions);