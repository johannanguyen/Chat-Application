import Bot
from dotenv import load_dotenv
from google.oauth2 import id_token as idToken
from google.auth.transport import requests
import flask
import flask_socketio
import flask_sqlalchemy
from flask import request as Request
from flask import Flask, render_template, redirect, url_for, request
import json
import models
import os
from os.path import join, dirname
import random
import sys


MESSAGES_RECEIVED_CHANNEL = 'message_history'

app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

username = ""
num_users = 0

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URI']
    
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

db.create_all()
db.session.commit()

    
def emit_all_messages(channel, sid):
    all_messages = [ \
        DB_message.db_message for DB_message \
        in db.session.query(models.MessageHistory).all()]
        
    all_users = [ \
        DB_username.db_username for DB_username \
        in db.session.query(models.MessageHistory).all()]
        
    all_images = [ \
        DB_image.db_image for DB_image \
        in db.session.query(models.MessageHistory).all()]
        
    server_socket.emit('message_history', {
        'all_messages':all_messages,
        'all_users': all_users,
        'all_images': all_images
    }, sid)
    
    print(all_messages, all_users, all_images)
    
    
@server_socket.on('connect')
def on_connect():
    global num_users
    num_users += 1
    server_socket.emit('new_user', { 'num_users': num_users }, broadcast=True)
    
    
@server_socket.on('google_user')
def on_google_user(data):
    global username
    username = data['username']
    
    print("Google user data:", data)
    id_token = data['id_token']
    is_signed_in = data['is_signed_in']
    image = data['image']
    
    try:
        authentication = idToken.verify_oauth2_token(id_token, requests.Request(), "926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com" )
        
    except ValueError:
        print('Cannot be authenticated')
    

    if data['is_signed_in']==True:
        server_socket.emit('username', { 'username': username, 'num_users': num_users, 'image':image }, Request.sid)
        server_socket.emit('signed_in', {'is_signed_in': is_signed_in})
        print('Someone connected!', num_users)
        
        global MESSAGES_RECEIVED_CHANNEL
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL, Request.sid)


@server_socket.on('disconnect')
def on_disconnect():
    global num_users
    num_users -= 1
    print('Someone disconnected!')
    server_socket.emit('lost_user', { 'num_users': num_users })


@server_socket.on('message')
def message_handler(message):
    server_socket.emit('message', { 'message': message, 'username': username, 'image': message['image']})
    db.session.add(models.MessageHistory(message["username"], message["new_message"], message['image']));
    db.session.commit();
    
    dexter = Bot.Bot(message)
    if message["new_message"][0:2] == "!!":
        message['username'] = "DEXTER"
        message['image']= "https://cdn.bulbagarden.net/upload/thumb/e/e2/133Eevee.png/250px-133Eevee.png"
        message['new_message'] = dexter.bot_action()
        server_socket.emit('message', {'username': username, 'message': message, 'image': message['image'] })
        db.session.add(models.MessageHistory(message["username"], message["new_message"], message['image']));
        db.session.commit();
    
    
@app.route('/', methods=['GET', 'POST'])
def hello():
    return flask.render_template('index.html')


if __name__ == '__main__': 
    server_socket.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )