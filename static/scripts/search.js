function mainTableReload(path, value) {
    const Http = new XMLHttpRequest();
    const url = path + "?search=" + value;
    Http.open("GET", url);
    Http.send();
    Http.onreadystatechange = (e) => {
        document.getElementById("main-table").innerHTML = Http.responseText
    }
}