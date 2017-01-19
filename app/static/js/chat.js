$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('server response', function(msg) {
        console.log('Recieved: ' + msg['data'])
    });
    $('form').submit(function(){
        socket.emit('chat message', $('#m').val());
        $('#m').val('');
        return false;
    });
    socket.on('chat message', function(msg){
        $('#messages').append($('<li>').text(msg['data']));
    });
});
