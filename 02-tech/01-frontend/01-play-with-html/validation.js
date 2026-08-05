


// using DOM to validate form inputs
//------------------------------------

const form = document.querySelector('#loginForm');
form.addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission
    console.log('Form submitted');
    // read form fields using FormData API
    const formData = new FormData(form);
    const email = formData.get('email');
    const password = formData.get('password');


    // validate email and password
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    // validate email format using regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return;
    }

    // validate password length
    if (password.length < 6) {
        alert('Password must be at least 6 characters long');
        return;
    }

    // if all validations pass, submit the form
    alert('Form submitted successfully');

});