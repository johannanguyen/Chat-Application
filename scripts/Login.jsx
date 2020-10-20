import React, {useState, useEffect} from 'react'
import GoogleLogin from 'react-google-login';
import * as SocketIO from 'socket.io-client';

export var client_socket = SocketIO.connect();



export default function Login(props){
 
    const [userName, setUserName] = useState("");
   
   
    const onChange = (event) => {
      setUserName(event.target.value);
    };

        function handleGoogleLogin(event) {
            let username = event.getBasicProfile().getName()
            let image = event.getBasicProfile().getImageUrl()
            let token_id = event.getAuthResponse().id_token
            console.log(username);
            console.log(image);
            console.log(token_id);
            props.set_logged_in(true);
        
    }
      
    const responseGoogle = (response) => {
        console.log(response);
    }

    return (
        <GoogleLogin
            clientId="926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={handleGoogleLogin}
            onFailure={responseGoogle}
            cookiePolicy={'single_host_origin'}
         />
    )
}