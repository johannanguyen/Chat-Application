import * as React from 'react';
import Login from './Login';
import Layout from './Layout';

export default function Content() {
    const [accounts, setAccounts] = React.useState([]);
    
    return (
        <div>
            <Login />
            <Layout />
        </div>
    );
}