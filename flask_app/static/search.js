var search = document.querySelector('#search')

search.addEventListener('search', updateValue);

function updateValue(e) {
    return e.target.value
}