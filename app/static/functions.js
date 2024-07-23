const socket = io();
socket.on("connect", () => {
  socket.emit("user_connect");
});

socket.on("message-sent", function (res) {
  $("#messages").prepend(
    '<div class="message message-sent"><div class="content">' +
      res.msg +
      "</div>" +
      '<div class="meta">Yo, 10:30 AM</div>' +
      "</div>"
    //"<div><strong>" + res.user + ":</strong>" + res.msg + "</div>"
  );
});
socket.on("message-received", function (res) {
  $("#messages").prepend(
    '<div class="message message-received">' +
      '<img src="static/profile.png" width="40"alt="Perfil" class="profile-pic">' +
      '<div class="content">' +
      res.msg +
      "</div>" +
      '<div class="meta"><strong>' +
      res.user +
      "</strong>, 10:31 AM</div></div>"
    //"<div><strong>" + res.user + ":</strong>" + res.msg + "</div>"
  );
});

socket.on("user_connect_list", function (data) {
  $("#listUsuarios").empty();
  data.user.forEach((user) => {
    $("#listUsuarios").prepend(
      '<li><i class="bi bi-person-circle"></i>' + user + "</li>"
    );
  });
});

socket.on("user_disconnect", function (data) {
  $("#messages").prepend(
    '<div id="chat-box" class="chat-box">' +
      data.user +
      " se ha desconectado</div>"
  );
});

socket.on("user_connected", function (data) {
  $("#messages").prepend(
    '<div id="chat-box" class="chat-box">' +
      data.user +
      " ha ingresado al chat</div>"
  );
});

$("#send").on("click", function () {
  socket.send($("#msgUser").val());
  $("#msgUser").val("");
});
