function CustomJs() {
    $(".ls-toggle-btn").on("click", function () {
        $("body").toggleClass("ls-toggle-menu");
        $('.menu ').css('overflow', 'initial');
    }),
        $(".mobile_menu").on("click", function () {
            $(".sidebar").toggleClass("open")
        });

};

// function checkStatuForResize (a) {
//     var b = $("body"),
//         c = $(".navbar .navbar-header .bars"),
//         d = b.width();
//     a && b.find(".page-wrapper, .sidebar").addClass("no-animate").delay(1e3).queue(function() {
//         $(this).removeClass("no-animate").dequeue()
//     }), d < 1170 ? (d > 767 && b.addClass("ls-toggle-menu"), b.addClass("ls-closed"), c.fadeIn()) : (b.removeClass("ls-closed ls-toggle-menu"), c.fadeOut())
// };
// checkStatuForResize();


// $(window).on('resize',function(){
//     function checkStatuForResize (a) {
//         var b = $("body"),
//             c = $(".navbar .navbar-header .bars"),
//             d = b.width();
//         a && b.find(".page-wrapper, .sidebar").addClass("no-animate").delay(1e3).queue(function() {
//             $(this).removeClass("no-animate").dequeue()
//         }), d < 1170 ? (d > 767 && b.addClass("ls-toggle-menu"), b.addClass("ls-closed"), c.fadeIn()) : (b.removeClass("ls-closed ls-toggle-menu"), c.fadeOut())
//     };
//     checkStatuForResize();
// })

// $('.menu .list li a.menu-toggle').on('click', function (e) {
//     e.preventDefault();
//     // $("body").addClass("ls-toggle-menu");

//     if ($(this).closest('li').next().hasClass('submenu')) {
//         $('.menu .list li').removeClass('submenu');
//     } else {
//         $('.menu .list li').removeClass('submenu');
//     }
//     $(this).closest('li').toggleClass('submenu');
// });

function dropdownMenu(){
    $('.ml-menu').hide();
    //stores the total number of indicated classes(in this case , hidden paragraph titles) in the variable 'numberOfDesc'
    var numberOfSubmenu = $('.menu-toggle').length; 
    //initiates the 'while loop' inidicated below
    var i = 0;
    //start while loop
    while(i <= numberOfSubmenu) {
      function dropdown(i) {
          $('.menu-toggle').eq(i).click(function () {
              //this closes any paragraph that might be open. can be seen as default behaviour.
              $('.ml-menu').slideUp();
              $('.menu-toggle').removeClass('toggled');
              
              // opens paragraph (if it's closed) with equivalent index to clicked '.submenu'
              if($('.ml-menu').eq(i).is(':hidden')){
                  $('.ml-menu').eq(i).slideDown("slow");
                  $(this).addClass('toggled');
              } else {
                  // hides paragraph if its visible
                  $('.ml-menu').eq(i).slideUp();
              }        
          });
      }  
      dropdown(i);
      i++;  //repeats the task till last declared index
    }
  }
  dropdownMenu();

$('.program-footer a').on('click', function (e) {
    e.preventDefault();
    $(this).closest('.sakchyam-program').find('.hide-details').slideToggle('300');
});

// function checkbox(){
//     $(".checklist-header .custom-control-input").change(function () {
//       $(this).closest('.checklist-card').find('.custom-checkbox input').prop('checked', $(this).prop("checked"));
//       $(this).closest('.checklist-header').toggleClass('active');
//       $(this).closest('.checklist-card').find('ul').slideToggle(300);
//     });

//     $(".checklist-card .custom-checkbox input").change(function() {
//         var checkboxes = $(this).closest('.custom-checkbox').find('input');
//         var checkedboxes = checkboxes.filter(':checked');

//         if(checkboxes.length === checkedboxes.length) {
//         $(this).closest('.checklist-header').find('.custom-checkbox input').prop('checked', true);

//         } else {
//           $(this).closest('.checklist-header').find('.custom-checkbox input').prop('checked', false);
//         }
//     });
//   };
//   checkbox();
//   function tableAction (){
//     $('.table-action a.more-action').on('click',function(e){
//         e.preventDefault();
//         $(this).closest('.table-action ').find('ul').slideToggle(200);
//     })
//   }
//   tableAction();
//   function minHeight (){
//     var programmeHeight = $('.sakchyam-program .program-info').innerHeight();
//     $('.sakchyam-program .about-program').css({'min-height': programmeHeight});
//     var winWidth = $( window ).width();
//     if(winWidth <= 767){
//         $('.sakchyam-program .about-program').css({'min-height': 'auto'});
//     }
//   }
//   minHeight();

$(window).on('scroll', function () {
    if ($(window).scrollTop() > 50) {
        $('.sakchyam-header').addClass('fixed');
    } else {
        $('.sakchyam-header').removeClass('fixed');
    }
})
function tableAction() {
    var actionUl = $('.table-action ul');
    $('.table-action a.more-action').on('click', function (e) {
        e.preventDefault();
        $(this).closest('.table-action').find('ul').slideToggle(200);
        $(this).closest('.table-responsive').css('overflow-y', 'initial');
        
    });
    $(document).mouseup(function (e) { 
        if (!actionUl.is(e.target) // if the target of the click isn't the actionUl...
            && actionUl.has(e.target).length === 0) // ... nor a descendant of the actionUl
        {
            actionUl.hide();
        } 
    }); 
    

}
tableAction();




$(function () {
    "use strict";
    CustomJs()
});

