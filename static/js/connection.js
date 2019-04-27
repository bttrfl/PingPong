function game(){
  
  var socket = new WebSocket("ws://0.0.0.0:8080/ws");
  
  socket.onopen = function() {
    socket.send("NU CHE NA NAROD POGNALI NAHOOI");
    socket.send("EEEBANII V ROT"); 
    alert("C1");
  };

  socket.onclose = function(event) {
    if (event.wasClean) {
      alert('C2');
    } else {
      alert('C3'); // например, "убит" процесс сервера
    }
    alert('C4: ' + event.code + ' C5: ' + event.reason);
  };

  socket.onmessage = function(event) {
    alert("C6 " + event.data);
  };

  socket.onerror = function(error) {
    alert("C7 " + error.message);
  };


}

