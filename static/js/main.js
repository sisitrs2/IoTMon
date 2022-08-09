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

    $("tr").click(function() {
        var url = this.title;
        if(url){
            window.open(url, '_blank').focus();
        }
    })

    if(window.location.pathname != "/") {
        window.location.href = "/"; 
    }
});

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
    var i = r.parentNode.parentNode.rowIndex;
    document.getElementById("device-table").deleteRow(i)
}