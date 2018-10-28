$(".menu-link").on('click', function(event) {
    let target = this.getAttribute("data-target");
    $("#" + target).toggleClass('hidden');
    event.stopPropagation();
});

$(window).on('click', function() {
    $(".menu").addClass('hidden');
});
