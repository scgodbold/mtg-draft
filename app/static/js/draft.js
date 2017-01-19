function get_payload_base() {
    var payload = { 
        'username': $('#username').text(),
        'room': $('#draft-id').text(),
    };
    return payload
};

function add_message(msg) {
    if(msg['user'] === null) {
        $('#messages').append($('<li class="server-msg">').text(msg['msg']));
    } else {
        $('#messages').append($('<li>').text(msg['user'] + ': ' + msg['msg']));

    };
};

$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/draft');
    socket.on('connected', function(msg) {
        console.log('Connection Established');
        socket.emit('join', get_payload_base());
    });

    $('#send-message').submit(function(e){
        e.preventDefault();
        var payload = get_payload_base();
        payload['msg'] = $('#message-text').val()
        socket.emit('chat message', payload)
        $('#message-text').val('');
        return false;
    });
    socket.on('message', function(msg){
        add_message(msg);
        $('#messages').animate({
                    scrollTop: $('#messages')[0].scrollHeight}, 100);
    });
});
