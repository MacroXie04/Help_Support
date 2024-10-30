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
                <option value="Abinary">Abinary</option>
                <option value="Agender">Agender</option>
                <option value="Ambigender">Ambigender</option>
                <option value="Androgyne">Androgyne</option>
                <option value="Androgynous">Androgynous</option>
                <option value="Aporagender">Aporagender</option>
                <option value="Autigender">Autigender</option>
                <option value="Bakla">Bakla</option>
                <option value="Bigender">Bigender</option>
                <option value="Binary">Binary</option>
                <option value="Bissu">Bissu</option>
                <option value="Butch">Butch</option>
                <option value="Calabai">Calabai</option>
                <option value="Calalai">Calalai</option>
                <option value="Cis">Cis</option>
                <option value="Cisgender">Cisgender</option>
                <option value="Cis female">Cis female</option>
                <option value="Cis male">Cis male</option>
                <option value="Cis man">Cis man</option>
                <option value="Cis woman">Cis woman</option>
                <option value="Demi-boy">Demi-boy</option>
                <option value="Demiflux">Demiflux</option>
                <option value="Demigender">Demigender</option>
                <option value="Demi-girl">Demi-girl</option>
                <option value="Demi-guy">Demi-guy</option>
                <option value="Demi-man">Demi-man</option>
                <option value="Demi-woman">Demi-woman</option>
                <option value="Dual gender">Dual gender</option>
                <option value="Eunuch">Eunuch</option>
                <option value="Fa'afafine">Fa'afafine</option>
                <option value="Female">Female</option>
                <option value="Female to male">Female to male</option>
                <option value="Femme">Femme</option>
                <option value="FTM">FTM</option>
                <option value="Gender bender">Gender bender</option>
                <option value="Gender diverse">Gender diverse</option>
                <option value="Gender gifted">Gender gifted</option>
                <option value="Genderfae">Genderfae</option>
                <option value="Genderfluid">Genderfluid</option>
                <option value="Genderflux">Genderflux</option>
                <option value="Genderfuck">Genderfuck</option>
                <option value="Genderless">Genderless</option>
                <option value="Gender nonconforming">Gender nonconforming</option>
                <option value="Genderqueer">Genderqueer</option>
                <option value="Gender questioning">Gender questioning</option>
                <option value="Gender variant">Gender variant</option>
                <option value="Graygender">Graygender</option>
                <option value="Hijra">Hijra</option>
                <option value="Intergender">Intergender</option>
                <option value="Intersex">Intersex</option>
                <option value="Ipsogender">Ipsogender</option>
                <option value="Kathoey">Kathoey</option>
                <option value="Māhū">Māhū</option>
                <option value="Male">Male</option>
                <option value="Male to female">Male to female</option>
                <option value="Man of trans experience">Man of trans experience</option>
                <option value="Maverique">Maverique</option>
                <option value="Meta-gender">Meta-gender</option>
                <option value="MTF">MTF</option>
                <option value="Multigender">Multigender</option>
                <option value="Muxe">Muxe</option>
                <option value="Neither">Neither</option>
                <option value="Neurogender">Neurogender</option>
                <option value="Neutrois">Neutrois</option>
                <option value="Non-binary">Non-binary</option>
                <option value="Non-binary transgender">Non-binary transgender</option>
                <option value="Omnigender">Omnigender</option>
                <option value="Other">Other</option>
                <option value="Pangender">Pangender</option>
                <option value="Person of transgendered experience">Person of transgendered experience</option>
                <option value="Polygender">Polygender</option>
                <option value="Queer">Queer</option>
                <option value="Sekhet">Sekhet</option>
                <option value="Third gender">Third gender</option>
                <option value="Trans">Trans</option>
                <option value="Trans female">Trans female</option>
                <option value="Trans male">Trans male</option>
                <option value="Trans man">Trans man</option>
                <option value="Trans person">Trans person</option>
                <option value="Trans woman">Trans woman</option>
                <option value="Transgender">Transgender</option>
                <option value="Transgender female">Transgender female</option>
                <option value="Transgender male">Transgender male</option>
                <option value="Transgender man">Transgender man</option>
                <option value="Transgender person">Transgender person</option>
                <option value="Transgender woman">Transgender woman</option>
                <option value="Transfeminine">Transfeminine</option>
                <option value="Transmasculine">Transmasculine</option>
                <option value="Transsexual">Transsexual</option>
                <option value="Transsexual female">Transsexual female</option>
                <option value="Transsexual male">Transsexual male</option>
                <option value="Transsexual man">Transsexual man</option>
                <option value="Transsexual person">Transsexual person</option>
                <option value="Transsexual woman">Transsexual woman</option>
                <option value="Travesti">Travesti</option>
                <option value="Trigender">Trigender</option>
                <option value="Tumtum">Tumtum</option>
                <option value="Two spirit">Two spirit</option>
                
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