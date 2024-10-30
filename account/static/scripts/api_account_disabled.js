document.addEventListener("DOMContentLoaded", function () {
    fetchCsrfToken().then(fetchUserInfo);
});

// request CSRF token from server
function fetchCsrfToken() {
    return fetch('/csrf_token/', {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            if (data && data.csrfToken) {
                return data.csrfToken;
            } else {
                throw new Error("Failed to fetch CSRF token");
            }
        })
        .catch(error => console.error('Error fetching CSRF token:', error));
}

// request user info from server
function fetchUserInfo(csrfToken) {
    fetch('/api/user_info_short/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // 使用从服务器获取的CSRF token
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById("user-name").value = data.user_name;
                document.getElementById("user-email").value = data.user_email;
                document.getElementById("user-balance").value = data.user_balance;
            }
        })
        .catch(error => console.error('Error fetching user info:', error));
}