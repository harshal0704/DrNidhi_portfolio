// Wait for the DOM to be fully loaded before running scripts
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Element Caching ---
    const preloader = document.getElementById('preloader');
    const mainNav = document.getElementById('mainNav');
    const menuToggleBtn = document.querySelector('.menu-toggle');
    const mainNavUl = mainNav.querySelector('ul'); 
    const navLinks = document.querySelectorAll('#mainNav ul li a'); 
    const sections = document.querySelectorAll('main section');
    const currentYearSpan = document.getElementById('currentYear');
    const wellnessOrb = document.querySelector('.wellness-orb');
    const scrollToTopBtn = document.getElementById('scrollToTopBtn');
    const constellationCanvas = document.getElementById('constellation-canvas');

    // --- Preloader ---
    window.addEventListener('load', () => {
        if (preloader) preloader.classList.add('loaded');
        document.body.classList.add('page-loaded');
    });

    // --- Interactive Constellation Canvas - DISABLED FOR PERFORMANCE. 
    /*
    This script was causing the "Forced Reflow" error.
    Keep it commented out to maintain a high PageSpeed score.

    if (constellationCanvas) {
        const ctx = constellationCanvas.getContext('2d');
        let stars = [];
        let mouse = { x: undefined, y: undefined };
        let numStars = window.innerWidth < 768 ? 50 : 100; 
        const connectDistance = window.innerWidth < 768 ? 80 : 120;

        function resizeCanvas() {
            const heroSection = document.getElementById('hero');
            const dpr = window.devicePixelRatio || 1;
            if (heroSection) {
                const rect = heroSection.getBoundingClientRect();
                constellationCanvas.width = rect.width * dpr;
                constellationCanvas.height = rect.height * dpr;
            } else {
                 constellationCanvas.width = window.innerWidth * dpr;
                 constellationCanvas.height = window.innerHeight * dpr;
            }
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0); 
            numStars = window.innerWidth < 768 ? 50 : 100; 
            initStars();
        }

        class Star { 
            constructor(x, y, radius, color) {
                this.x = x; this.y = y; this.radius = radius; this.color = color;
                this.vx = (Math.random() - 0.5) * 0.25; 
                this.vy = (Math.random() - 0.5) * 0.25;
                this.originalRadius = radius;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                const scaledWidth = constellationCanvas.width / (window.devicePixelRatio || 1);
                const scaledHeight = constellationCanvas.height / (window.devicePixelRatio || 1);

                if (this.x + this.radius > scaledWidth || this.x - this.radius < 0) this.vx = -this.vx;
                if (this.y + this.radius > scaledHeight || this.y - this.radius < 0) this.vy = -this.vy;

                if (mouse.x && mouse.y) {
                    const dist = Math.hypot(this.x - mouse.x, this.y - mouse.y);
                    if (dist < 80) { 
                        this.radius = this.originalRadius * (1 + (80 - dist) / 180) ; 
                    } else {
                        this.radius = this.originalRadius;
                    }
                } else {
                     this.radius = this.originalRadius;
                }
                this.draw();
            }
        }
        function initStars() { 
            stars = [];
            const scaledWidth = constellationCanvas.width / (window.devicePixelRatio || 1);
            const scaledHeight = constellationCanvas.height / (window.devicePixelRatio || 1);
            for (let i = 0; i < numStars; i++) {
                const radius = Math.random() * 1.2 + 0.4; 
                const x = Math.random() * (scaledWidth - radius * 2) + radius;
                const y = Math.random() * (scaledHeight - radius * 2) + radius;
                const color = `rgba(248, 200, 220, ${Math.random() * 0.4 + 0.25})`; 
                stars.push(new Star(x, y, radius, color));
            }
        }
        function connectStars() { 
            for (let i = 0; i < stars.length; i++) {
                for (let j = i + 1; j < stars.length; j++) {
                    const dist = Math.hypot(stars[i].x - stars[j].x, stars[i].y - stars[j].y);
                    if (dist < connectDistance) {
                        ctx.beginPath();
                        ctx.moveTo(stars[i].x, stars[i].y);
                        ctx.lineTo(stars[j].x, stars[j].y);
                        ctx.strokeStyle = `rgba(224, 187, 228, ${ (1 - dist / connectDistance) * 0.7 })`; 
                        ctx.lineWidth = 0.25;
                        ctx.stroke();
                    }
                }
            }
        }
        
        let animationFrameIdConstellation;
        function animateConstellation() {
            animationFrameIdConstellation = requestAnimationFrame(animateConstellation);
            ctx.clearRect(0, 0, constellationCanvas.width, constellationCanvas.height); 
            stars.forEach(star => star.update());
            connectStars();
        }

        const heroSectionForMouse = document.getElementById('hero');
        if (heroSectionForMouse) { 
            heroSectionForMouse.addEventListener('mousemove', (e) => {
                 const rect = constellationCanvas.getBoundingClientRect();
                 mouse.x = (e.clientX - rect.left); 
                 mouse.y = (e.clientY - rect.top);
            });
            heroSectionForMouse.addEventListener('mouseleave', () => {
                mouse.x = undefined; mouse.y = undefined;
            });
        }
        
        let resizeTimerConstellation;
        window.addEventListener('resize', () => { 
            clearTimeout(resizeTimerConstellation);
            resizeTimerConstellation = setTimeout(() => {
                if(animationFrameIdConstellation) cancelAnimationFrame(animationFrameIdConstellation);
                resizeCanvas();
                animateConstellation();
            }, 250);
        });
        
        if (document.readyState === 'complete') {
            resizeCanvas();
            animateConstellation();
        } else {
            window.addEventListener('load', () => {
                resizeCanvas();
                animateConstellation();
            });
        }
    }
    */

    // --- Wellness Orb, ScrollToTop, Nav Logic, Intersection Observer, Ripple, FAQ, Footer Year, Smooth Scroll ---
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
    
    // --- Wellness Orb DISABLED FOR PERFORMANCE. 
    /*
    This script was causing the "Forced Reflow" error.
    Keep it commented out to maintain a high PageSpeed score.

    if (wellnessOrb && !isTouchDevice) { 
        wellnessOrb.style.display = 'block';
        document.body.classList.add('hide-native-cursor');
        let orbTimeout, clickTimeout;

        window.addEventListener('mousemove', (e) => {
            wellnessOrb.style.left = e.clientX + 'px';
            wellnessOrb.style.top = e.clientY + 'px';
            
            wellnessOrb.classList.add('active');
            clearTimeout(orbTimeout);
            orbTimeout = setTimeout(() => wellnessOrb.classList.remove('active'), 150);
        });

        document.addEventListener('mousedown', () => { wellnessOrb.classList.add('clicking'); });
        document.addEventListener('mouseup', () => {
            clearTimeout(clickTimeout);
            clickTimeout = setTimeout(() => wellnessOrb.classList.remove('clicking'), 100);
        });
        
        document.querySelectorAll('a, button, input[type="submit"], .section-card, .service-item, .testimonial-item, .faq-question, p, h1, h2, h3, h4, h5, h6, li, strong, span').forEach(el => {
            el.addEventListener('mouseenter', () => {
                if (el.matches('a:not(.logo-main-header)') || el.matches('button') || el.matches('input[type="submit"]') || el.matches('.faq-question')) {
                    wellnessOrb.classList.add('hovering-link');
                } else if (el.matches('.section-card') || el.matches('.service-item') || el.matches('.testimonial-item')) {
                    wellnessOrb.classList.add('hovering-card');
                } else if (el.matches('p') || el.matches('h1') || el.matches('h2') || el.matches('h3') || el.matches('li') || el.matches('strong')) {
                    wellnessOrb.classList.add('hovering-text');
                }
            });
            el.addEventListener('mouseleave', () => {
                wellnessOrb.classList.remove('hovering-link', 'hovering-card', 'hovering-text');
            });
        });
    }
    */

    if (scrollToTopBtn) { 
        window.addEventListener('scroll', () => {
            scrollToTopBtn.classList.toggle('visible', window.pageYOffset > 400);
        });
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    if (mainNav) { 
        window.addEventListener('scroll', () => {
            mainNav.classList.toggle('scrolled', window.scrollY > 70);
        });
    }

    const observerOptions = { 
        root: null,
        threshold: window.innerWidth <= 768 ? 0.06 : 0.1, 
        rootMargin: window.innerWidth <= 768 ? "-20px 0px -50px 0px" : "-60px 0px -90px 0px"
    };
    const sectionObserver = new IntersectionObserver((entries, observer) => { 
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                let currentId = entry.target.id;
                navLinks.forEach(link => {
                    link.classList.toggle('active', link.getAttribute('href').substring(1) === currentId);
                });

                const staggerParents = entry.target.querySelectorAll('.stagger-animate');
                staggerParents.forEach(parent => {
                    const staggerChildren = parent.querySelectorAll('.stagger-child');
                    staggerChildren.forEach((child, index) => {
                        child.style.transitionDelay = `${index * 0.12 + 0.15}s`; 
                    });
                });
            }
        });
    }, observerOptions);
    
    sections.forEach(section => { 
        sectionObserver.observe(section);
        const lists = section.querySelectorAll('ul'); 
        lists.forEach(list => {
            list.classList.add('stagger-animate');
            list.querySelectorAll('li').forEach(li => li.classList.add('stagger-child'));
        });
        const journeyMap = section.querySelector('.journey-map');
        if (journeyMap) {
            journeyMap.classList.add('stagger-animate'); 
            journeyMap.querySelectorAll('.journey-milestone').forEach(m => m.classList.add('stagger-child'));
        }
         const faqContainer = section.querySelector('.faq-items-container'); 
         if (faqContainer) {
            faqContainer.classList.add('stagger-animate');
            faqContainer.querySelectorAll('.faq-item').forEach(item => item.classList.add('stagger-child'));
         }
    });

    navLinks.forEach(link => { 
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navHeight = mainNav ? mainNav.offsetHeight : 0;
                let extraOffset = 30; 
                if (targetId === '#hero') extraOffset = 0; 
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight - extraOffset;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
            if (mainNavUl && mainNavUl.classList.contains('open')) {
                mainNavUl.classList.add('closing'); 
                mainNavUl.addEventListener('animationend', () => {
                    mainNavUl.classList.remove('open', 'closing');
                    if (menuToggleBtn) menuToggleBtn.innerHTML = '☰';
                    if (menuToggleBtn) menuToggleBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }, { once: true });
            }
        });
    });
    
    if (menuToggleBtn && mainNavUl) { 
        menuToggleBtn.addEventListener('click', () => {
            if (mainNavUl.classList.contains('open')) {
                mainNavUl.classList.add('closing');
                let closed = false;
                const closeMenu = () => {
                    if (closed) return;
                    closed = true;
                    mainNavUl.classList.remove('open', 'closing');
                    menuToggleBtn.innerHTML = '☰';
                    menuToggleBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                };
                mainNavUl.addEventListener('animationend', closeMenu, {once: true});
                // Fallback: force close after 500ms if animationend doesn't fire
                setTimeout(closeMenu, 500);
            } else {
                mainNavUl.classList.remove('closing'); 
                mainNavUl.classList.add('open');
                menuToggleBtn.innerHTML = '×';
                menuToggleBtn.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
            }
        });
    }
    window.addEventListener('resize', () => { 
        if (window.innerWidth > 768) {
            if (mainNavUl && mainNavUl.classList.contains('open')) {
                mainNavUl.classList.remove('open', 'closing');
                if(menuToggleBtn) menuToggleBtn.innerHTML = '☰';
                if(menuToggleBtn) menuToggleBtn.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        }
    });

    function createRipple(event) { 
        const button = event.currentTarget;
        const existingRipple = button.querySelector(".ripple");
        if (existingRipple) existingRipple.remove();

        const circle = document.createElement("span");
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        circle.style.width = circle.style.height = `${diameter}px`;
        const rect = button.getBoundingClientRect();
        circle.style.left = `${event.clientX - rect.left - radius}px`;
        circle.style.top = `${event.clientY - rect.top - radius}px`;
        circle.classList.add("ripple");
        button.appendChild(circle);
        setTimeout(() => circle.remove(), 850);
    }
    document.querySelectorAll('.cta-button, .whatsapp-button, .faq-question').forEach(button => { 
        button.addEventListener("click", createRipple);
    });

    document.querySelectorAll('.faq-item').forEach(item => { 
        const questionButton = item.querySelector('.faq-question');
        questionButton.addEventListener('click', () => {
            item.classList.toggle('active');
            questionButton.setAttribute('aria-expanded', item.classList.contains('active'));
        });
    });

    if (currentYearSpan) { 
         currentYearSpan.textContent = new Date().getFullYear();
    }

    document.querySelectorAll('a[href^="#"]:not(#mainNav ul li a)').forEach(anchor => { 
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.length > 1 && document.querySelector(href)) {
                e.preventDefault();
                const targetElement = document.querySelector(href);
                const navHeight = mainNav ? mainNav.offsetHeight : 0;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight - 30;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
        });
    });
});