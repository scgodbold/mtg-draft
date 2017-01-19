from app import socketio

from flask_socketio import emit, send, join_room, leave_room


@socketio.on('connect', namespace='/chat')
def chat_connect():
    print('User has connected to: /chat')
    emit('server response', {'data': 'Connected to /chat'})


@socketio.on('disconnect', namespace='/chat')
def chat_disconnect():
    print('User has disconnected from: /chat')


@socketio.on('chat message', namespace='/chat')
def recieve_message(msg):
    print('Recieved message: {}'.format(msg))
    emit('chat message', {'data': msg}, broadcast=True)


@socketio.on('connect', namespace='/draft')
def draft_connect():
    emit('connected', {'data': 'Connected to draft'})


@socketio.on('join', namespace='/draft')
def join_draft(data):
    username = data['username']
    room = data['room']
    join_room(room)
    payload = {
        'user': None,
        'msg': '{} has joined the room'.format(username),
    };
    emit('message', payload, room=room)


@socketio.on('chat message', namespace='/draft')
def draft_chat(data):
    print(data)
    payload = {
        'user': data['username'],
        'room': data['room'],
        'msg': data['msg']
    }
    emit('message', payload, room=data['room'])
