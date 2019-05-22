function sign_in() {
    $("#signin_window").fadeIn();
    $("#signup_window").fadeOut();
}

function sign_out() {
    $.get("/user/logout");
    document.location.reload();
}

function sign_up() {
    $("#signup_window").fadeIn();
    $("#signin_window").fadeOut();
}

function trigger_leaderboard() {
    lb = $("#leaderboard");
    if (lb.css('display') == 'block') {
        lb.fadeOut();
    } else {
        lb.fadeIn();
    }
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

$(document).mouseup(function(e){
    divs = $(".auth_window, #leaderboard");
    if (!divs.is(e.target) && divs.has(e.target).length === 0) {
        divs.fadeOut();
    }
});

function send(form_id){
    var form = document.getElementById(form_id);
    var user = form.user.value, pwd = form.pwd.value;

    var url = "/user/login";
    if (form_id != "signin_form") {
        url = "/user/signup";
    }

    $.post(url, { "user": user, "pwd": pwd })
    .done(function( data ) {
        document.location.reload();
    });
}
