function sign_in() {
    $(".auth_window").fadeOut(function(){
        $("#signin_window").fadeIn();
    });
}

function sign_out() {
    $.get("/user/logout");
    document.location.reload();
}

function sign_up() {
    $(".auth_window").fadeOut(function(){
        $("#signup_window").fadeIn();
    });
}

function lang2ru() {
    set_cookie("lang", "ru", 30);
    document.location.reload();
}

function lang2en() {
    set_cookie("lang", "en", 30);
    document.location.reload();
}

function set_cookie(key, val , ttl) {
    var date = new Date;
    date.setDate(date.getDate() + 30);
    document.cookie = key+"="+val+"; path=/; expires=" + date.toUTCString();

}
