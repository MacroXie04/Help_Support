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

// Display field-specific error messages
function displayFieldMessage(elementId, message, isError = true) {
    const element = document.getElementById(elementId);
    const feedback = element.parentElement.querySelector('.invalid-feedback');
    feedback.textContent = message;
    feedback.style.display = isError ? 'block' : 'none';
    element.classList.toggle('is-invalid', isError);
}

// JavaScript function to create login form
function createLoginForm() {
    const formContainer = document.getElementById('loginFormContainer');

    const formHTML = `
        <form id="loginForm" novalidate>
            <div class="form-custom form-label form-icon mb-3">
                <i class="bi bi-person-circle font-14"></i>
                <input type="text" class="form-control rounded-xs" id="username" name="username" placeholder="Username">
                <label for="username" class="color-theme">Username or Email</label>
                <div class="valid-feedback"></div>
                <div class="invalid-feedback"></div>
            </div>
            <div class="form-custom form-label form-icon mb-3">
                <i class="bi bi-asterisk font-12"></i>
                <input type="password" class="form-control rounded-xs" id="password" name="password" placeholder="Password">
                <label for="password" class="color-theme">Password</label>
                <div class="valid-feedback"></div>
                <div class="invalid-feedback"></div>
            </div>
            <button type="submit" class="btn btn-full bg-blue-dark rounded-xs text-uppercase font-700 w-100 btn-s mt-4">Sign In</button>
        </form>
    `;

    formContainer.innerHTML = formHTML;
}

// Initialize login form
createLoginForm();

// Add event listener to login form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const submitButton = document.querySelector('button[type="submit"]');

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission

        // Get username and password values
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // Reset error messages
        displayFieldMessage('username', '', false);
        displayFieldMessage('password', '', false);

        // Check if username and password are empty
        if (!username) {
            displayFieldMessage('username', 'Username is required!');
        }
        if (!password) {
            displayFieldMessage('password', 'Password is required!');
        }
        if (!username || !password) return; // Stop if validation fails

        // Disable submit button and change text
        submitButton.disabled = true;
        submitButton.innerHTML = 'Logging in...';

        // 10-second timeout
        const timeout = setTimeout(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Sign In';
            displayFieldMessage('username', 'Login request timed out. Please try again.');
        }, 10000);

        // Get CSRF token and send login request
        getCSRFToken()
            .then(csrfToken => {
                return fetch('/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password,
                    })
                });
            })
            .then(response => {
                clearTimeout(timeout); // Clear timeout if request succeeds
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(errorData => Promise.reject(errorData));
                }
            })
            .then(data => {
                if (data.success) {
                    window.location.href = '/';
                }
            })
            .catch(errorData => {
                // Handle specific errors based on the response
                if (errorData.error.includes('Account locked')) {
                    displayFieldMessage('username', errorData.error);
                } else if (errorData.error.includes('Invalid credentials')) {
                    displayFieldMessage('username', errorData.error);
                } else if (errorData.error.includes('Username and password required')) {
                    displayFieldMessage('username', 'Username is required!');
                    displayFieldMessage('password', 'Password is required!');
                } else {
                    displayFieldMessage('username', errorData.error || 'Login failed. Please try again.');
                }
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Sign In';
            });
    });
});