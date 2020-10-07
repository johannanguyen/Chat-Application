import os
import flask
import flask_socketio

app = flask.Flask(__name__)
server_socket = flask_socketio.SocketIO(app)
server_socket.init_app(app, cors_allowed_origins="*")

@app.route('/')
def hello():
    return flask.render_template('index.html')
    

@server_socket.on('connect')
def on_connect():
    print('Someone connected!')
    server_socket.emit('connected', {
        'test': 'Connected'
    })
    

@server_socket.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')


@server_socket.on('message')
def message_handler(message):
    print("Received message: " + message)
    flask_socketio.send(message)


if __name__ == '__main__': 
    server_socket.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
