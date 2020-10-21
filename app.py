import os
import flask 
from flask import request
import flask_socketio
import random
import requests
import flask_sqlalchemy
import models
from os.path import join, dirname
from dotenv import load_dotenv
import Bot


#DB STUFF
MESSAGES_RECEIVED_CHANNEL = 'message_history'

app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

num_users = 0
new_username = ""

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']


app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

db.create_all()
db.session.commit()


def emit_all_messages(channel, sid):
    all_messages = [ \
        DB_message.db_message for DB_message \
        in db.session.query(models.SavedMessages).all()]
    
    all_users = [ \
        DB_username.db_username for DB_username \
        in db.session.query(models.SavedMessages).all()]
        
    server_socket.emit("message_history", { 'allMessages': all_messages, 'allUsers': all_users }, sid)
    
    global MESSAGES_RECEIVED_CHANNEL
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL, request.sid)

@server_socket.on('connect')
def on_connect():

    global num_users
    num_users += .5
    
    poke_num = random.randint(1, 151)
    api_link = f"https://pokeapi.co/api/v2/pokemon/{poke_num}"
    poke_data = requests.get(api_link)
    pack_data = poke_data.json()
    
    global new_username 
    new_username = pack_data['species']['name']
    
    server_socket.emit('username', { 'new_username': new_username, 'num_users': num_users }, request.sid)
    print("Given username: ", new_username)
    
    server_socket.emit('new_user', { 'num_users': num_users }, broadcast=True)
    print('Someone connected!', num_users)
    
    global MESSAGES_RECEIVED_CHANNEL
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL, request.sid)


@server_socket.on('disconnect')
def on_disconnect():
    global num_users
    num_users -= .5
    print('Someone disconnected!')
    server_socket.emit('lost_user', { 'num_users': num_users })


@server_socket.on('message')
def message_handler(message):
    global new_username
    server_socket.emit('message', { 'message': message, 'new_username': new_username })
    
    dexter = Bot.Bot(message)
    if message["new_message"][0:2] == "!!":
        message['new_username'] = "DEXTER"
        message['new_message'] = dexter.bot_action()
        server_socket.emit('message', { 'new_username': new_username, "message": message } )

    db.session.add(models.SavedMessages(message["new_message"], message["new_username"]))
    db.session.commit();
    print("Received message: ", message["new_username"], message["new_message"])


@app.route('/')
def hello():
    return flask.render_template('index.html')
    
        
if __name__ == '__main__': 
    server_socket.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )



