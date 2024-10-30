document.addEventListener("DOMContentLoaded", function () {
    fetchCsrfToken().then(csrfToken => fetchUserInfo(csrfToken));
});

// 请求服务器获取 CSRF token
function fetchCsrfToken() {
    return fetch('/csrf_token/', {
        method: 'GET',
        credentials: 'include'  // 包含凭证以确保会话安全
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

// 请求服务器获取用户信息并更新页面
function fetchUserInfo(csrfToken) {
    fetch('/api/user_info/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,  // 设置 CSRF token 头
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                document.getElementById("username").value = data.user_name;
                document.getElementById("email").value = data.user_email;
                document.getElementById("full-name").value = data.user_full_name;
                document.getElementById("phone").value = data.user_phone;
                document.getElementById("account-balance").value = data.user_balance;
                document.getElementById("created-at").value = data.user_created_at;
                document.getElementById("gender").value = data.user_gender;
            }
        })
        .catch(error => console.error('Error fetching user info:', error));
}