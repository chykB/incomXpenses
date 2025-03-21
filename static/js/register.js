const usernameField = document.querySelector('#usernamefield');
const feedBackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector('#emailfield');
const emailfeedBackArea = document.querySelector('.email-invalid-feedback');
const passwordField = document.querySelector('#passwordField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn')


const handlePasswordToggle = (e) => {
    if (showPasswordToggle.textContent === 'SHOW'){
        showPasswordToggle.textContent = 'HIDE'
        passwordField.setAttribute('type', 'password');
    }else {
        showPasswordToggle.textContent = 'SHOW'
        passwordField.setAttribute('type', 'text');
    }

}
showPasswordToggle.addEventListener('click', handlePasswordToggle);



emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;

    emailField.classList.remove('is-invalid');
    emailfeedBackArea.style.display = 'none';
    if (emailValue.length > 0){
        fetch("/authentication/validate_email", {
            body: JSON.stringify({email: emailValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data:', data);
            if (data.email_error){
                submitBtn.disabled =true;
                emailField.classList.add('is-invalid');
                emailfeedBackArea.style.display = 'block';
                emailfeedBackArea.innerHTML = `<p>${data.email_error}</p>`;

            }else {
                submitBtn.removeAttribute('disabled');
            }
        })
    }
})

usernameField.addEventListener('keyup', (e) => {
    
    const usernameValue = e.target.value;
    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display = 'none';

    if (usernameValue.length > 0){
        fetch("/authentication/validate_username", {
            body: JSON.stringify({username: usernameValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data:', data);
            if (data.username_error){
                submitBtn.disabled = true;
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;

            }else {
                submitBtn.removeAttribute('disabled');
            }
        })
    }
    
});
