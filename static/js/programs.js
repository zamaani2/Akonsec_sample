document.addEventListener("DOMContentLoaded", function () {
    // Carousel functionality with improved performance
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    const dotsContainer = document.querySelector('.carousel-dots');
    let currentSlide = 0;
    let slideInterval;
    let isAnimating = false;

    // Create dots with proper ARIA attributes
    slides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', `Slide ${index + 1}`);
        dot.setAttribute('tabindex', '0');

        if (index === 0) {
            dot.classList.add('active');
            dot.setAttribute('aria-selected', 'true');
        } else {
            dot.setAttribute('aria-selected', 'false');
        }

        dot.addEventListener('click', () => goToSlide(index));
        dot.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                goToSlide(index);
            }
        });

        dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll('.dot');

    function updateSlide() {
        if (isAnimating) return;
        isAnimating = true;

        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            slide.setAttribute('aria-hidden', 'true');
            dots[i].classList.remove('active');
            dots[i].setAttribute('aria-selected', 'false');
        });

        slides[currentSlide].classList.add('active');
        slides[currentSlide].setAttribute('aria-hidden', 'false');
        dots[currentSlide].classList.add('active');
        dots[currentSlide].setAttribute('aria-selected', 'true');

        // Use requestAnimationFrame for smoother animations
        requestAnimationFrame(() => {
            setTimeout(() => {
                isAnimating = false;
            }, 800); // Match the CSS transition duration
        });
    }

    function nextSlide() {
        if (isAnimating) return;
        currentSlide = (currentSlide + 1) % slides.length;
        updateSlide();
    }

    function prevSlide() {
        if (isAnimating) return;
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateSlide();
    }

    function goToSlide(index) {
        if (isAnimating || currentSlide === index) return;
        currentSlide = index;
        updateSlide();
        resetInterval();
    }

    function resetInterval() {
        clearInterval(slideInterval);
        // Check if user prefers reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (!prefersReducedMotion) {
            slideInterval = setInterval(nextSlide, 5000);
        }
    }

    // Event listeners with improved accessibility
    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetInterval();
    });

    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetInterval();
    });

    // Keyboard navigation for carousel
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
            resetInterval();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            resetInterval();
        }
    });

    // Start automatic slideshow only if user doesn't prefer reduced motion
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        slideInterval = setInterval(nextSlide, 5000);
    }

    // Pause slideshow on hover or focus
    const carouselContainer = document.querySelector('.carousel-container');
    carouselContainer.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
    });

    carouselContainer.addEventListener('mouseleave', () => {
        resetInterval();
    });

    carouselContainer.addEventListener('focusin', () => {
        clearInterval(slideInterval);
    });

    carouselContainer.addEventListener('focusout', () => {
        resetInterval();
    });

    // Animation for stats with IntersectionObserver for better performance
    const statNumbers = document.querySelectorAll(".stat-number");

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "0";
                setTimeout(() => {
                    entry.target.style.animation = "countUp 0.8s forwards";
                }, 200);
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(stat => {
        statsObserver.observe(stat);
    });

    // Animation for leaders with IntersectionObserver
    const leaders = document.querySelectorAll(".leader");

    const leaderObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add("fade-in");
                }, 100 * index);
                leaderObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    leaders.forEach(leader => {
        leaderObserver.observe(leader);
    });

    // Program filtering functionality with improved accessibility
    const filterButtons = document.querySelectorAll(".filter-btn");
    const programs = document.querySelectorAll(".program");

    filterButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Remove active class and update ARIA attributes
            filterButtons.forEach((btn) => {
                btn.classList.remove("active");
                btn.setAttribute('aria-selected', 'false');
            });

            // Add active class and update ARIA attributes
            this.classList.add("active");
            this.setAttribute('aria-selected', 'true');

            const filterValue = this.getAttribute("data-filter");

            // Announce filter change for screen readers
            const filterAnnouncement = document.createElement('div');
            filterAnnouncement.setAttribute('aria-live', 'polite');
            filterAnnouncement.classList.add('sr-only');
            filterAnnouncement.textContent = `Showing ${filterValue} programs`;
            document.body.appendChild(filterAnnouncement);

            setTimeout(() => {
                document.body.removeChild(filterAnnouncement);
            }, 1000);

            // Show/hide programs based on filter with improved animation
            programs.forEach((program) => {
                const shouldShow = filterValue === "all" || program.getAttribute("data-category") === filterValue;

                if (shouldShow) {
                    program.style.display = "flex";
                    requestAnimationFrame(() => {
                        program.style.opacity = "1";
                        program.style.transform = "translateY(0)";
                    });
                } else {
                    program.style.opacity = "0";
                    program.style.transform = "translateY(20px)";

                    setTimeout(() => {
                        program.style.display = "none";
                    }, 300); // Match transition duration
                }
            });
        });
    });

    // Lazy load images for better performance
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports native lazy loading
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.setAttribute('loading', 'lazy');
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const lazyImages = document.querySelectorAll('img');

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Smooth scroll for anchor links with improved accessibility
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();

            const targetId = this.getAttribute("href");
            if (targetId === "#") return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Check if user prefers reduced motion
                if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    // Instant scroll for users who prefer reduced motion
                    targetElement.scrollIntoView();
                } else {
                    // Smooth scroll for others
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: "smooth",
                    });
                }

                // Set focus to the target element for accessibility
                targetElement.setAttribute('tabindex', '-1');
                targetElement.focus();

                // Update URL without page reload
                history.pushState(null, null, targetId);
            }
        });
    });
}); 