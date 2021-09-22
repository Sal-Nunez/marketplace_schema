const search = document.querySelector('#search')
const searchInput = document.querySelector('#search_input')

search.addEventListener('input', updateValue);

function updateValue(e) {
    // var log;
    searchInput.innerText = e.target.value;
    console.log(searchInput.innerText);
}

console.log("Hello");