document.addEventListener('DOMContentLoaded', function() {
    // Function to show a specific page
    function showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.style.display = 'none';
        });

        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.style.display = 'block';
            targetPage.classList.add('fade-in'); 
        }
    }

    // Initial load: ensure only loginPage is visible
    showPage('loginPage');

    // Event listener for "Register now" link
    const toRegisterLink = document.getElementById('toRegister');
    if (toRegisterLink) {
        toRegisterLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('registerPage');
        });
    }

    // Event listener for "Login" link on Register page
    const toLoginLink = document.getElementById('toLogin');
    if (toLoginLink) {
        toLoginLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('loginPage');
        });
    }
    
    // Event listeners for header navigation links
    document.getElementById('navHome').addEventListener('click', function(e) {
        e.preventDefault();
        showPage('homePage');
    });
    
    document.getElementById('navAbout').addEventListener('click', function(e) {
        e.preventDefault();
        showPage('aboutPage');
    });
    
    document.getElementById('navLogin').addEventListener('click', function(e) {
        e.preventDefault();
        showPage('loginPage');
    });
    

    // Form submission logic
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Implement actual login logic (e.g., AJAX/fetch) here
            console.log("Login submitted");
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Implement actual registration logic (e.g., AJAX/fetch) here
            console.log("Register submitted");
        });
    }
});
