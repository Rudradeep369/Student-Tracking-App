// banner Icon animation

document.getElementById('exploreClassesBtn').addEventListener('click', function() {
    var socialIcons = document.getElementById('socialMediaIcons');
    if (socialIcons.classList.contains('d-none')) {
      socialIcons.classList.remove('d-none');

      // Add animation class to each button with staggered delay
      var buttons = document.querySelectorAll('.social-btn');
      buttons.forEach(function(btn, index) {
        btn.style.animationDelay = (index * 0.2) + 's';
      });
    } else {
      socialIcons.classList.add('d-none');
    }
  });

//   -----------

