function connect(){
  socket = new WebSocket(
    window.location.protocol == 'https:' ? 'wss://' : 'ws://' +
    window.location.host + '/ws/game'
  );

  socket.onclose = function(event) {
    document.getElementById('main').style.visibility = 'visible';
    document.getElementById('main').style.visibility = 'block';
    document.getElementById('canvas').style.visibility = 'hidden';
    document.body.style.backgroundColor = '#404040';
  };

  socket.onmessage = function(event) {
    var msg = JSON.parse(event.data);

    switch(msg.event){
      case "gameReady":
        document.getElementById('main').style.visibility = 'hidden';
        document.getElementById('main').style.display = 'none';
        document.getElementById('canvas').style.visibility = 'visible';
        document.body.style.backgroundColor = 'black';
        init();
        break;
      case "moveUp":
        break;
      case "moveDown":
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
