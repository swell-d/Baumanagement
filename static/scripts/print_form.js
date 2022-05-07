function edit() {
    document.getElementById("save").classList.remove("d-none");
    document.getElementById("edit").classList.add("d-none");
    document.getElementById("print").classList.add("d-none");
    $('#summernote').summernote();
};

function save() {
    $('#summernote').summernote('code');
    $('#summernote').summernote('destroy');
    document.getElementById("save").classList.add("d-none");
    document.getElementById("edit").classList.remove("d-none");
    document.getElementById("print").classList.remove("d-none");
};