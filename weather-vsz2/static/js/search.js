function getWeather() {
    var locationInput = document.querySelector(".locationInput").value;
    if (locationInput === "" || locationInput.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/weather/${locationInput.replace("/", ",").toLowerCase()}`;
    }
}