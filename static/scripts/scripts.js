function onLoad() {

}

function mainTableReload() {
    const Http = new XMLHttpRequest();
    const urlSearchParams = new URLSearchParams();
    urlSearchParams.set('search', ((document.getElementById("search") || {}).value) || "");
    if ((document.getElementById("dateFrom") || {}).value) {
        urlSearchParams.set('dateFrom', document.getElementById("dateFrom").value);
    }
    if ((document.getElementById("dateTo") || {}).value) {
        urlSearchParams.set('dateTo', document.getElementById("dateTo").value);
    }
    if ((document.getElementById("sort") || {}).value) {
        urlSearchParams.set('sort', document.getElementById("sort").value);
    }
    if ((document.getElementById("tag") || {}).value) {
        urlSearchParams.set('tag', document.getElementById("tag").value);
    }
    if ((document.getElementById("project") || {}).value) {
        urlSearchParams.set('project', document.getElementById("project").value);
    }
    Http.open("GET", location.href.split('?')[0] + '?' + urlSearchParams.toString());
    Http.send();
    Http.onreadystatechange = (e) => {
        document.getElementById("main-table").innerHTML = Http.responseText
    }
}

function mainTableSort(querystring) {
    const urlSearchParams = new URLSearchParams(querystring);
    document.getElementById("sort").value = urlSearchParams.get("sort");
    mainTableReload();
}

function mainTableTag(querystring) {
    const urlSearchParams = new URLSearchParams(querystring);
    document.getElementById("tag").value = urlSearchParams.get("tag");
    mainTableReload();
}

function deleteFile(csrftoken, lang, id) {
    const Http = new XMLHttpRequest();
    const url = "/" + lang + "/delete_file/" + id;
    Http.open("POST", url);
    Http.setRequestHeader("X-CSRFToken", csrftoken);
    Http.send();
}

function openTab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function setInputBackground() {
    this.style.backgroundColor = !!this.value ? "#FFFCC8" : "white";
}
