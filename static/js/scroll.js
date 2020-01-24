$(document).ready(function() {
  $(window).scroll(function() {
    if ($(this).scrollTop() > 0) {
      $('nav').css('background-color', '#FFF');
      $('nav').css('opacity', 0.7);
    } else {
      $('nav').css('background', 'none');
    }
  });
});
