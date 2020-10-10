import os
import flask 
from flask import request
import flask_socketio
import random
import requests
import emoji

import random
import requests
import emoji


app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")
num_users = 0
new_username = ""


def bot(message):
    if(message[0:2] == "!!"):
        if (message == "!!about"):
            server_socket.send("This is the best chat app in the world!")
            
        elif (message == "!!pokemon"):
            poke_num = random.randint(1, 151)
            api_link = f"https://pokeapi.co/api/v2/pokemon/{poke_num}"
            poke_data = requests.get(api_link)
            pack_data = poke_data.json()
            poke_name = pack_data['species']['name']
            poke_type = pack_data['types'][0]['type']['name']
            print(poke_name, poke_type)
            server_socket.send(poke_name + " is a " + poke_type + " pokemon! :)")
            
        elif (message == "!!mood"):
            moods = [ "I'm feeling happy.",
                    "I'm feeling sleepy.",
                    "I'm feeling awkward.",
                    "I'm feeling lovely.",
                    "I'm feeling hungry.",
                    "I'm feeling evil.",
                    "I'm feeling bored.",
                    "I'm feeling lazy....."]
            server_socket.send(random.choice(moods))
            
        elif (message == "!!help"):
            server_socket.send("Select from one of these: !!about -  !!funtranslate [message] - !!mood -  !!pokemon - !!help")
            
        elif (message.split()[0] == "!!funtranslate"):
            phrase= message[15:]
            """
            api_link = f"https://api.funtranslations.com/translate/doge.json?text={phrase}"
            doge_data = requests.get(api_link)
            pack_data = doge_data.json()
            translated = pack_data['contents']['translated']
            """
            server_socket.send("PLACEHOLDER VALUE - DOGE")
        
        else:
            server_socket.send("Sorry, that's not a proper command. :/")
        

@app.route('/')
def hello():
    return flask.render_template('index.html')
    

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
    
    server_socket.emit('username', { 'new_username': new_username}, request.sid)
    print("Given username: ", new_username)
    
    print('Someone connected!', num_users)
    server_socket.emit('new_user', { 'num_users': num_users })

    

@server_socket.on('disconnect')
def on_disconnect():
    global num_users
    num_users -= 1
    print('Someone disconnected!')
    server_socket.emit('lost_user', { 'num_users': num_users })


@server_socket.on('message')
def message_handler(message):
    global new_username
    #bot(message)
    server_socket.emit('message', {
        'message': message,
        'new_username': new_username
    })
    print("Received message: ", message["new_username"], message["new_message"])
    

if __name__ == '__main__': 
    server_socket.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
