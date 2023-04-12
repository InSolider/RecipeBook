(function ($) {
    "use strict"; var $wrapper = $('.main-wrapper'); var $pageWrapper = $('.page-wrapper'); var $slimScrolls = $('.slimscroll'); var Sidemenu = function () { this.$menuItem = $('#sidebar-menu a'); }; function init() {
        var $this = Sidemenu; $('#sidebar-menu a').on('click', function (e) {
            if ($(this).parent().hasClass('submenu')) { e.preventDefault(); }
            if (!$(this).hasClass('subdrop')) { $('ul', $(this).parents('ul:first')).slideUp(350); $('a', $(this).parents('ul:first')).removeClass('subdrop'); $(this).next('ul').slideDown(350); $(this).addClass('subdrop'); } else if ($(this).hasClass('subdrop')) { $(this).removeClass('subdrop'); $(this).next('ul').slideUp(350); }
        }); $('#sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
    }
    init(); $('body').append('<div class="sidebar-overlay"></div>'); $(document).on('click', '#mobile_btn', function () { $wrapper.toggleClass('slide-nav'); $('.sidebar-overlay').toggleClass('opened'); $('html').addClass('menu-opened'); return false; }); $(".sidebar-overlay").on("click", function () { $wrapper.removeClass('slide-nav'); $(".sidebar-overlay").removeClass("opened"); $('html').removeClass('menu-opened'); }); if ($('.page-wrapper').length > 0) { var height = $(window).height(); $(".page-wrapper").css("min-height", height); }
    $(window).resize(function () { if ($('.page-wrapper').length > 0) { var height = $(window).height(); $(".page-wrapper").css("min-height", height); } }); if ($('.select').length > 0) { $('.select').select2({ minimumResultsForSearch: -1, width: '100%' }); }
    if ($('[data-toggle="tooltip"]').length > 0) { $('[data-toggle="tooltip"]').tooltip(); }
    if ($('.datatable').length > 0) { $('.datatable').DataTable({ "bFilter": false, }); }
    if ($('.clickable-row').length > 0) { $(document).on('click', '.clickable-row', function () { window.location = $(this).data("href"); }); }
    if ($('.proimage-thumb li a').length > 0) { var full_image = $(this).attr("href"); $(".proimage-thumb li a").click(function () { full_image = $(this).attr("href"); $(".pro-image img").attr("src", full_image); $(".pro-image img").parent().attr("href", full_image); return false; }); }
    if ($('#pro_popup').length > 0) { $('#pro_popup').lightGallery({ thumbnail: true, selector: 'a' }); }
    if ($slimScrolls.length > 0) { $slimScrolls.slimScroll({ height: 'auto', width: '100%', position: 'right', size: '7px', color: '#ccc', allowPageScroll: false, wheelStep: 10, touchScrollStep: 100 }); var wHeight = $(window).height() - 60; $slimScrolls.height(wHeight); $('.sidebar .slimScrollDiv').height(wHeight); $(window).resize(function () { var rHeight = $(window).height() - 60; $slimScrolls.height(rHeight); $('.sidebar .slimScrollDiv').height(rHeight); }); }
    $(document).on('click', '#toggle_btn', function () {
        if ($('body').hasClass('mini-sidebar')) { $('body').removeClass('mini-sidebar'); $('.subdrop + ul').slideDown(); } else { $('body').addClass('mini-sidebar'); $('.subdrop + ul').slideUp(); }
        return false;
    }); $(document).on('mouseover', function (e) {
        e.stopPropagation(); if ($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
            var targ = $(e.target).closest('.sidebar').length; if (targ) { $('body').addClass('expand-menu'); $('.subdrop + ul').slideDown(); } else { $('body').removeClass('expand-menu'); $('.subdrop + ul').slideUp(); }
            return false;
        }
    });
})(jQuery);

var toastElements = document.querySelectorAll('.toast');
for (var i = 0; i < toastElements.length; i++) {
  new bootstrap.Toast(toastElements[i]).show();
}