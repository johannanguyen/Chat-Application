import React, { useState } from 'react';
import { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import * as SocketIO from 'socket.io-client';

export var client_socket = SocketIO.connect();


//Position the different components
const useStyles = makeStyles(layout => ({
    root: {
        margin: '100px',
        padding: layout.spacing(5, 2),
        width: '600px',
    },
    flex: {
        display: 'flex',
    },
    chat_box: {
        width: '90%'  
    },
    chat_button: {
        width: '10%'
        },

    }));

    const [num_users, set_user_count] = useState(0);
    const [initial_message, set_initial_message] = useState([]);
    const [new_message, set_message] = useState("");

    useEffect(() => {
    client_socket.on('message', msg => {
      set_initial_message([...initial_message, msg]);
        });
    });
    
    useEffect(() => {
    client_socket.on("new_user", (data) => {
      set_user_count(data['num_users']);
        });
    });
    
    useEffect(() => {
    client_socket.on("lost_user", (data) => {
      set_user_count(data['num_users']);
        });
    });
    
    client_socket.removeAllListeners();

    const click_handler = () => {
        client_socket.emit("message", new_message);
        set_message("");
    };


    return (
        <div>
            <TextField
                id="standard-multiline-flexible"
                label="Type a message"
                multiline
                rowsMax={4}
                className={useStyles().chat_box}
                onChange={ click_handler } 
                value={ new_message }
            />
            <Button variant="contained" color="secondary">Send</Button>  
        </div>
    );

