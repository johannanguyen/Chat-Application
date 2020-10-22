import { client_socket } from './Socket';
import GoogleLogin from 'react-google-login';
import * as React from 'react';


const responseGoogle = (response) => {
  console.log("Could not log in: ", response);
}

function get_info(google_user) {
    var id_token = google_user.getAuthResponse().id_token;
    let username = google_user.profileObj.name;
    let image = google_user.profileObj.imageUrl;
    let is_signed_in = google_user.isSignedIn()
    
    client_socket.emit('google_user', {
        'id_token': id_token,
        'username': username,
        'image': image,
        'is_signed_in': is_signed_in
    });
}

export function GoogleButton() {
    return (
        <div>
            <GoogleLogin
            clientId="926047747876-uprudtkm1e9d6e23nrf252dq07qb62tn.apps.googleusercontent.com"
            buttonText="Login to Talk to the Coolest People EVER"
            onSuccess={get_info}
            onFailure={responseGoogle}
            cookiePolicy={'single_host_origin'}
            />
        </div>
    );
}
