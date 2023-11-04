const api = `https://raw.githubusercontent.com/pensnarik/russian-cities/master/russian-cities.json`

const cities = [];

fetch(api).then(res => res.json()).then(data => {
    data.forEach(e => {
        cities.push(e.name);
    })
})

const searchInput = document.querySelector('#inputCity');
const searchOptions = document.querySelector('.options');

function getOptions(word, cities) {

    return cities.filter(s => {
        // Определить совпадаетли то что мы вбили в input 
        // названием города внутри массива

        const regex = new RegExp(word, 'gi');

        return s.match(regex);
    })
}

function displayOptions() {

    const options = getOptions(this.value, cities);

    const html = options
        .map(city => {

            const regex = new RegExp(this.value, 'gi');
            const cityName = city.replace(regex, 
                    `<span class="hl">${this.value}</span>`
                );

            return `<li><span>${cityName}</span></li>`;
        })
        .slice(0, 10)
        .join('');

    searchOptions.innerHTML = this.value ? html : null;
}

searchInput.addEventListener('change', displayOptions);
searchInput.addEventListener('keyup', displayOptions);