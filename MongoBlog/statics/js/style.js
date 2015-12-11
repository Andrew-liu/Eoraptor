$('.nav__button').on('click',function(){
  $('.nav').toggleClass('is-expanded');
  $('.nav__items').toggleClass('is-fading-up'); 
});

$('#fullpage').fullpage();