function setValue(selector, value) {
    let elem = document.querySelector(selector);
    if (value === "") {
        elem.style.display = "none";
    } else {
        elem.style.display = "inline";
    }
    elem.innerHTML = value
}

async function getInfo(id) {
    let url = `https://raw.githubusercontent.com/maypink/history_project_Petr1/main/data/processed/info${parseInt(id / 1000) + 1}/${id}.json`
    let entity = await (await fetch(url)).json();
    let name = entity.name
    let location = entity.location
    let type = entity.type
    let status = entity.status
    let description = entity.description
    let imageURLs = entity.imageURLs

    let images = document.querySelector('.gallery');
    imageURLs.reverse().forEach(url => {
        let img = document.createElement("img");
        img.setAttribute("src", url);
        img.setAttribute("class", "image_inserted");
        img.setAttribute("alt", "");
        images.appendChild(img);
    });

    setValue('.name', name);
    setValue('.location', location);
    setValue('.type_of_monument', type);
    setValue('.status', status);
    setValue('.description', description);
}

let popupBg = document.querySelector('.popup__bg');
let popup = document.querySelector('.popup');
let open = document.querySelector('.open');

open.addEventListener('click', (e) => {
    e.preventDefault();

    getInfo(0)

    popupBg.classList.add('active');
    popup.classList.add('active');
});

document.addEventListener('click', (e) => {
    if (e.target === popupBg) {
        popupBg.classList.remove('active');
        popup.classList.remove('active');
    }
});