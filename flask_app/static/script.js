$(document).ready(function() {
    $(".dropdown").hover(function() {
        var dropdownMenu = $(this).children(".dropdown-menu");
        if (dropdownMenu.is(":visible")) {
            dropdownMenu.parent().toggleClass("open");
        }
    });
});

function myFunction() {
    var x = document.getElementById("mySelect").value;
    console.log('hello')
}

function getURL() {
    return window.location.href;
}

function selectChange() {
    const selectElement = document.querySelector('#form');
    const price = document.querySelector('#price');
    const result = document.querySelector('#result');
    result.innerText = '$' + selectElement.value * price.innerText;
}