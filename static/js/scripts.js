// Testimonials Carousel Slider
document.addEventListener('DOMContentLoaded', function () {
    const testimonialCarousel = document.querySelector('.testimonials-carousel');
    if (!testimonialCarousel) return;
    
    const grid = testimonialCarousel.querySelector('.testimonials-grid');
    const cards = Array.from(grid.querySelectorAll('.testimonial-card'));
    const leftArrow = testimonialCarousel.querySelector('.testimonial-arrow-left');
    const rightArrow = testimonialCarousel.querySelector('.testimonial-arrow-right');
    const dotsContainer = testimonialCarousel.querySelector('.testimonial-dots');
    
    let currentSlide = 0;
    let cardsPerView = 4; // Default for desktop
    
    // Function to update cards per view based on screen size
    function updateCardsPerView() {
        if (window.innerWidth <= 768) {
            cardsPerView = 1;
        } else if (window.innerWidth <= 1024) {
            cardsPerView = 2;
        } else {
            cardsPerView = 4;
        }
    }
    
    // Calculate total slides
    function getTotalSlides() {
        return Math.ceil(cards.length / cardsPerView);
    }
    
    // Create dots
    function createDots() {
        dotsContainer.innerHTML = '';
        const totalSlides = getTotalSlides();
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('div');
            dot.className = 'testimonial-dot' + (i === 0 ? ' active' : '');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }
    
    // Update dots
    function updateDots() {
        const dots = dotsContainer.querySelectorAll('.testimonial-dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
    
    // Go to specific slide
    function goToSlide(slideIndex) {
        const totalSlides = getTotalSlides();
        currentSlide = Math.max(0, Math.min(slideIndex, totalSlides - 1));
        
        // Calculate the percentage to move based on cards per view
        const cardWidth = 100 / cardsPerView; // Each card takes this % of container width
        const translateX = -(currentSlide * cardsPerView * cardWidth);
        grid.style.transform = `translateX(${translateX}%)`;
        
        updateDots();
        updateArrowStates();
    }
    
    // Update arrow states
    function updateArrowStates() {
        const totalSlides = getTotalSlides();
        leftArrow.style.opacity = currentSlide === 0 ? '0.5' : '1';
        rightArrow.style.opacity = currentSlide === totalSlides - 1 ? '0.5' : '1';
        leftArrow.style.pointerEvents = currentSlide === 0 ? 'none' : 'auto';
        rightArrow.style.pointerEvents = currentSlide === totalSlides - 1 ? 'none' : 'auto';
    }
    
    // Next slide
    function nextSlide() {
        const totalSlides = getTotalSlides();
        if (currentSlide < totalSlides - 1) {
            goToSlide(currentSlide + 1);
        }
    }
    
    // Previous slide
    function prevSlide() {
        if (currentSlide > 0) {
            goToSlide(currentSlide - 1);
        }
    }
    
    // Initialize
    function init() {
        updateCardsPerView();
        createDots();
        goToSlide(0);
    }
    
    // Event listeners
    leftArrow.addEventListener('click', prevSlide);
    rightArrow.addEventListener('click', nextSlide);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        updateCardsPerView();
        createDots();
        goToSlide(0); // Reset to first slide on resize
    });
    
    // Initialize the carousel
    init();
});

