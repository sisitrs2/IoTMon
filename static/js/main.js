jQuery(function($) {

    $(".status").each(function() {
        var status = this.innerHTML;
        if (status == "Power") {
            $(this).addClass("green");
        } else if (status == "Battery") {
            $(this).addClass("red");
        } else {
            $(this).addClass("yellow");
        }
    })

    $("tr").click(function() {
        var url = this.title;
        if(url){
            window.open(url, '_blank').focus();
        }
    })
    
});

$(".add-device-button").click(function() {
    $(".add-device").toggle()
})


$(".add-device-user-button").click(function() {
    $(".add-device-user").toggle()
})

$(".cancel").click(function() {
    $(this).parent().parent().toggle()
})