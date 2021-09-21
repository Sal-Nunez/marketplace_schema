var loginForm = document.querySelector('#login-form')
var regForm = document.querySelector('#reg-form')

loginForm.addEventListener('submit', function(e) {
    e.preventDefault()

    let form = new FormData(loginForm)

    fetch('/api/user/process_login', {
            method: 'POST',
            body: form
        })
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            if (data['status'] === 400) {
                let userInputError = document.querySelector('#user_input_error')
                let pwError = document.querySelector('#pw_error')
                userInputError.innerText = 'Something'

                let allErrors = document.querySelectorAll(".errors")
                for (const error of allErrors) {
                    let errorID = error.getAttribute('id')
                    if (errorId in data['errors']) {
                        error.innerText = data['errors'][errorId]
                    }
                }
            } else if (data['status'] === 200) {
                window.location.href = '/dashboard'
            }
        })
})

regForm.addEventListener('submit', function(e) {
    e.preventDefault()
})