// Brand Carousel Slider
document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.brand-carousel');
    if (!carousel) return;
    const slidesContainer = carousel.querySelector('.brand-slides');
    const slides = Array.from(carousel.querySelectorAll('.brand-slide'));
    const dotsContainer = carousel.querySelector('.brand-dots');
    const leftArrow = carousel.querySelector('.brand-arrow-left');
    const rightArrow = carousel.querySelector('.brand-arrow-right');
    let current = 0;
    let intervalId = null;

    // Create dots
    slides.forEach((_, idx) => {
        const dot = document.createElement('div');
        dot.className = 'brand-dot' + (idx === 0 ? ' active' : '');
        dot.addEventListener('click', () => {
            goToSlide(idx);
            resetInterval();
        });
        dotsContainer.appendChild(dot);
    });

    function updateDots(idx) {
        dotsContainer.querySelectorAll('.brand-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === idx);
        });
    }

    function updateArrowStates() {
        leftArrow.style.opacity = current === 0 ? '0.5' : '1';
        rightArrow.style.opacity = current === slides.length - 1 ? '0.5' : '1';
        leftArrow.style.pointerEvents = current === 0 ? 'none' : 'auto';
        rightArrow.style.pointerEvents = current === slides.length - 1 ? 'none' : 'auto';
    }

    function goToSlide(idx) {
        current = idx;
        slidesContainer.style.transform = `translateX(-${idx * 100}%)`;
        updateDots(idx);
        updateArrowStates();
    }

    function nextSlide() {
        if (current < slides.length - 1) {
            goToSlide(current + 1);
        } else {
            goToSlide(0); // Loop back to first slide
        }
    }

    function prevSlide() {
        if (current > 0) {
            goToSlide(current - 1);
        } else {
            goToSlide(slides.length - 1); // Loop to last slide
        }
    }

    function resetInterval() {
        if (intervalId) clearInterval(intervalId);
        intervalId = setInterval(nextSlide, 5000);
    }

    // Event listeners for arrows
    if (leftArrow) leftArrow.addEventListener('click', () => {
        prevSlide();
        resetInterval();
    });
    
    if (rightArrow) rightArrow.addEventListener('click', () => {
        nextSlide();
        resetInterval();
    });

    // Initialize
    goToSlide(0);
    resetInterval();

    // Pause on hover
    carousel.addEventListener('mouseenter', () => clearInterval(intervalId));
    carousel.addEventListener('mouseleave', resetInterval);

    // Responsive: update on window resize
    window.addEventListener('resize', () => goToSlide(current));
});
// Number count-up animation for .stat-number elements
document.addEventListener('DOMContentLoaded', function () {
    function animateCountUp(el, target, duration) {
        let start = 0;
        let startTimestamp = null;
        const isPercent = /%$/.test(target);
        const isPlus = /\+$/.test(target);
        const cleanTarget = parseFloat(target.replace(/[^\d.]/g, ''));
        function step(timestamp) {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (cleanTarget - start) + start);
            el.textContent = value + (isPercent ? '%' : '') + (isPlus ? '+' : '');
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                el.textContent = target; // Ensure final value is exact
            }
        }
        window.requestAnimationFrame(step);
    }

    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    let animated = false;
    function triggerAnimations() {
        if (animated) return;
        const statNumbers = document.querySelectorAll('.stat-number');
        let anyVisible = false;
        statNumbers.forEach(function (el) {
            if (isInViewport(el)) {
                anyVisible = true;
                animateCountUp(el, el.getAttribute('data-target') || el.textContent, 1500);
            }
        });
        if (anyVisible) animated = true;
    }

    // Set data-target attribute for each stat-number
    document.querySelectorAll('.stat-number').forEach(function (el) {
        el.setAttribute('data-target', el.textContent.trim());
        el.textContent = '0' + (/%$/.test(el.getAttribute('data-target')) ? '%' : '') + (/\+$/.test(el.getAttribute('data-target')) ? '+' : '');
    });

    window.addEventListener('scroll', triggerAnimations);
    triggerAnimations(); // In case already in view
});
  // Mobile Menu Toggle
const mobileToggle = document.getElementById('mobile-toggle');
const navMenu = document.getElementById('nav-menu');

mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    const icon = mobileToggle.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-times');
});

// Header Scroll Effect
const header = document.getElementById('header');
let lastScrollTop = 0;

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    lastScrollTop = scrollTop;
});

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerHeight = header.offsetHeight;
            const targetPosition = target.offsetTop - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
        
        // Close mobile menu if open
        navMenu.classList.remove('active');
        const icon = mobileToggle.querySelector('i');
        icon.classList.add('fa-bars');
        icon.classList.remove('fa-times');
    });
});

