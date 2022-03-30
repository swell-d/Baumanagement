function mainTableReload(path, value) {
    if (value == "") {
        location.href = location.href;
        return;
    }
    const Http = new XMLHttpRequest();
    const urlSearchParams = new URLSearchParams(window.location.search);
    urlSearchParams.set('search', value);
    Http.open("GET", path + '?' + urlSearchParams.toString());
    Http.send();
    Http.onreadystatechange = (e) => {
        document.getElementById("main-table").innerHTML = Http.responseText
    }
}

function deleteFile(csrftoken, lang, id) {
    const Http = new XMLHttpRequest();
    const url = "/" + lang + "/delete_file/" + id;
    Http.open("POST", url);
    Http.setRequestHeader("X-CSRFToken", csrftoken);
    Http.send();
}