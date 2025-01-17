document.addEventListener("DOMContentLoaded", function () {
    const login = document.getElementById("login-link");
    const sigin = document.getElementById("sigin-link");
    const userInfo = document.getElementById("user-info");
    if (user === "AnonymousUser") {
        login.style.display = "block";
        sigin.style.display = "block";
        userInfo.style.display = "none";
    } else {
        login.style.display = "none";
        sigin.style.display = "none";
        userInfo.style.display = "block";
    }
});