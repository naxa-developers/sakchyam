function CustomJs() {
  $('.ls-toggle-btn').on('click', function () {
    $('body').toggleClass('ls-toggle-menu');
    $('.menu ').css('overflow', 'initial');
  }),
    $('.mobile_menu').on('click', function () {
      $('.sidebar').toggleClass('open');
    });
}

function preloader() {
  $(document).ready(function () {
    $('#sakchyam-preloader').fadeOut();
  });
}
preloader();
$winHeight = $(window).innerHeight();
$headerHeight = $('.sakchyam-header').height();
$btnmenuHeight = $('.btn-menu').height();
$menuHeight = $winHeight - $headerHeight + $btnmenuHeight;
$('.menu').css({ 'max-height': $menuHeight - 50 });

function dropdownMenu() {
  $('.ml-menu').hide();
  //stores the total number of indicated classes(in this case , hidden paragraph titles) in the variable 'numberOfDesc'
  var numberOfSubmenu = $('.menu-toggle').length;
  //initiates the 'while loop' inidicated below
  var i = 0;
  //start while loop
  while (i <= numberOfSubmenu) {
    function dropdown(i) {
      $('.menu-toggle')
        .eq(i)
        .click(function () {
          //this closes any paragraph that might be open. can be seen as default behaviour.
          $('.ml-menu').slideUp();
          $('.menu-toggle').removeClass('toggled');

          // opens paragraph (if it's closed) with equivalent index to clicked '.submenu'
          if ($('.ml-menu').eq(i).is(':hidden')) {
            $('.ml-menu').eq(i).slideDown('slow');
            $(this).addClass('toggled');
          } else {
            // hides paragraph if its visible
            $('.ml-menu').eq(i).slideUp();
          }
        });
    }
    dropdown(i);
    i++; //repeats the task till last declared index
  }
}
dropdownMenu();

$('.program-footer a').on('click', function (e) {
  e.preventDefault();
  $(this).closest('.sakchyam-program').find('.hide-details').slideToggle('300');
});

$(window).on('scroll', function () {
  if ($(window).scrollTop() > 50) {
    $('.sakchyam-header').addClass('fixed');
  } else {
    $('.sakchyam-header').removeClass('fixed');
  }
});
function tableAction() {
  var actionUl = $('.table-action ul');
  $('.table-action a.more-action').on('click', function (e) {
    e.preventDefault();
    $(this).closest('.table-action').find('ul').slideToggle(200);
    $(this).closest('.table-responsive').css('overflow-y', 'initial');
  });
  $(document).mouseup(function (e) {
    if (
      !actionUl.is(e.target) && // if the target of the click isn't the actionUl...
      actionUl.has(e.target).length === 0
    ) {
      // ... nor a descendant of the actionUl
      actionUl.hide();
    }
  });
}
tableAction();

$(function () {
  'use strict';
  CustomJs();
});
