function showErrorMessage(message){
    $('.alert').text(message)
    $('.alert').show();
    document.getElementsByClassName("alert")[0].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
}


function setError(input){
    input.css("border-color", "red")
}


$(document).on("keyup", ".form-control", function () {
    $(this).css("border-color", "")
});
