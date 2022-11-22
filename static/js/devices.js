

jQuery(function($) {

    $(".status").each(function() {
        var status = this.innerHTML;
        if (status == "OK") {
            $(this).addClass("green");
        } else if (status == "Alert") {
            $(this).addClass("red");
        } else if (status == "-") {
            // pass
        } else {
            $(this).addClass("orange");
        }
    })

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
    var id = $(this).find(".device-id").val();
    console.log(id);
    //if(url && !$(e.target).is("a") && !$(e.target).is("i")){
    //    window.open(url, '_blank').focus();
    //}
})

$(".add-device-button").click(function() {
    $(".add-device").toggle()
})

$(".add-device-user-button").click(function() {
    $(".add-device-user").toggle()
})

$(".add-device-type-button").click(function() {
    $(".add-device-type").toggle()
})


$(".cancel").click(function() {
    $(this).parent().parent().toggle()
})

function deleteRow(r) {
    var tr = r.parentNode.parentNode.rowIndex;
    var id = $(r).parent().parent().find(".device-id").val();
    document.getElementById("device-table").deleteRow(tr);
    $.post(Flask.url_for('remove_device', { id: id }));
}