jQuery(function($) {
    $(".celsius").each(function() {
        var cel = this.innerHTML;
        if (parseInt(cel) >= 29) {
            $(this).parent().addClass("red");
        }
    })

    $(".voltage").each(function() {
        var vol = this.innerHTML;
        console.log(parseFloat(vol));
        if (parseFloat(vol) <= 54 || parseFloat(vol) >= 55) {
            $(this).parent().addClass("red");
        }
    })
});

$(".clickable tr").click(function(e) {
    var url = this.title;
    if(url && !$(e.target).is("input")){
        window.open(url, '_blank').focus();
    }
})

$(".add-user-button").click(function() {
    $(".add-user").toggle()
})

$(".add-area-button").click(function() {
    $(".add-area").toggle()
})


$(".cancel").click(function() {
    $(this).parent().parent().toggle()
})

function toggleRelevant(r) {
    var id = $(r).parent().parent().find(".alarm-id").val();
    $.post(Flask.url_for('toggle_relevant', { id: id }));
}