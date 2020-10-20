import React, { useState } from 'react';
import Login from './Login';
import  { GoogleButton } from './GoogleButton';
import Layout from './Layout';

export default function Content() {
    const [logged_in, set_logged_in] = useState(false)
    
    return logged_in ? <Layout /> : <Login set_logged_in={set_logged_in}/>
}