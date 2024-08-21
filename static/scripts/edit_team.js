function loadList() {
    let trackList = document.body.dataset.tracks.split(' ');
    trackList.forEach((item) => {
        document.querySelector(`input[value="${item}"]`).checked = true;
        transportCheckbox(document.querySelector(`input[value="${item}"]`));
    }) 
}
window.onload = loadList