// Form Submission
const quoteForm = document.getElementById('quote-form');
quoteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(quoteForm);
    const data = Object.fromEntries(formData);
    
    // Show success message (replace with actual form handling)
    alert('Thank you for your inquiry! We will contact you within 24 hours with your free quote.');
    
    // Reset form
    quoteForm.reset();
    
    // In a real application, you would send this data to your server
    console.log('Form submitted:', data);
});

// Animate stats on scroll
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -100px 0px'
};

const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animationPlayState = 'running';
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-item').forEach(item => {
    statObserver.observe(item);
});

// Add loading animation to cards
const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.usp-card, .testimonial-card, .reason-item').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    cardObserver.observe(card);
});

// Add floating animation to hero elements
document.addEventListener('DOMContentLoaded', () => {
    const heroContent = document.querySelector('.hero-content');
    const heroForm = document.querySelector('.hero-form');
    
    setTimeout(() => {
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
    }, 300);
    
    setTimeout(() => {
        heroForm.style.opacity = '1';
        heroForm.style.transform = 'translateY(0)';
    }, 600);
});

// Add hover effect to brand logos
document.querySelectorAll('.brand-logo').forEach(logo => {
    logo.addEventListener('mouseenter', () => {
        logo.style.backgroundColor = 'var(--bright-cyan)';
        logo.style.color = 'var(--white)';
    });
    
    logo.addEventListener('mouseleave', () => {
        logo.style.backgroundColor = 'var(--white)';
        logo.style.color = 'var(--primary-navy)';
    });
});

// Add click tracking for analytics (placeholder)
document.querySelectorAll('.cta-button, .social-link, .nav-link').forEach(element => {
    element.addEventListener('click', (e) => {
        // Track clicks for analytics
        const elementType = e.target.className;
        const elementText = e.target.textContent || e.target.title;
        console.log(`Clicked: ${elementType} - ${elementText}`);
        
        // In a real application, send this to your analytics service
        // gtag('event', 'click', { element_type: elementType, element_text: elementText });
    });
});

// Preload critical images and optimize performance
const criticalImages = [
    // Add any critical image URLs here
];

criticalImages.forEach(src => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'image';
    link.href = src;
    document.head.appendChild(link);
});

// Add typing effect to hero title (optional enhancement)
const heroTitle = document.querySelector('.hero-title');
const titleText = heroTitle.textContent;
heroTitle.textContent = '';

let i = 0;
const typeWriter = () => {
    if (i < titleText.length) {
        heroTitle.textContent += titleText.charAt(i);
        i++;
        setTimeout(typeWriter, 50);
    }
};

setTimeout(typeWriter, 1000);

// Add scroll progress indicator
const scrollProgress = document.createElement('div');
scrollProgress.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: var(--bright-cyan);
    z-index: 9999;
    transition: width 0.1s ease;
`;
document.body.appendChild(scrollProgress);

window.addEventListener('scroll', () => {
    const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    scrollProgress.style.width = scrolled + '%';
});

// Add WhatsApp floating button
const whatsappButton = document.createElement('a');
whatsappButton.href = 'https://wa.me/60122992909?text=Hi, I would like to get a quote for air conditioning service';
whatsappButton.target = '_blank';
whatsappButton.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: #25D366;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    text-decoration: none;
    box-shadow: var(--shadow-large);
    z-index: 1000;
    transition: all 0.3s ease;
`;
whatsappButton.innerHTML = '<i class="fab fa-whatsapp"></i>';

whatsappButton.addEventListener('mouseenter', () => {
    whatsappButton.style.transform = 'scale(1.1)';
    whatsappButton.style.boxShadow = '0 25px 30px -5px rgba(0, 0, 0, 0.2)';
});

whatsappButton.addEventListener('mouseleave', () => {
    whatsappButton.style.transform = 'scale(1)';
    whatsappButton.style.boxShadow = 'var(--shadow-large)';
});

document.body.appendChild(whatsappButton);

