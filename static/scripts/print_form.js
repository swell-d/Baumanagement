function edit(lang) {
    document.getElementById("cancel").classList.remove("d-none");
    document.getElementById("save").classList.remove("d-none");
    document.getElementById("edit").classList.add("d-none");
    document.getElementById("print").classList.add("d-none");
    $('#summernote').summernote({
        width: 814,
        height: 1143,
        lang: lang
    });
};

function save() {
    $('#summernote').summernote('code');
    $('#summernote').summernote('destroy');
    document.getElementById("cancel").classList.add("d-none");
    document.getElementById("save").classList.add("d-none");
    document.getElementById("edit").classList.remove("d-none");
    document.getElementById("print").classList.remove("d-none");
};