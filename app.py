import os
import flask 
from flask import request
import flask_socketio
import random
import requests


app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")
num_users = 0
new_username = ""


def bot(message):
    if (message["new_message"] == "!!about"):
        print("Function entered !!about")
        message['new_username'] = "Poke-bot"
        message['new_message'] = "This is the best chat ever"
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"] == "!!pokemon"):
        poke_num = random.randint(1, 151)
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
        server_socket.send(random.choice(moods))
            
    elif (message["new_message"] == "!!help"):
        message['new_username'] = "Poke-bot"
        message['new_message'] = "Select from one of these: !!about -  !!funtranslate [message] - !!mood -  !!pokemon - !!help"
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
            
    elif (message["new_message"].split()[0] == "!!funtranslate"):
        phrase= message["new_message"][15:]
        """
        api_link = f"https://api.funtranslations.com/translate/doge.json?text={phrase}"
        doge_data = requests.get(api_link)
        pack_data = doge_data.json()
        translated = pack_data['contents']['translated']
        message['new_message'] = translated
        """
        message['new_username'] = "Poke-bot"
        message['new_message'] = "Placeholder"
        
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
        
    else:
        message['new_username'] = "Poke-bot"
        message['new_message'] = "Sorry, that is not a valid command. :/"
        
        server_socket.emit('message', { 'new_username': new_username, "message": message } )
        

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
    
    server_socket.emit('username', { 'new_username': new_username, 'num_users': num_users }, request.sid)
    print("Given username: ", new_username)
    
    server_socket.emit('new_user', { 'num_users': num_users }, broadcast=True)
    print('Someone connected!', num_users)
    


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
    if message["new_message"][0:2] == "!!":
        bot(message)
    print("Received message: ", message["new_username"], message["new_message"])

        
if __name__ == '__main__': 
    server_socket.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )