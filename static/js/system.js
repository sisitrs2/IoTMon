
$("devices tr").click(function(e) {
    var url = this.title;
    if(url && !$(e.target).is("a") && !$(e.target).is("i")){
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

function deleteUser(r) {
    var tr = r.parentNode.parentNode.rowIndex;
    var id = $(r).parent().parent().find(".user-id").val();
    document.getElementById("users-table").deleteRow(tr);
    $.post(Flask.url_for('remove_user', { id: id }));
}

function deleteArea(r) {
    var tr = r.parentNode.parentNode.rowIndex;
    var id = $(r).parent().parent().find(".area-id").val();
    document.getElementById("areas-table").deleteRow(tr);
    $.post(Flask.url_for('remove_area', { id: id }));
}