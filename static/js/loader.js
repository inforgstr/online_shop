$(function () {
  $(".order-item").slice(0, 3).show();
  $("body").on("click touchstart", ".load-more", function (e) {
    e.preventDefault();
    $(".order-item:hidden").slice(0, 3).slideDown();
    if ($(".order-item:hidden").length == 0) {
      $(".load-more").css("visibility", "hidden");
    }
    $("html,body").animate(
      {
        scrollTop: $(this).offset().top,
      },
      1000
    );
  });
});
