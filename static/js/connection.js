var ps = 15;

function nfp(urpx) {
    return Number(urpx.replace("px", ""))
}

var r = document.getElementById('right');
var l = document.getElementById('left');
var b = document.getElementById('ball');

var rscore = document.getElementById('scoreleft');
var lscore = document.getElementById('scoreright');
var ogoal = document.getElementById('goal');

var w = window.innerWidth;
var h = window.innerHeight;

var map = []; // Or you could call it "key"
onkeydown = onkeyup = function(e) {
    e = e || event; // to deal with IE
    map[e.keyCode] = e.type == 'keydown';
    /*insert conditional here*/
}





function keydown(socket, pl_pos) {
    //if key was s
    if (map[83]) {
        var msg = {
          event: "moveUp",
          pos: pl_pos
        }
        socket.send(JSON.stringify(msg));
    }

    //if key was w
    else if (map[87]) {
        var msg = {
          event: "moveDown",
          pos: pl_pos
        }
        socket.send(JSON.stringify(msg));
    }
}



var speedx = 3,
    speedy = 1;
var balltime = 1;
b.style.left = w / 2 + "px";

function ball() {
    b.style.left = nfp(b.style.left) + speedx + "px";
    b.style.top = nfp(b.style.top) + speedy + "px";
}




function performkeydown(direction, pos){
    if (direction) {
      if (pos){
        
        if (nfp(l.style.top) + ps > h - 200)
            l.style.top = h - 200 + "px";
        else
            l.style.top = nfp(l.style.top) + ps + "px";
      
      } else {
        
        if (nfp(r.style.top) + ps > h - 200)
          r.style.top = h - 200 + "px";
        else
          r.style.top = nfp(r.style.top) + ps + "px";
      }
    }

    else {
      if (pos) {
       
       if (nfp(l.style.top) - ps < 0)
            l.style.top = 0 + "px";
        else
            l.style.top = nfp(l.style.top) - ps + "px";

      } else {
        
        if (nfp(r.style.top) - ps < 0)
            r.style.top = 0 + "px";
        else
            r.style.top = nfp(r.style.top) - ps + "px";

      }
    }
}


function game(){
  var socket = new WebSocket(
    window.location.protocol == 'https:' ? 'wss://' : 'ws://' +
    window.location.host + '/ws/game'
  );

  socket.onopen = function() {
    socket.send("NU CHE NA NAROD POGNALI NAHOOI");
    socket.send("EEEBANII V ROT");
  };

  socket.onclose = function(event) {

    document.getElementById('main').style.visibility = 'visible';
    document.getElementById('main').style.visibility = 'block';
    document.getElementById('game').style.visibility = 'hidden';
    document.body.style.backgroundColor = '#404040';
  };

  socket.onmessage = function(event) {
    var msg = JSON.parse(event.data);
    var pl_pos = "0";

    switch(msg.event){
      case "gameReady":
        document.getElementById('main').style.visibility = 'hidden';
        document.getElementById('main').style.display = 'none';
        document.getElementById('game').style.visibility = 'visible';
        document.body.style.backgroundColor = 'black';

        pl_pos = msg.pos;
        setInterval(function() {
          keydown(socket, pl_pos);
        }, 10);
        break;
      case "moveUp":
        performkeydown(true, msg.pos == pl_pos);
        break;
      case "moveDown":
        performkeydown(false, msg.pos == pl.pos);
        break;
      case "gameOver":
        alert('not implemented');
        break;
      case "wsError":
        alert('not implemented');
        break;
    }
  };

  socket.onerror = function(error) {
    alert(error.message);
  };


}



function moveball() {
    ball();

    //remove overflow y
    if (h < nfp(b.style.top) + 20 || nfp(b.style.top) < 0) {
        speedy *= -1;
    }

    //overflow-x right
    if (nfp(b.style.left) >= w - 50) {
        if (nfp(r.style.top) <= nfp(b.style.top) + 20 && nfp(r.style.top) + 200 >= nfp(b.style.top)) {
            speedx *= -1;
        } else if (nfp(b.style.left) >= w - 20)
            goal('left');
    }




    //remove overflow x in left ir get the goal in left
    if (nfp(b.style.left) <= 30) {
        if (nfp(l.style.top) <= nfp(b.style.top) + 20 && nfp(l.style.top) + 200 >= nfp(b.style.top)) {
            speedx *= -1;
        } else if (nfp(b.style.left) <= 0)
            goal('right');
    }



    setTimeout(function() {
        moveball()
    }, balltime);
}


moveball();



function goal(pos) {

    ogoal.style.color = "white";

    setTimeout(function() {
        ogoal.style.color = "black"
    }, 1000);

    if (pos == "left")
        rscore.innerHTML = Number(rscore.innerHTML) + 1;
    else
        lscore.innerHTML = Number(lscore.innerHTML) + 1;


    speedx *= -1;
    b.style.left = w / 2 + "px";


}
