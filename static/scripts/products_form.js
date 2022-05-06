checkVisibility();

function addProduct() {
    const count = new Number(document.getElementById("id_products-TOTAL_FORMS").value);
    const copyRow = document.getElementById("products_form-empty_row").cloneNode(true);
    copyRow.setAttribute('class', 'table-success');
    copyRow.setAttribute('id', 'row-'+ count);
    const regexp = new RegExp('__prefix__', 'g');
    copyRow.innerHTML = copyRow.innerHTML.replace(regexp, count);
    document.getElementById("products_form-tbody").append(copyRow);
    document.getElementById("id_products-TOTAL_FORMS").value = count + 1;
    checkVisibility();
}

function checkVisibility() {
    const count = new Number(document.getElementById("id_products-TOTAL_FORMS").value);
    for (var row = 0; row < count; row++) {
        const checkbox = document.getElementById("id_products-" + row +"-use_product_price");
        checkbox.addEventListener('click', checkVisibility);
        if (checkbox.checked) {
            document.getElementById("id_products-" + row +"-amount_netto_positiv").disabled = true;
            document.getElementById("id_products-" + row +"-vat").disabled = true;
            document.getElementById("id_products-" + row +"-amount_brutto_positiv").disabled = true;
        } else {
            document.getElementById("id_products-" + row +"-amount_netto_positiv").disabled = false;
            document.getElementById("id_products-" + row +"-vat").disabled = false;
            document.getElementById("id_products-" + row +"-amount_brutto_positiv").disabled = false;
        }
    }
}

function removeDisabled() {
    var elems = document.querySelectorAll('[disabled]');
    for (var i = 0; i < elems.length; i++) {
        elems[i].removeAttribute('disabled');
        if (!elems[i].value) elems[i].value = 0;
    }
}