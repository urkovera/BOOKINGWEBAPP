// Function to switch between pages (simulating navigation)
function switchPage(pageId) {
    // 1. Get all elements with the class 'page'
    const pages = document.querySelectorAll('.page');
    
    // 2. Hide all pages (display: none)
    pages.forEach(page => {
        page.style.display = 'none';
    });

    // 3. Show the target page based on the ID provided
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.style.display = 'block';
        
        // Optional: Reset fade-in animation when switching back to a page
        const animatedElements = targetPage.querySelectorAll('.fade-in');
        animatedElements.forEach(el => {
            el.style.animation = 'none';
            // Trigger reflow to restart animation
            el.offsetHeight; 
            el.style.animation = null; 
        });
    }
}

// Initialize default state when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // We rely on the inline style="display: none;" on register/home/about
    // to keep loginPage visible by default.
});
