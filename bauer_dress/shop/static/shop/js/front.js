$(function () {


    /* ===============================================================
         LIGHTBOX
      =============================================================== */
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    });


    /* ===============================================================
         PRODUCT SLIDER
      =============================================================== */
      $('.owl-carousel-product').owlCarousel({
          loop:true,
          margin:10,
          responsiveClass:true,
          lazyLoad:true,
          responsive:{
              0:{
                  items:1,
                  nav:false
              },
              600:{
                  items:1,
                  nav:false
              },
              1000:{
                  items:1,
                  nav:false,
                  loop:false
              }
          }
      });


    /* ===============================================================
         PRODUCT QUANTITY
      =============================================================== */
      $('.dec-btn').click(function () {
          var siblings = $(this).siblings('input');
          if (parseInt(siblings.val(), 10) >= 1) {
              siblings.val(parseInt(siblings.val(), 10) - 1);
          }
      });

      $('.inc-btn').click(function () {
          var siblings = $(this).siblings('input');
          siblings.val(parseInt(siblings.val(), 10) + 1);
      });


      /* ===============================================================
           BOOTSTRAP SELECT
        =============================================================== */
      $('.selectpicker').on('change', function () {
          $(this).closest('.dropdown').find('.filter-option-inner-inner').addClass('selected');
      });



      /* ===============================================================
           DISABLE UNWORKED ANCHORS
        =============================================================== */
      $('a[href="#"]').on('click', function (e) {
         e.preventDefault();
      });

});



$('.size-slider').owlCarousel({
    margin:8,
    loop:false,
    autoWidth:true,
    items:4
});



// $('.owl-carousel-product').owlCarousel({
//     loop:true,
//     margin:10,
//     responsiveClass:true,
//     responsive:{
//         0:{
//             items:1,
//             nav:false
//         },
//         600:{
//             items:1,
//             nav:false
//         },
//         1000:{
//             items:1,
//             nav:false,
//             loop:false
//         }
//     }
// });