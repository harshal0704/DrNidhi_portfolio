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
    let preloaderFaded = false;
    const fadeOutPreloader = () => {
        if (preloaderFaded) return;
        preloaderFaded = true;
        
        if (preloader) {
            if (gsapAvailable) {
                gsap.to(preloader, {
                    opacity: 0,
                    duration: 0.6,
                    ease: 'power2.out',
                    onComplete: () => {
                        preloader.style.visibility = 'hidden';
                        preloader.style.display = 'none';
                        preloader.classList.add('loaded');
                        document.body.classList.add('page-loaded');
                        playEntranceAnimations();
                    }
                });
            } else {
                preloader.style.opacity = '0';
                preloader.style.transition = 'opacity 0.6s ease';
                setTimeout(() => {
                    preloader.style.visibility = 'hidden';
                    preloader.style.display = 'none';
                    preloader.classList.add('loaded');
                    document.body.classList.add('page-loaded');
                    playEntranceAnimations();
                }, 600);
            }
        } else {
            playEntranceAnimations();
        }
    };

    // Trigger preloader fade-out 400ms after DOM is ready
    setTimeout(fadeOutPreloader, 400);

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
            text: 'Dear sister, when the body feels stressed and out of cycle, Vata dosha is often seeking grounding. Focus on warm, cooked meals, daily self-massage (Abhyanga) with warm sesame oil, and gentle breathing. I approach hormonal health by soothing the nervous system first, helping your body rediscover its natural, rhythmic flow. You are not alone on this path.'
        },
        'AB': {
            title: 'Nourishment for Rhythm',
            text: 'When cycles are irregular and stress is high, your endocrine system needs deep replenishment. Focus on nourishing herbs like Ashwagandha and Shatavari, and sip warm spiced almond milk. We will work together to build your Ojas (vital energy) and stabilize hormonal patterns gently.'
        },
        'AC': {
            title: 'Cooling Calm',
            text: 'If stress is accompanied by heat or emotional swings, Pitta is rising. Soothe your fire with coconut water, meditation, and cooling herbs like Shatavari or aloe vera. We will guide your system to release accumulated tension and restore a peaceful inner climate.'
        },
        'AD': {
            title: 'Light Flow',
            text: 'When stress leaves you feeling sluggish, we need to clear stagnation while supporting your energy. Sip warm ginger water, engage in dynamic stretching, and focus on warm, light meals. Our path will focus on clearing blockages to let your life-force flow freely.'
        },
        'BA': {
            title: 'Calm Fertility Prep',
            text: 'Preparing for conception begins with calming the mind and grounding the body. A peaceful womb (Garbhashaya) is created through a calm nervous system. Focus on gentle yoga, sweet-grounding foods, and slowing down. Let us co-create a peaceful sanctuary for your future child.'
        },
        'BB': {
            title: 'Nurturing Preconception (Beej Shuddhi)',
            text: 'Conscious conception is like preparing fertile soil for a seed. Focus on nutrient-dense foods (ghee, dates, almonds, fresh organic milk) to purify the reproductive tissues (Shukra Dhatu). We will craft a tailored Beej Shuddhi (cleansing and strengthening) protocol to welcome new life with vibrant vitality.'
        },
        'BC': {
            title: 'Cooling & Nurturing',
            text: 'If you feel fatigued but also warm or irritable, we must cool the reproductive channels while nourishing them. Use rose water sprays, cooling herbs, and sweet fruits. We will focus on soothing any inflammation in the reproductive system to create a welcoming, temperate environment.'
        },
        'BD': {
            title: 'Energy & Revitalization',
            text: 'To welcome new life, we must clear away sluggishness (Ama) and awaken your reproductive vitality. Focus on warm herbal teas, light spices (cardamom, fennel), and moderate movement. We will focus on awakening your body\'s innate wisdom and vitality.'
        },
        'CA': {
            title: 'Graceful Transitions (Calm & Ground)',
            text: 'Menopause is the sacred transition into a time of wisdom. When hot flashes and mood shifts arise, Vata and Pitta are fluctuating. Focus on grounding routines, cooling pranayama (Sheetali), and self-compassion. I am here to help you navigate this transition with grace, using herbs that cool the fire and ground the wind.'
        },
        'CB': {
            title: 'Nourishing the Wise Self',
            text: 'During life\'s major transitions, our vital reserves can feel depleted. Replenish your tissues with warm, moist foods, healthy fats like ghee, and adaptogenic herbs like Ashwagandha. We will design a program to preserve your bone health, skin luster, and vital juices.'
        },
        'CC': {
            title: 'Cooling the Fire',
            text: 'When hot flashes and irritability dominate, Pitta is seeking release. Avoid spicy, sour, and fermented foods. Embrace cooling coconut, coriander infusions, and quiet reflection. We will work to clear excess heat from your blood (Rakta) and liver, cooling your body and mind.'
        },
        'CD': {
            title: 'Lightness in Transition',
            text: 'If menopause makes you feel heavy, sluggish, or bloated, we need to gently kindle your digestive fire (Agni) without overheating it. Use mild spices like cumin and fennel, and enjoy warm, easily digestible meals. We will support your metabolism and clear accumulation during this shift.'
        },
        'DA': {
            title: 'Calming Detox',
            text: 'When feeling heavy, we must cleanse gently without depleting your nervous system. Sip warm water with lemon, practice gentle movement, and prioritize deep rest. We will focus on a gentle, soothing detoxification that clears toxins while leaving you feeling secure and grounded.'
        },
        'DB': {
            title: 'Nourishing Revitalization',
            text: 'If you feel sluggish and depleted, simple fasting or harsh detox will only exhaust you. We need Shodhana (gentle clearing) followed by immediate Rasayana (rejuvenation). Focus on warm mung soup, light spices, and restful sleep. Let us design a path that cleanses your body while restoring deep strength.'
        },
        'DC': {
            title: 'Cooling Release',
            text: 'If sluggishness is paired with acidity or skin rashes, toxins are mixed with heat. Cleanse with cooling green juices, cucumber, mint, and bitter herbs. We will focus on purifying the blood and liver, clearing sluggishness while cooling your entire system.'
        },
        'DD': {
            title: 'Awakening & Rejuvenation',
            text: 'Feeling heavy and sluggish suggests the presence of Ama (undigested metabolic toxins) and elevated Kapha. Kindle your digestive fire with dry ginger, black pepper, and warm foods. Engage in active, energizing exercise. We will design a custom home-cleanse to revitalize your metabolism and restore your light, joyful nature.'
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
                            menuToggleBtn.innerHTML = '☰';
                            menuToggleBtn.setAttribute('aria-expanded', 'false');
                            document.body.style.overflow = '';
                        }
                    });
                } else {
                    mainNavUl.classList.remove('open');
                    menuToggleBtn.innerHTML = '☰';
                    menuToggleBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            } else {
                mainNavUl.classList.add('open');
                menuToggleBtn.innerHTML = '×';
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

    // --- Mobile navigation links close menu ---
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetEl = document.querySelector(targetId);
            
            if (mainNavUl.classList.contains('open')) {
                mainNavUl.classList.remove('open');
                menuToggleBtn.innerHTML = '☰';
                menuToggleBtn.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }

            if (targetEl) {
                const navHeight = mainNav ? mainNav.offsetHeight : 0;
                const offset = targetId === '#hero' ? 0 : 30;
                if (lenis) {
                    lenis.scrollTo(targetEl, { offset: -(navHeight + offset) });
                } else {
                    const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight - offset;
                    window.scrollTo({ top: targetPosition, behavior: 'smooth' });
                }
            }
        });
    });

    // --- General Smooth Links Scroll (not in nav) ---
    document.querySelectorAll('a[href^="#"]:not(#mainNav ul li a)').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const href = anchor.getAttribute('href');
            if (href.length > 1 && document.querySelector(href)) {
                e.preventDefault();
                const targetEl = document.querySelector(href);
                const navHeight = mainNav ? mainNav.offsetHeight : 0;
                if (lenis) {
                    lenis.scrollTo(targetEl, { offset: -(navHeight + 30) });
                } else {
                    const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight - 30;
                    window.scrollTo({ top: targetPosition, behavior: 'smooth' });
                }
            }
        });
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