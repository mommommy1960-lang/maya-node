// MayaNode Webflow Export - Main JavaScript
// Smooth scroll interactions and animations

(function() {
  'use strict';
  
  // Navbar scroll effect
  function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }
  
  // Mobile menu toggle
  function initMobileMenu() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.nav-menu');
    
    if (!toggle || !menu) return;
    
    toggle.addEventListener('click', function() {
      menu.classList.toggle('active');
      
      // Animate toggle button
      const spans = toggle.querySelectorAll('span');
      if (menu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translateY(8px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
      } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
      }
    });
    
    // Close menu when clicking a link
    const navLinks = menu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        menu.classList.remove('active');
        const spans = toggle.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
      });
    });
  }
  
  // Mobile dropdown toggle
  function initMobileDropdowns() {
    if (window.innerWidth <= 768) {
      const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
      
      dropdownItems.forEach(item => {
        const link = item.querySelector('.nav-link');
        link.addEventListener('click', function(e) {
          e.preventDefault();
          item.classList.toggle('active');
        });
      });
    }
  }
  
  // Scroll reveal animation
  function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');
    
    if (!reveals.length) return;
    
    const revealOnScroll = function() {
      const windowHeight = window.innerHeight;
      const revealPoint = 150;
      
      reveals.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        
        if (elementTop < windowHeight - revealPoint) {
          element.classList.add('active');
        }
      });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Run on load
  }
  
  // Smooth scroll to anchor links
  function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
      link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const offsetTop = target.offsetTop - 80; // Account for fixed navbar
          
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  }
  
  // Form validation (basic)
  function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
          if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#ff4444';
          } else {
            field.style.borderColor = '';
          }
        });
        
        if (!isValid) {
          e.preventDefault();
          alert('Please fill in all required fields.');
        }
      });
    });
  }
  
  // Fade in elements on page load
  function initPageLoad() {
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-up');
    fadeElements.forEach((element, index) => {
      setTimeout(() => {
        element.style.opacity = '1';
      }, index * 100);
    });
  }
  
  // Volume I chapter navigation
  function initChapterNav() {
    const chapterLinks = document.querySelectorAll('.chapter-link');
    
    chapterLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        // Remove active class from all links
        chapterLinks.forEach(l => l.classList.remove('active'));
        // Add active class to clicked link
        this.classList.add('active');
      });
    });
  }
  
  // Initialize all functions when DOM is loaded
  document.addEventListener('DOMContentLoaded', function() {
    initNavbarScroll();
    initMobileMenu();
    initMobileDropdowns();
    initScrollReveal();
    initSmoothScroll();
    initFormValidation();
    initPageLoad();
    initChapterNav();
  });
  
  // Handle window resize
  let resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      initMobileDropdowns();
    }, 250);
  });
  
})();
