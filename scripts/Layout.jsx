import Button from '@material-ui/core/Button';
import { client_socket } from './Socket';
import { GoogleButton } from './GoogleButton';
import Linkify from 'react-linkify';
import {Login} from './Login'
import { makeStyles } from '@material-ui/core/styles';
import React, { useState, useEffect } from 'react'
import ScrollToBottom from 'react-scroll-to-bottom';
import './Styles.css';
import TextField from '@material-ui/core/TextField';

const is_image_url = require('is-image-url');


export default function Content() {
  const [username, set_username] = useState("");
  const [num_users, set_num_users] = useState(0);
  const [initial_message, set_initial_message] = useState([]);
  const [new_message, set_message] = useState("");
  const [image, set_image] = useState("");
  const [db_message, set_db_message] = useState([]);
  const [db_username, set_db_username] = useState([]);
  const [db_image, set_db_image] = useState([]);
  const [hide, set_hide] = useState(true);


  useEffect(() => {
    client_socket.on("username", (data) => {
      set_username(data['username']);
      set_image(data['image'])
      set_num_users(data['num_users']);
    });
  });

  useEffect(() => {
    client_socket.on('message', (data) => {
      if (is_image_url(data['message']['new_message'])) {}
      set_initial_message([...initial_message, (data['username'], data['message'])]);
      client_socket.removeAllListeners()
    });
  });


  useEffect(() => {
    client_socket.on('message_history', (data) => {
      set_db_message(data["all_messages"], []);
      set_db_username(data["all_users"], []);
      set_db_image(data["all_images"], []);
        });
    });


  useEffect(() => {
    client_socket.on("new_user", (data) => {
      set_num_users(data['num_users']);
    });
  });

  useEffect(() => {
    client_socket.on("lost_user", (data) => {
      set_num_users(data['num_users']);
    });
  });
  
   useEffect(() => {
    client_socket.on("signed_in", (data) => {
      set_hide(!data['is_signed_in']);
    });
  });
  
  const change_handler = (event) => {
    set_message(event.target.value);
  };

  
  const click_handler = () => {
    client_socket.emit("message", { username, new_message, image });
    set_message("");
  };
  
  const onKeyPress = (e) => {
    if(e.which === 13) {
      click_handler();
    }
  }
  
  return (
    <div hidden={hide}>
      <Login/>
        <div className="chat_box" >
          <div className="header">Active users: {num_users} </div>

            <div className="chat_container">
    
              <ScrollToBottom>
              <Linkify>
              {
                db_message.map(function(data,index) {
                  return is_image_url(data) ? 
                    (
                    <div key={index}> 
                      <div className="chip">
                        <div className="sender_info_area">
                          <div className="sender_info">
                              <img src={db_image[index]} className="profile_pic"/> {db_username[index]}
                          </div>
                        </div>
                        
                        <div> <img src={data}/> </div>
        
                      </div>
                    </div>
                    ) :
                        
                    (
                    <div key={index}> 
                      <div className="chip">
                        <div className="sender_info_area">
                          <div className="sender_info">
                            <img src={db_image[index]} className="profile_pic"/> {db_username[index]}
                          </div>
                        </div>
        
                        <div> {data} </div>
          
                      </div>
                    </div>
                  );
                })
              }
                  
              {
                initial_message.map(function(data,index) {
                  return is_image_url(data['new_message']) ? 
                    (
                      <div key={index}> 
                        <div className="chip">
                          <div className="sender_info_area">
                            <div className="sender_info">
                              <img src={data['image']} className="profile_pic"/> {data['username']}
                            </div>
                          </div>
                         
                          <div> <img src={data['new_message']}/> </div>
                     
                        </div>
                      </div>
                    ) : 
                        
                    (
                      <div key={index}> 
                        <div className="chip">
                          <div className="sender_info_area">
                            <div className="sender_info">
                              <img src={data['image']} className="profile_pic"/> {data['username']}
                            </div>
                          </div>
               
                          <div> {data['new_message']} </div>
          
                        </div>
                      </div>
                    );
                })
              }
            
          </Linkify>  
          </ScrollToBottom>
      </div>
      <div className="message_input">
        <TextField 
          id="outlined-basic"
          variant="outlined"
          label="Type a message"
          onChange={change_handler}
          value={new_message}
          id="text-box"
          onKeyPress={onKeyPress}
          fullWidth
          />
        
          <div align="right">
            <div className="useStyles().chat_button">
              <Button variant="contained" color="secondary" onClick={click_handler}>Send</Button>
            </div>
          </div>
     </div>
   </div>
</div>
  );
}