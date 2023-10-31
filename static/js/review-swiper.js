const swiper = new Swiper(".swiper", {
  direction: 'horizontal',
  autoplay: {
    delay: 5000,
    disableOnInteraction: false
  },
  layLoading: true,
  slidesPerView: 3,

  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});
