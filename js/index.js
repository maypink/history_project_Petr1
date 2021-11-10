let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 59.93863, lng: 30.31413 },
    zoom: 8,
  });

  getMarkers()
}

async function getMarkers() {
  let DB = await(await fetch('temp.json')).json();

  DB.forEach(elem => {
    const position = { lat: elem.lat, lng: elem.lng };

    const marker = new google.maps.Marker({
      position,
      map,
      title: `${elem.id}`,
      label: `${elem.id}`,
      id_for_json: `${elem.id}`,
      optimized: false,
    })

    marker.addListener("click", () => {

      // DOWNLOAD JSON FILE WITH NAME ({id}.json)
      // AND UPDATE VIEW

      console.log(marker.id_for_json)
      popupBg.classList.add('active');
      popup.classList.add('active');
    });
  });

  console.log(DB);
  console.log(DB[0].lat)
}