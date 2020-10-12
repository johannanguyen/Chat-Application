import React, { useState } from 'react';
import { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import * as SocketIO from 'socket.io-client';
import './Styles.css';
import ScrollToBottom from 'react-scroll-to-bottom';

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
    chat_window: {
        width: '100%',
        height: '300px',
        textAlign: 'right',
        padding: '3px',
        overflowY: 'auto',
        overflowX: 'hidden',
        flex: 'row-reverse'
    },
    chat_box: {
        width: '90%'  
    },
    chat_button: {
        width: '10%'
        },

}));


export default function Layout() {
    const [new_username, set_username] = useState("");
    const [num_users, set_user_count] = useState(0);
    const [initial_message, set_initial_message] = useState([]);
    const [new_message, set_message] = useState("");
    const [db_message, set_db_message] = useState([]);
    const [db_user, set_db_user] = useState([]);
    
    useEffect(() => {
    client_socket.on("username", (data) => {
      set_username(data['new_username']);
      set_user_count(data['num_users']);
      console.log("Received user name: " + data['new_username'], data['num_users']);
        });
    });
    

    useEffect(() => {
    client_socket.on('message', (data) => {
      set_initial_message([...initial_message, (data['new_username'], data['message']) ] );
      console.log("Received a message from: ", data['new_username'], data['message']);
        });
    });
    
    
    useEffect(() => {
    client_socket.on('message_history', (data) => {
      set_db_message(data["allMessages"], []);
      set_db_user(data["allUsers"], []);
      console.log("Received something: ", data["allMessages"], data["allUsers"]);
        });
    });

    
    useEffect(() => {
    client_socket.on("new_user", (data) => {
      set_user_count(data['num_users']);
      console.log("Received num users: " + data['num_users']);
        });
    });
    
    useEffect(() => {
    client_socket.on("lost_user", (data) => {
      set_user_count(data['num_users']);
      console.log("Received num users: " + data['num_users']);
        });
    });
    


    const change_handler = (event) => {
        set_message(event.target.value);
    };

    const click_handler = () => {
        client_socket.emit("message", {new_username, new_message});
        set_message("");
    };

    

    return (
        <div>
            <div align = "center">
            

                <Paper className={useStyles().root}>
                <Paper elevation={3} />
                

                    <Typography variant="h5" component="h3"> Chat </Typography>
                    <Typography component="h3">Number of users: {num_users} Your username: {new_username}</Typography>
        

                    <div className={useStyles().chat_window}>
                    <ScrollToBottom className="useStyles().chat_window">
                    
                        { db_message.map((data, index) => (<div><div className="p_self">{data}</div>{db_user[index]}</div>)) }
                        { initial_message.map((data) => (<div><div className="p_self">{data['new_message']}</div>{data['new_username']}</div>)) }
                        
                    </ScrollToBottom>
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