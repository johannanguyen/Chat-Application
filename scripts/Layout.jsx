import React, { useState } from 'react';
import { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
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
        alignItems: 'center'
    },
    chat_window: {
        width: '100%',
        height: '300px',
        textAlign: 'right',
        padding: '3px',
        overflowY: 'auto'
    },
    chat_box: {
        width: '90%'  
    },
    chat_button: {
        width: '10%'
        },

}));

export default function Layout() {
    const [initial_message, set_initial_message] = useState([]);
    const [new_message, set_message] = useState("");

    useEffect(() => {
    client_socket.on('message', msg => {
      set_initial_message([...initial_message, msg]);
        });
    });
    
    client_socket.removeAllListeners();

    const change_handler = (event) => {
        set_message(event.target.value);
    };

    const click_handler = () => {
        client_socket.emit("message", new_message);
        set_message("");
    };

    return (
        <div>
            <div align = "center">
                <Paper className={useStyles().root}>
                <Paper elevation={3} />
                    <Typography variant="h5" component="h3"> Chat </Typography>
                    <Typography component="p">Have some fun</Typography>

                    <div className={useStyles().chat_window}>
                        { initial_message.map(msg => (<p>{msg}</p>)) }
                    </div>

                    <div className={useStyles().flex}>
                        <TextField
                          id="standard-multiline-flexible"
                          label="Type a message"
                          multiline
                          rowsMax={4}
                          className={useStyles().chat_box}
                          onChange={ change_handler } 
                          value={ new_message }
                        />
                      <Button variant="contained" color="secondary" onClick={ click_handler }>Send</Button>  
                    </div>
                </Paper>
            </div>
        </div>
    );
}
