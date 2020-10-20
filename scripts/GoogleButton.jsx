import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';

const responseGoogle = (response) => {
  console.log(response);
}

function get_info(response) {
    let username = response.nt.Ad
    let picture = response.profileObj.imageUrl
    console.log("Name is ", username)
    console.log("Picture url is ", picture)
    
    Socket.emit("new google user", {
        "username": username,
        "picture": picture
    })
}

export function GoogleButton() {
    return <GoogleLogin
        clientId="926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={get_info}
        onFailure={responseGoogle}
        cookiePolicy={'single_host_origin'}
        />;
}
