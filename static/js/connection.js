function connect(){
  socket = new WebSocket(
    window.location.protocol == 'https:' ? 'wss://' : 'ws://' +
    window.location.host + '/ws/game'
  );

  socket.onclose = function(event) {
    $("#main").fadeOut();
    $("#canvas").fadeIn();
  };

  socket.onmessage = function(event) {
    var msg = JSON.parse(event.data);

    switch(msg.event){
      case "gameReady":
        $("#main").fadeOut();
        $("#canvas").fadeIn();
        init();
        startGame(msg.data.pos);
        break;
      case "moveUp":
            update_y(player2, player2.y - delta);
        break;
      case "moveDown":
            update_y(player2, player2.y + delta);
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
