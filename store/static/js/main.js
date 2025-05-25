document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle'); // Will add this ID to the hamburger button
    const mainNav = document.getElementById('mainNav'); // Will add this ID to the nav ul

    if (navToggle && mainNav) {
        navToggle.addEventListener('click', function() {
            mainNav.classList.toggle('nav-open');
            // Optional: Animate hamburger icon itself
            navToggle.classList.toggle('is-active'); 
        });
    }

    // Mobile "Catégories" Accordion
    const categoryToggleMobile = document.querySelector('.nav-mobile-category-toggle'); 
    
    if (categoryToggleMobile) {
        const categoryDropdownContentMobile = categoryToggleMobile.nextElementSibling; 

        if (categoryDropdownContentMobile && categoryDropdownContentMobile.classList.contains('dropdown-content')) {
            categoryToggleMobile.addEventListener('click', function(event) {
                event.preventDefault(); 
                
                const parentLi = categoryToggleMobile.closest('.dropdown'); // Use closest to find parent .dropdown
                if (parentLi) { // Check if parentLi exists
                    parentLi.classList.toggle('is-open');

                    // Get the actual dropdown content again, in case structure is nested
                    const actualDropdownContent = parentLi.querySelector('.dropdown-content');
                    if (actualDropdownContent) {
                        if (parentLi.classList.contains('is-open')) {
                            actualDropdownContent.style.maxHeight = actualDropdownContent.scrollHeight + "px";
                            actualDropdownContent.style.opacity = '1';
                            actualDropdownContent.style.visibility = 'visible';
                        } else {
                            actualDropdownContent.style.maxHeight = '0';
                            actualDropdownContent.style.opacity = '0';
                            setTimeout(() => {
                                if (!parentLi.classList.contains('is-open')) { // Double check state before hiding
                                    actualDropdownContent.style.visibility = 'hidden';
                                }
                            }, 300); 
                        }
                    }
                }
            });
        }
    }

    // Intersection Observer for Scroll Animations
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target); // Optional: stop observing once visible
                }
            });
        }, {
            threshold: 0.1 // Trigger when 10% of the element is visible
        });

        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
});
