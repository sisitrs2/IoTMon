jQuery(function($) {

    $(".status").each(function() {
        var status = this.innerHTML;
        if (status == "Active") {
            $(this).addClass("green");
        } else if (status == "Down") {
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