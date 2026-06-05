// This small script controls the mobile navigation menu.
const menuBtn = document.getElementById('menuBtn');
const navLinks = document.getElementById('navLinks');

if (menuBtn) {
    menuBtn.addEventListener('click', function () {
        navLinks.classList.toggle('show');
    });
}
