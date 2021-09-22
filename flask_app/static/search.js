const search = document.querySelector('#search')
const suggestions = document.querySelector('#suggestions')

search.addEventListener('input', updateValue);

const products = ['Roses', 'Rose Petals', 'Rhodentrence', 'Daisy']

function updateValue(e) {
    // var log;
    const userInput = e.target.value.toLowerCase();
    suggestions.innerHTML = ""
    for (const product of products) {
        if (product.toLowerCase().includes(userInput)) {
            const li = document.createElement('li');
            li.onclick = e => search.value = li.innerText;
            li.innerText = product
            suggestions.append(li)
        }
    }
    // e.target.value;
    // console.log(suggestions.innerText);
}

console.log("Hello");