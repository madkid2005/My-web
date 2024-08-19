// massage js 

// Automatically close the message after 3 seconds (3000 milliseconds)
setTimeout(function() {
    var messageDivs = document.querySelectorAll('.messages .alert');
    messageDivs.forEach(function(div) {
        div.classList.add('fade-out'); // Start the fade-out effect
        setTimeout(function() {
            div.style.display = 'none'; // Hide the element after the fade-out
        }, 500); // Wait for the fade-out transition to complete
    });
}, 3000);

// navbar js

// Smooth scrolling for internal links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        if (this.hash !== "") {
            e.preventDefault();
            const hash = this.hash;
            document.querySelector(hash).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Change navbar background on scroll
window.onscroll = function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = '#f8f9fa';
    } else {
        navbar.style.backgroundColor = '#ffffff';
    }
};
