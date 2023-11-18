const searchInput = document.querySelector('#inputCity');
const searchOptions = document.querySelector('.options');

function getOptions(word) {
    const lang = "ru_RU"; // TODO изменить жесткое задание локализации
    const url = `/api/findLocation?lang=${lang}&query=${encodeURIComponent(word)}`;

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
            options = options.result;
            const html = options.map(city => {
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