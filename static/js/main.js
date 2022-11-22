jQuery(function($) {

    $(".status").each(function() {
        var status = this.innerHTML;
        if (status == "Power") {
            $(this).addClass("green");
        } else if (status == "Battery") {
            $(this).addClass("red");
        } else {
            $(this).addClass("orange");
        }
    })

    if(window.location.pathname != "/") {
        window.location.href = "/"; 
    }
});



$("tr").click(function(e) {
    var url = this.title;
    if(url && !$(e.target).is("a") && !$(e.target).is("i")){
        window.open(url, '_blank').focus();
    }
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

$(".profile").click(function() {
    document.cookie = ""
})

function deleteRow(r) {
    var tr = r.parentNode.parentNode.rowIndex;
    var id = $(r).parent().parent().find(".device-id").val();
    document.getElementById("device-table").deleteRow(tr);
    $.post(Flask.url_for('remove_device', { id: id }));
}