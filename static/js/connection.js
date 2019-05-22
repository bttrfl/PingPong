function connect(){
  socket = new WebSocket(
    window.location.protocol == 'https:' ? 'wss://' : 'ws://' +
    window.location.host + '/ws/game'
  );

  socket.onclose = function(event) {
    $("#game").fadeOut();
    $("#wrapper").fadeIn();
  };

  socket.onmessage = function(event) {
    var msg = JSON.parse(event.data);

    switch(msg.event){
      case "gameReady":
        $("#wrapper").fadeOut();
        $("#game").fadeIn();
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
        $("#game").fadeOut();
        $("#wrapper").fadeIn();
        break;
      case "wsError":
        alert('Error: client disconnected');
        break;
    }

  };

  socket.onerror = function(error) {
    alert(error.message);
  };
}
