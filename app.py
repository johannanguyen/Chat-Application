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
MESSAGE_RECEIVED_CHANNEL = 'message_history'

app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

num_users = 0
new_username = ""

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app


db.create_all()
db.session.commit()


#BOT STUFF
"""
def bot(message):
    if (message["new_message"] == "!!about"):
        print("Function entered !!about")
        message['new_username'] = "Poke-bot"
        message['new_message'] = "This is the best chat ever"
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"] == "!!pokemon"):
        poke_num = random.randint(1, 300)
        api_link = f"https://pokeapi.co/api/v2/pokemon/{poke_num}"
        poke_data = requests.get(api_link)
        pack_data = poke_data.json()
        poke_name = pack_data['species']['name']
        poke_type = pack_data['types'][0]['type']['name']
        print(poke_name, poke_type)
        
        message['new_username'] = "Poke-bot"
        message['new_message'] = poke_name + " is a " + poke_type + " pokemon! :)"
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"] == "!!mood"):
        moods = [ "I'm feeling happy.",
                "I'm feeling sleepy.",
                "I'm feeling awkward.",
                "I'm feeling lovely.",
                "I'm feeling hungry.",
                "I'm feeling evil.",
                "I'm feeling bored.",
                "I'm feeling lazy....."]
        message['new_username'] = "Poke-bot"
        message['new_message'] = random.choice(moods)
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"] == "!!help"):
        message['new_username'] = "Poke-bot"
        message['new_message'] = "Select from one of these: !!about -  !!funtranslate [message] - !!mood -  !!pokemon - !!help"
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"].split()[0] == "!!funtranslate"):
        phrase= message["new_message"][15:]

        #api_link = f"https://api.funtranslations.com/translate/doge.json?text={phrase}"
        #doge_data = requests.get(api_link)
        #pack_data = doge_data.json()
        #translated = pack_data['contents']['translated']
        #message['new_message'] = translated

        message['new_username'] = "Poke-bot"
        message['new_message'] = "Placeholder"
        
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
        
    else:
        message['new_username'] = "Poke-bot"
        message['new_message'] = "Sorry, that is not a valid command. :/"
        
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
"""        

@server_socket.on('connect')
def on_connect():
    poke_num = random.randint(1, 151)
    api_link = f"https://pokeapi.co/api/v2/pokemon/{poke_num}"
    poke_data = requests.get(api_link)
    pack_data = poke_data.json()
    
    global new_username 
    new_username = pack_data['species']['name']
    
    global num_users
    num_users += 1
    
    
    server_socket.emit('username', { 'new_username': new_username, 'num_users': num_users }, request.sid)
    print("Given username: ", new_username)
    
    server_socket.emit('new_user', { 'num_users': num_users }, broadcast=True)
    print('Someone connected!', num_users)
    
    all_messages = [ \
        DB_message.db_message for DB_message \
        in db.session.query(models.SavedMessages).all()]
    
    all_users = [ \
        DB_username.db_username for DB_username \
        in db.session.query(models.SavedMessages).all()]
        
    server_socket.emit("message_history", { 'allMessages': all_messages, 'allUsers': all_users }, request.sid)
    


@server_socket.on('disconnect')
def on_disconnect():
    global num_users
    num_users -= 1
    print('Someone disconnected!')
    server_socket.emit('lost_user', { 'num_users': num_users })


@server_socket.on('message')
def message_handler(message):
    global new_username
    server_socket.emit('message', { 'message': message, 'new_username': new_username })
    
    poke_bot = Bot.Bot(message)
    if message["new_message"][0:2] == "!!":
        message['new_username'] = "Poke-bot"
        message['new_message'] = poke_bot.bot_action()
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



