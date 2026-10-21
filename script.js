// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Elements ---
    const preloader = document.getElementById('preloader');
    const mainNav = document.getElementById('mainNav');
    const menuToggleBtn = document.querySelector('.menu-toggle');
    const mainNavUl = mainNav.querySelector('ul');
    const navLinks = document.querySelectorAll('#mainNav ul li a');
    const sections = document.querySelectorAll('main section, header.hero');
    const currentYearSpan = document.getElementById('currentYear');
    const scrollToTopBtn = document.getElementById('scrollToTopBtn');

    // --- GSAP and ScrollTrigger Safeties ---
    const gsapAvailable = typeof gsap !== 'undefined';
    const scrollTriggerAvailable = typeof ScrollTrigger !== 'undefined';
    const lenisAvailable = typeof Lenis !== 'undefined';

    if (gsapAvailable && scrollTriggerAvailable) {
        gsap.registerPlugin(ScrollTrigger);
    }

    // --- Preloader Fade Out ---
    // The overlay must never outlive the page. GSAP drives the fade, but a tween
    // only advances while the tab is producing frames: a background tab, a
    // throttled device or a failed CDN would otherwise leave the visitor staring
    // at an opaque screen. So start the fade, and force-clear on a hard timer.
    let preloaderFaded = false;
    let entrancePlayed = false;

    const playEntranceOnce = () => {
        if (entrancePlayed) return;
        entrancePlayed = true;
        try {
            playEntranceAnimations();
        } catch (err) {
            /* the entrance is decorative; never let it block the page */
        }
    };

    const clearPreloader = () => {
        if (preloader) {
            preloader.style.opacity = '0';
            preloader.style.visibility = 'hidden';
            preloader.style.display = 'none';
            preloader.classList.add('loaded');
            document.body.classList.add('page-loaded');
        }
        playEntranceOnce();
    };

    const fadeOutPreloader = () => {
        if (preloaderFaded) return;
        preloaderFaded = true;

        if (!preloader) {
            playEntranceOnce();
            return;
        }

        if (!gsapAvailable) {
            preloader.style.transition = 'opacity 0.6s ease';
            preloader.style.opacity = '0';
            setTimeout(clearPreloader, 600);
            return;
        }

        try {
            gsap.to(preloader, {
                opacity: 0,
                duration: 0.6,
                ease: 'power2.out',
                onComplete: clearPreloader
            });
        } catch (err) {
            clearPreloader();
        }
    };

    // Trigger the fade 400ms after DOM is ready, and force-clear 2s after that
    // whatever the animation is doing.
    setTimeout(fadeOutPreloader, 400);
    setTimeout(clearPreloader, 2000);

    // Fallback force-clear preloader if load event fires
    window.addEventListener('load', fadeOutPreloader);

    // --- Initialize Lenis Smooth Scroll ---
    let lenis = null;
    if (lenisAvailable) {
        try {
            lenis = new Lenis({
                duration: 1.2,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                direction: 'vertical',
                gestureDirection: 'vertical',
                smooth: true,
                mouseMultiplier: 1,
                smoothTouch: false,
                touchMultiplier: 2,
                infinite: false,
            });

            function raf(time) {
                if (lenis) {
                    lenis.raf(time);
                    requestAnimationFrame(raf);
                }
            }
            requestAnimationFrame(raf);

            if (gsapAvailable && scrollTriggerAvailable) {
                lenis.on('scroll', ScrollTrigger.update);
                gsap.ticker.lagSmoothing(0);
            }
        } catch (e) {
            console.warn('Lenis scroll initialization failed. Using native scroll:', e);
            lenis = null;
        }
    }

    // --- Scroll progress bar ---
    if (gsapAvailable && scrollTriggerAvailable) {
        try {
            const progressBar = document.createElement('div');
            progressBar.className = 'scroll-progress-bar';
            progressBar.style.cssText = `
                position: fixed;
                top: 0; left: 0;
                width: 0%; height: 4px;
                background: linear-gradient(to right, var(--secondary-rose), var(--accent-gold));
                z-index: 1002;
                pointer-events: none;
            `;
            document.body.appendChild(progressBar);

            gsap.to(progressBar, {
                width: '100%',
                ease: 'none',
                scrollTrigger: {
                    trigger: 'body',
                    start: 'top top',
                    end: 'bottom bottom',
                    scrub: true
                }
            });
        } catch (e) {
            console.warn('Scroll progress bar GSAP animation failed:', e);
        }
    }

    // --- GSAP Entrance Animations ---
    function playEntranceAnimations() {
        if (!gsapAvailable) return;
        try {
            const tl = gsap.timeline();
            
            tl.from('nav', {
                y: -30,
                opacity: 0,
                duration: 0.8,
                ease: 'power3.out'
            });

            tl.from('.hero .greeting', {
                y: 30,
                opacity: 0,
                duration: 0.8,
                ease: 'power2.out'
            }, '-=0.4');

            tl.from('.hero h1', {
                y: 35,
                opacity: 0,
                duration: 0.9,
                ease: 'power3.out'
            }, '-=0.6');

            tl.from('.hero .subtitle', {
                y: 25,
                opacity: 0,
                duration: 0.8,
                ease: 'power2.out'
            }, '-=0.6');

            tl.from('.hero .cta-button', {
                scale: 0.9,
                opacity: 0,
                duration: 0.8,
                ease: 'elastic.out(1, 0.75)'
            }, '-=0.5');

            gsap.from('.glow-bubble', {
                scale: 0.5,
                opacity: 0,
                stagger: 0.2,
                duration: 3,
                ease: 'power1.out'
            });
        } catch (e) {
            console.warn('Entrance GSAP animations failed:', e);
        }
    }

    // Add stagger classes dynamically on load
    sections.forEach(section => {
        if (section.id === 'hero') return;
        
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
        
        const serviceGrid = section.querySelector('.service-grid');
        if (serviceGrid) {
            serviceGrid.classList.add('stagger-animate');
            serviceGrid.querySelectorAll('.service-item').forEach(m => m.classList.add('stagger-child'));
        }
        
        const testimonialGrid = section.querySelector('.testimonial-carousel');
        if (testimonialGrid) {
            testimonialGrid.classList.add('stagger-animate');
            testimonialGrid.querySelectorAll('.testimonial-item').forEach(m => m.classList.add('stagger-child'));
        }

        const faqContainer = section.querySelector('.faq-items-container');
        if (faqContainer) {
            faqContainer.classList.add('stagger-animate');
            faqContainer.querySelectorAll('.faq-item').forEach(m => m.classList.add('stagger-child'));
        }
    });

    // --- Native Scroll Reveal Observer ---
    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Trigger stagger transitions inside card
                const staggerParents = entry.target.querySelectorAll('.stagger-animate');
                staggerParents.forEach(parent => {
                    const staggerChildren = parent.querySelectorAll('.stagger-child');
                    staggerChildren.forEach((child, index) => {
                        child.style.transitionDelay = `${index * 0.08 + 0.12}s`;
                    });
                });
                
                observer.unobserve(entry.target); // Reveal only once
            }
        });
    }, {
        threshold: window.innerWidth <= 768 ? 0.05 : 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    sections.forEach(section => {
        if (section.id !== 'hero') {
            sectionObserver.observe(section);
        }
    });

    // --- Dynamic Journey Timeline Drawing ---
    let timelineTween = null;
    function updateTimelinePath() {
        const journeyMap = document.querySelector('.journey-map');
        const pathBg = document.querySelector('.timeline-path-bg');
        const pathActive = document.querySelector('.timeline-path-active');
        const icons = document.querySelectorAll('.milestone-icon-container');
        if (!journeyMap || !pathBg || !pathActive || icons.length === 0) return;
        
        try {
            const mapRect = journeyMap.getBoundingClientRect();
            let d = '';
            icons.forEach((icon, index) => {
                const rect = icon.getBoundingClientRect();
                const x = rect.left + rect.width / 2 - mapRect.left;
                const y = rect.top + rect.height / 2 - mapRect.top;
                if (index === 0) {
                    d += `M ${x} ${y}`;
                } else {
                    d += ` L ${x} ${y}`;
                }
            });
            
            pathBg.setAttribute('d', d);
            pathActive.setAttribute('d', d);
            
            const pathLength = pathActive.getTotalLength();
            gsap.set(pathActive, { strokeDasharray: pathLength, strokeDashoffset: pathLength });
            
            if (timelineTween) {
                timelineTween.kill();
            }
            
            if (gsapAvailable && scrollTriggerAvailable) {
                timelineTween = gsap.to(pathActive, {
                    strokeDashoffset: 0,
                    ease: 'none',
                    scrollTrigger: {
                        trigger: '.journey-map',
                        start: 'top 60%',
                        end: 'bottom 70%',
                        scrub: 1
                    }
                });
            }
        } catch (e) {
            console.warn('Journey SVG timeline drawing failed:', e);
        }
    }

    // Wait slightly to compute timeline path coordinates after layout stabilizes
    setTimeout(updateTimelinePath, 1500);

    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            updateTimelinePath();
            if (gsapAvailable && scrollTriggerAvailable) {
                ScrollTrigger.refresh();
            }
        }, 250);
    });

    // --- Wellness Compass Interactivity ---
    let bodyFeeling = null;
    let heartSeeking = null;
    
    const compassWidget = document.getElementById('compassWidget');
    const stepButtons = document.querySelectorAll('.compass-option-btn');
    const backBtn = document.querySelector('.back-btn');
    const restartBtn = document.querySelector('.restart-btn');
    const resultTitle = document.getElementById('resultTitle');
    const resultText = document.getElementById('resultText');

    const adviceMap = {
        'AA': {
            title: 'Rhythm & Calm',
            text: 'Stress and irregular periods often go together. Ayurveda reads this as Vata — the quality of movement and dryness in the body — asking to be settled down. Warm cooked meals, a daily oil massage with warm sesame oil, and slow breathing are the foundations. I usually start by calming the nervous system, because that is what the cycle responds to first.'
        },
        'AB': {
            title: 'Nourishment for Rhythm',
            text: 'When periods are irregular and stress is high, the body needs building up, not stimulating. Herbs such as Ashwagandha and Shatavari, and warm spiced almond milk, are the usual starting points. The aim is to build what Ayurveda calls Ojas — your deep reserve of energy — so your cycle steadies on its own rather than being pushed.'
        },
        'AC': {
            title: 'Cooling Calm',
            text: 'Stress that shows up as heat and mood swings usually points to Pitta being raised. Coconut water, meditation, and cooling herbs such as Shatavari or aloe vera help bring the temperature down. Expect this to feel less like pushing and more like letting go of pressure that has been building.'
        },
        'AD': {
            title: 'Light Flow',
            text: 'When stress leaves you heavy and sluggish, the aim is to clear the stagnation without depleting you. Warm ginger water, some active stretching, and light warm meals help. The goal is to get things moving again so you feel like yourself.'
        },
        'BA': {
            title: 'Calm Fertility Prep',
            text: 'Preparing to conceive starts with settling the mind and steadying the body. Ayurveda links a calm nervous system to a healthy reproductive system, so gentle yoga, nourishing foods and a slower pace all belong here. It is not a race, and the groundwork matters more than the timing.'
        },
        'BB': {
            title: 'Nurturing Preconception (Beej Shuddhi)',
            text: 'Think of it as preparing fertile soil. Good nutrition — ghee, dates, almonds, fresh milk — nourishes what Ayurveda calls Shukra Dhatu, the reproductive tissue. From there, Beej Shuddhi (cleansing and strengthening) is planned for you individually, for the three months before you try.'
        },
        'BC': {
            title: 'Cooling & Nurturing',
            text: 'Feeling tired but also warm or irritable means the reproductive system needs cooling and feeding at the same time. Rose water, cooling herbs and sweet fruits are useful, alongside less heat in the diet. This is about creating a comfortable, temperate internal environment.'
        },
        'BD': {
            title: 'Energy & Revitalization',
            text: 'Before trying to conceive, it helps to clear sluggishness first. Warm herbal teas, gentle warming spices like cardamom and fennel, and moderate movement get things going. This is usually the shortest part of preconception care, and it makes everything after it work better.'
        },
        'CA': {
            title: 'Graceful Transitions (Calm & Ground)',
            text: 'Menopause is a shift, and the symptoms you notice — hot flushes, mood swings, disturbed sleep — usually come from Vata and Pitta fluctuating. Steady routines, cooling breathing exercises (Sheetali) and a little self-compassion help. There are also herbs that cool and ground, and they are worth trying.'
        },
        'CB': {
            title: 'Nourishing the Wise Self',
            text: 'Major life stages can leave your reserves feeling thinner. Warm, moist food, healthy fats such as ghee, and adaptogenic herbs like Ashwagandha help rebuild. The aim is to protect your bone health, skin and energy for the years ahead, not just to get through the week.'
        },
        'CC': {
            title: 'Cooling the Fire',
            text: 'When hot flushes and irritability dominate, the usual starting point is to reduce what is heating you up: less spicy, sour and fermented food, and more cooling things like coconut, coriander drinks and quiet time. Ayurveda also looks at the blood and liver here, since heat often shows up in both.'
        },
        'CD': {
            title: 'Lightness in Transition',
            text: 'If menopause leaves you feeling heavy, slow or bloated, digestion usually needs gentle encouragement rather than a hard push. Mild spices like cumin and fennel, and warm meals that are easy to digest, help. Most people find the change gradual rather than sudden.'
        },
        'DA': {
            title: 'Calming Detox',
            text: 'When you feel heavy, a harsh cleanse will leave you worse. Gentle is the point: warm water with lemon, easy movement, and proper rest. The aim is to clear what has accumulated without draining your nervous system in the process.'
        },
        'DB': {
            title: 'Nourishing Revitalization',
            text: 'If you are sluggish and depleted, fasting or a harsh detox will only exhaust you further. Ayurveda pairs gentle clearing (Shodhana) with immediate rebuilding (Rasayana), in that order. Warm mung soup, light spices and proper sleep are the basics — and they are genuinely enough to start with.'
        },
        'DC': {
            title: 'Cooling Release',
            text: 'Sluggishness together with acidity or skin rashes usually means heat and stagnation together. Cooling foods like cucumber, mint and green drinks, with bitter herbs, help clear both. This pattern responds better to cooling and clearing than to stimulating.'
        },
        'DD': {
            title: 'Awakening & Rejuvenation',
            text: 'Feeling heavy and slow usually points to Ama — the residue Ayurveda associates with poor digestion — along with raised Kapha. Dry ginger, black pepper and warm food help get the digestive fire going again, and lively movement does the same for the body. Worth doing slowly, over weeks rather than days.'
        }
    };

    function transitionStep(fromStep, toStep) {
        const fromEl = compassWidget.querySelector(`.compass-step[data-step="${fromStep}"]`);
        const toEl = compassWidget.querySelector(`.compass-step[data-step="${toStep}"]`);
        
        if (fromEl) fromEl.classList.remove('active');
        if (toEl) toEl.classList.add('active');
        
        if (gsapAvailable && toEl) {
            gsap.fromTo(toEl, 
                { opacity: 0, y: 15 },
                { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out', clearProps: 'all' }
            );
        }
    }

    stepButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const stepEl = btn.closest('.compass-step');
            const stepVal = parseInt(stepEl.dataset.step);
            const choice = btn.dataset.value;

            if (stepVal === 1) {
                bodyFeeling = choice;
                transitionStep(1, 2);
            } else if (stepVal === 2) {
                heartSeeking = choice;
                showResult();
                transitionStep(2, 3);
            }
        });
    });

    if (backBtn) {
        backBtn.addEventListener('click', () => {
            transitionStep(2, 1);
        });
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', () => {
            bodyFeeling = null;
            heartSeeking = null;
            transitionStep(3, 1);
        });
    }

    function showResult() {
        const key = bodyFeeling + heartSeeking;
        const result = adviceMap[key] || adviceMap['AA'];
        
        resultTitle.textContent = result.title;
        resultText.textContent = result.text;
    }

    // --- Dinacharya Tabs Interactivity ---
    const dinacharyaTabs = document.querySelectorAll('.dinacharya-tab-btn');
    const dinacharyaPanels = document.querySelectorAll('.dinacharya-panel');
    const tabIndicatorPill = document.querySelector('.tab-indicator-pill');

    function updateTabIndicator(activeTab) {
        if (!tabIndicatorPill || !activeTab) return;
        const tabRect = activeTab.getBoundingClientRect();
        const tabsContainerRect = activeTab.parentElement.getBoundingClientRect();
        
        const leftOffset = tabRect.left - tabsContainerRect.left;
        const tabWidth = tabRect.width;
        
        tabIndicatorPill.style.width = `${tabWidth - 12}px`; // accounting for container padding
        tabIndicatorPill.style.left = `${leftOffset + 6}px`;
    }

    if (dinacharyaTabs.length > 0) {
        // Set initial tab indicator position
        setTimeout(() => {
            const activeTab = document.querySelector('.dinacharya-tab-btn.active');
            updateTabIndicator(activeTab);
        }, 500);

        dinacharyaTabs.forEach((tab) => {
            tab.addEventListener('click', () => {
                // Deactivate all tabs
                dinacharyaTabs.forEach(t => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                });
                
                // Activate clicked tab
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');
                updateTabIndicator(tab);

                // Show corresponding panel with fade transition
                const targetId = tab.getAttribute('aria-controls');
                dinacharyaPanels.forEach(panel => {
                    if (panel.id === targetId) {
                        panel.classList.add('active');
                        if (gsapAvailable) {
                            gsap.fromTo(panel, 
                                { opacity: 0, y: 15 },
                                { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out', clearProps: 'all' }
                            );
                            gsap.fromTo(panel.querySelectorAll('.practice-list li'),
                                { opacity: 0, x: -10 },
                                { opacity: 1, x: 0, stagger: 0.08, duration: 0.4, ease: 'power2.out', delay: 0.1 }
                            );
                        }
                    } else {
                        panel.classList.remove('active');
                    }
                });
            });
        });

        // Reposition pill on window resize
        let resizeIndicatorTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeIndicatorTimer);
            resizeIndicatorTimer = setTimeout(() => {
                const activeTab = document.querySelector('.dinacharya-tab-btn.active');
                updateTabIndicator(activeTab);
            }, 100);
        });
    }

    // --- Navigation Scroll Changes & Dynamic Active Class ---
    window.addEventListener('scroll', () => {
        if (window.scrollY > 70) {
            mainNav.classList.add('scrolled');
        } else {
            mainNav.classList.remove('scrolled');
        }

        let currentSection = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= (sectionTop - 120)) {
                currentSection = section.id;
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });

        if (scrollToTopBtn) {
            if (window.scrollY > 400) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        }
    });

    // --- Scroll To Top Click ---
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', () => {
            if (lenis) {
                lenis.scrollTo(0);
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // --- Mobile Navigation Toggle ---
    if (menuToggleBtn && mainNavUl) {
        menuToggleBtn.addEventListener('click', () => {
            if (mainNavUl.classList.contains('open')) {
                if (gsapAvailable) {
                    gsap.to(mainNavUl, {
                        y: -10,
                        opacity: 0,
                        duration: 0.35,
                        ease: 'power2.in',
                        onComplete: () => {
                            mainNavUl.classList.remove('open');
                            setMenuIcon(false);
                            menuToggleBtn.setAttribute('aria-expanded', 'false');
                            document.body.style.overflow = '';
                        }
                    });
                } else {
                    mainNavUl.classList.remove('open');
                    setMenuIcon(false);
                    menuToggleBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            } else {
                mainNavUl.classList.add('open');
                setMenuIcon(true);
                menuToggleBtn.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
                if (gsapAvailable) {
                    gsap.fromTo(mainNavUl, 
                        { y: -10, opacity: 0 },
                        { y: 0, opacity: 1, duration: 0.45, ease: 'power3.out' }
                    );
                }
            }
        });
    }

    // --- Shared helpers for in-page navigation ---
    // The button holds a span so the glyph can be swapped without touching the
    // accessible name.
    const setMenuIcon = (open) => {
        if (!menuToggleBtn) return;
        const icon = menuToggleBtn.querySelector('.menu-icon') || menuToggleBtn;
        icon.textContent = open ? '×' : '☰';
        menuToggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    const closeMobileMenu = () => {
        if (!mainNavUl || !mainNavUl.classList.contains('open')) return;
        mainNavUl.classList.remove('open');
        setMenuIcon(false);
        document.body.style.overflow = '';
    };

    // Resolve "#section" to an element. Returns null for anything that is not a
    // real, existing anchor - a guard, because `document.querySelector("about/")`
    // throws a SyntaxError and would kill the whole click handler.
    const resolveHash = (href) => {
        if (!href || href.charAt(0) !== '#' || href.length < 2) return null;
        try {
            return document.querySelector(href);
        } catch (err) {
            return null;
        }
    };

    const scrollToTarget = (targetEl, extraOffset) => {
        const navHeight = mainNav ? mainNav.offsetHeight : 0;
        if (lenis) {
            lenis.scrollTo(targetEl, { offset: -(navHeight + extraOffset) });
        } else {
            const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight - extraOffset;
            window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        }
    };

    // --- Navigation links ---
    // Only intercept real in-page anchors. A link to another document (writing/,
    // rss.xml, an external site) must be left alone so the browser navigates.
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            const targetEl = resolveHash(href);

            closeMobileMenu();

            if (!targetEl) return; // not an in-page anchor - let the browser handle it

            e.preventDefault();
            scrollToTarget(targetEl, href === '#hero' ? 0 : 30);
        });
    });

    // --- General Smooth Links Scroll (not in nav) ---
    document.querySelectorAll('a[href^="#"]:not(#mainNav ul li a)').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetEl = resolveHash(anchor.getAttribute('href'));
            if (!targetEl) return;
            e.preventDefault();
            scrollToTarget(targetEl, 30);
        });
    });

    // The mobile menu should also close if the viewport grows past the
    // breakpoint while it is open, otherwise the page stays scroll-locked.
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) closeMobileMenu();
    });

    // --- FAQ Accordions ---
    document.querySelectorAll('.faq-item').forEach(item => {
        const questionButton = item.querySelector('.faq-question');
        
        questionButton.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            document.querySelectorAll('.faq-item').forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
                }
            });
            
            item.classList.toggle('active', !isActive);
            questionButton.setAttribute('aria-expanded', !isActive);
        });
    });

    // --- Footer Year ---
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }
});