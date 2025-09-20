document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navWrapper = document.querySelector('.nav-wrapper');
    const navLinks = document.querySelectorAll('.nav-links a');
    // Create overlay if not present
    let overlay = document.querySelector('.mobile-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'mobile-overlay';
        document.body.appendChild(overlay);
    }

    function closeMenu() {
        hamburger.classList.remove('active');
        navWrapper.classList.remove('active');
        overlay.classList.remove('active');
    }

    // Close menu when clicking outside the sidebar menu(nav-wrapper)
    document.addEventListener('click', function(e) {
        if (
            navWrapper.classList.contains('active') &&
            !navWrapper.contains(e.target) &&
            !hamburger.contains(e.target)
        ) {
            closeMenu();
        }
    });

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navWrapper.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', closeMenu);

    navLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    navWrapper.addEventListener('click', function(e) {
        // Only trigger if nav-wrapper itself is clicked, not its children
        if (e.target === navWrapper && navWrapper.classList.contains('active')) {
            navWrapper.classList.remove('active');
            document.querySelector('.hamburger').classList.remove('active');
            document.querySelector('.mobile-overlay').classList.remove('active');
        }
    });
});