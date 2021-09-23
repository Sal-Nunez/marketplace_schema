var loginForm = document.querySelector('#login-form')
var regForm = document.querySelector('#reg-form')

regForm.addEventListener('submit', function(e) {
    e.preventDefault()

    let form = new FormData(regForm)

    fetch('/register', {
            method: 'POST',
            body: form
        })
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            if (data['status'] === 400) {
                let allErrors = document.querySelectorAll(".errors")
                for (const error of allErrors) {
                    let errorID = error.getAttribute('id')
                    if (errorID in data['errors']) {
                        error.innerText = data['errors'][errorID]
                    }
                }
            } else if (data['status'] === 200) {
                window.location.href = '/'
            }
        })
    })

loginForm.addEventListener('submit', function(e) {
    e.preventDefault()

    let form = new FormData(loginForm)

    fetch('/login', {
            method: 'POST',
            body: form
        })
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            if (data['status'] === 400) {
                let allErrors = document.querySelectorAll(".errors")
                for (const error of allErrors) {
                    let errorID = error.getAttribute('id')
                    if (errorID in data['errors']) {
                        error.innerText = data['errors'][errorID]
                    }
                }
            } else if (data['status'] === 200) {
                window.location.href = '/'
            }
        })
    })