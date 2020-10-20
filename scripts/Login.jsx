import * as React from 'react';
//import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import * as SocketIO from 'socket.io-client';
import { GoogleLogin } from 'react-google-login';

export var client_socket = SocketIO.connect();

const responseGoogle = (response) => {
  console.log(response);
}

function get_info(response) {
    let username = response.nt.Ad
    let picture = response.profileObj.imageUrl
    let token_id = response.tokenId
    
    console.log("Name is ", username)
    console.log("Picture url is ", picture)
    console.log("Token id is ", token_id)
    
    client_socket.emit("new google user", {
        "username": username,
        "picture": picture,
    })
}

export default function Login() {
    return <GoogleLogin
        clientId="926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={get_info}
        onFailure={responseGoogle}
        cookiePolicy={'single_host_origin'}
        />;
}


