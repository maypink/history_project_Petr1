let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 59.93863, lng: 30.31413 },
    zoom: 8,
  });

  getMarkers()
}

async function getMarkers() {
  let url = 'https://raw.githubusercontent.com/maypink/history_project_Petr1/main/data/processed/coords/coords.json'
  let DB = await(await fetch(url)).json();
  let markers = []

  DB.forEach(elem => {
    const position = { lat: elem.coords.lat, lng: elem.coords.lng };

    const marker = new google.maps.Marker({
      position,
      map,
      title: `${elem.id}`,
      label: `${elem.id}`,
      id_for_json: `${elem.id}`,
      optimized: true,
    })

    marker.addListener("click", () => {

      getInfo(marker.id_for_json);

      console.log(marker.id_for_json)
      popupBg.classList.add('active');
      popup.classList.add('active');
    });

    markers.push(marker);
  });

  new markerClusterer.MarkerClusterer({ markers, map });
}