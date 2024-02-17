// footer_script.js

window.addEventListener('scroll', function() {
    var footer = document.querySelector('footer');
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight) {
      footer.style.display = 'block';
    } else {
      footer.style.display = 'none';
    }
  });
  