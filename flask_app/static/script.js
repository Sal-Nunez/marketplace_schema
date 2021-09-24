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
console.log("SCRIPT FILE")
const amount = document.querySelector('#amount')
const prices = document.querySelectorAll('.price')
const quantities = document.querySelectorAll('.quantity')
// console.log(amount);
var sum = 0
for (var i = 0; i < prices.length; i++) {
            sum += parseInt(prices[i].innerText) * parseInt(quantities[i].innerText)
}
console.log(sum);
amount.value = parseInt(sum)
amount.innerText = parseInt(sum)