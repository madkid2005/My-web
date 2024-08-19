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

// Smooth scrolling for internal links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        // Check if the href attribute is valid and the hash exists in the document
        if (this.hash && document.querySelector(this.hash)) {
            e.preventDefault();  // Prevent default anchor click behavior
            const hash = this.hash;
            // Scroll to the element smoothly
            document.querySelector(hash).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Change navbar background on scroll
window.onscroll = function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {  // Ensure the navbar element is found
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = '#f8f9fa';
        } else {
            navbar.style.backgroundColor = '#ffffff';
        }
    }
};
