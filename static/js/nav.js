$(".sel_wrap").on("change", function() {
    var o;
    var opt = $(this).find('option');
    opt.each(function(i) {
        if (opt[i].selected == true) {
            o = opt[i].innerHTML;
        }
    })
    $(this).find('label').html(o);
});
