function mainTableReload(path, value) {
    const Http = new XMLHttpRequest();
    const url = path + "?search=" + value;
    Http.open("GET", url);
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