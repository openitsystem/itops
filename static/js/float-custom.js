/*
 * 
 * Template js
 */

$(document).ready(function () {
    //Left nav scroll
    $(".nano").nanoScroller();

    // Left menu collapse
    $('.left-nav-toggle a').on('click', function (event) {
        event.preventDefault();
        $("body").toggleClass("nav-toggle");
    });
 // Left menu collapse
    $('.right-sidebar-toggle').on('click', function (event) {
        event.preventDefault();
        $("#right-sidebar-toggle").toggleClass("right-sidebar-toggle");
    });
//metis menu
    $("#menu").metisMenu();
    //slim scroll
    $('.scrollDiv').slimScroll({
        color: '#eee',
        size: '5px',
        height: '250px',
        alwaysVisible: false
    });
//tooltip popover
 $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();
});
