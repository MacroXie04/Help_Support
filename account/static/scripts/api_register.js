// Request CSRF token
function getCSRFToken() {
    return fetch('/csrf_token/', {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject('Failed to fetch CSRF token');
            }
        })
        .then(data => data.csrfToken);
}

// Display messages under specific input fields
function displayFieldMessage(elementId, message, isError = true) {
    const element = document.getElementById(elementId);
    const feedback = element.parentElement.querySelector('.invalid-feedback');
    feedback.textContent = message;
    feedback.style.display = isError ? 'block' : 'none';
    element.classList.toggle('is-invalid', isError);
}

// Generate Registration Form
function createRegisterForm() {
    const formContainer = document.getElementById('registerFormContainer');
    const formHTML = `
    
    <form id="registerForm" novalidate>
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-person-circle font-14"></i>
            <input type="text" class="form-control rounded-xs" id="username" name="username" placeholder="Username" required>
            <label for="username" class="color-theme">Username</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-person-fill font-14"></i>
            <input type="text" class="form-control rounded-xs" id="first_name" name="first_name" placeholder="First Name" required>
            <label for="first_name" class="color-theme">First Name</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-person-fill font-14"></i>
            <input type="text" class="form-control rounded-xs" id="last_name" name="last_name" placeholder="Last Name" required>
            <label for="last_name" class="color-theme">Last Name</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-gender-ambiguous font-14"></i>
            <select class="form-control rounded-xs" id="gender" name="gender" required>
                <option value="" disabled selected>Select Gender</option>
                <option value="Man">Man</option>
                <option value="Woman">Woman</option>
                
            </select>
            <label for="gender" class="color-theme">Gender</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-telephone font-14"></i>
            <input type="text" class="form-control rounded-xs" id="phone" name="phone" placeholder="Phone Number" required>
            <label for="phone" class="color-theme">Phone Number</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-envelope font-14"></i>
            <input type="email" class="form-control rounded-xs" id="email" name="email" placeholder="Email" required>
            <label for="email" class="color-theme">Email</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
        
        <div class="mb-3">
            <button type="button" id="sendCodeButton" class="btn btn-primary w-100">
                Send Code
            </button>
        </div>
        
        <div class="d-flex align-items-center form-custom form-label form-icon mb-3">
            <div style="flex: 1;">
                <i class="bi bi-shield-lock font-14"></i>
                <input type="text" class="form-control rounded-xs" id="verification_code" name="verification_code" placeholder="Verification Code" required>
                <label for="verification_code" class="color-theme">Verification Code</label>
                <div class="valid-feedback"></div>
                <div class="invalid-feedback"></div>
            </div>
        </div>

    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-asterisk font-12"></i>
            <input type="password" class="form-control rounded-xs" id="password1" name="password1" placeholder="Password" required>
            <label for="password1" class="color-theme">Password</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>
    
        <div class="form-custom form-label form-icon mb-3">
            <i class="bi bi-asterisk font-12"></i>
            <input type="password" class="form-control rounded-xs" id="password2" name="password2" placeholder="Confirm Password" required>
            <label for="password2" class="color-theme">Confirm Password</label>
            <div class="valid-feedback"></div>
            <div class="invalid-feedback"></div>
        </div>

    <button type="submit" class="btn btn-full bg-green-dark rounded-xs text-uppercase font-700 w-100 btn-s mt-4">Create Account</button>
    </form>
        <div id="register_message" class="text-danger text-center mt-n3" style="display: none"></div>
    `;
    formContainer.innerHTML = formHTML;

// Event listener for "Send Code" button
    let isCodeRequestAllowed = true;
    let cooldownSeconds = 60;

    document.getElementById('sendCodeButton').addEventListener('click', function () {
        const email = document.getElementById('email').value.trim();

        if (!email) {
            displayFieldMessage('email', 'Please enter an email address to receive the code.');
            return;
        }

        if (!isCodeRequestAllowed) {
            displayFieldMessage('email', `Please wait ${cooldownSeconds} seconds before requesting another code.`);
            return;
        }

        // Get CSRF token and send verification code request
        getCSRFToken()
            .then(csrfToken => {
                return fetch('/api/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({action: 'send_verification_code', email})
                });
            })
            .then(response => {
                if (response.ok) {
                    displayFieldMessage('email', 'Verification code sent to your email.', false);
                    startCooldown();
                } else {
                    return response.json().then(data => Promise.reject(data));
                }
            })
            .catch(errorData => {
                displayFieldMessage('email', errorData.error || 'Failed to send verification code. Please try again.');
            });
    });

    function startCooldown() {
        isCodeRequestAllowed = false;
        document.getElementById('sendCodeButton').disabled = true;

        const cooldownInterval = setInterval(() => {
            cooldownSeconds--;
            document.getElementById('sendCodeButton').innerText = `Wait ${cooldownSeconds}s`;

            if (cooldownSeconds <= 0) {
                clearInterval(cooldownInterval);
                isCodeRequestAllowed = true;
                cooldownSeconds = 60; // Reset cooldown time
                document.getElementById('sendCodeButton').disabled = false;
                document.getElementById('sendCodeButton').innerText = 'Send Code';
            }
        }, 1000);
    }

    // Handle registration form submission
    document.getElementById('registerForm').addEventListener('submit', function (e) {
        e.preventDefault();

        // Gather form values
        const username = document.getElementById('username').value.trim();
        const password1 = document.getElementById('password1').value.trim();
        const password2 = document.getElementById('password2').value.trim();
        const email = document.getElementById('email').value.trim();
        const code = document.getElementById('verification_code').value.trim();
        const firstName = document.getElementById('first_name').value.trim();
        const lastName = document.getElementById('last_name').value.trim();
        const gender = document.getElementById('gender').value;
        const phone = document.getElementById('phone').value.trim();

        // Clear previous error messages
        ['username', 'password1', 'password2', 'email', 'verification_code', 'first_name', 'last_name', 'gender', 'phone']
            .forEach(fieldId => displayFieldMessage(fieldId, '', false));

        // Validate fields
        if (!username) displayFieldMessage('username', 'Username is required!');
        if (!password1) displayFieldMessage('password1', 'Password is required!');
        if (!password2) displayFieldMessage('password2', 'Confirmation password is required!');
        if (password1 && password2 && password1 !== password2) {
            displayFieldMessage('password2', 'Passwords do not match!');
            return;
        }
        if (!email) displayFieldMessage('email', 'Email is required!');
        if (!code) displayFieldMessage('verification_code', 'Verification code is required!');
        if (!firstName) displayFieldMessage('first_name', 'First name is required!');
        if (!lastName) displayFieldMessage('last_name', 'Last name is required!');
        if (!gender) displayFieldMessage('gender', 'Gender selection is required!');
        if (!phone) displayFieldMessage('phone', 'Phone number is required!');

        // Get CSRF token and send registration request
        getCSRFToken()
            .then(csrfToken => {
                return fetch('/api/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        action: 'register',
                        username,
                        password: password1,
                        email,
                        code,
                        first_name: firstName,
                        last_name: lastName,
                        gender,
                        phone
                    })
                });
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(data => Promise.reject(data));
                }
            })
            .then(data => {
                if (data.success) {
                    // Redirect to login page on successful registration
                    window.location.href = data.redirect_url;
                }
            })
            .catch(errorData => {
                // Display error messages for each field based on returned JSON
                Object.keys(errorData).forEach(field => {
                    if (field !== 'success') { // Ignore the 'success' key
                        displayFieldMessage(field, errorData[field]);
                    }
                });
            });
    });
}

// Initialize registration form
document.addEventListener('DOMContentLoaded', createRegisterForm);