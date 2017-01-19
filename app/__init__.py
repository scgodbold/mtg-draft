from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

# Database setup
db = SQLAlchemy(app)

# Websocket setup
socketio = SocketIO(app)


from app import models
db.create_all()


from app import views, websockets
