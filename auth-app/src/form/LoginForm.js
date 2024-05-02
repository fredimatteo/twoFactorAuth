// LoginForm.js

import React, {useState} from 'react';

function LoginForm({ onLoginSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showErrorMessage, setErrorMessage] = useState(false);

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    function hideErrorMessage() {
        setErrorMessage(false)
    }

    const handleSubmit = (event) => {
        event.preventDefault(); // Previeni il comportamento di default del submit

        login(username, password)
            .then(response => {
                localStorage.setItem("otpToken", response["otp_token"]);
                onLoginSuccess();
            })
            .catch(error => {
                setErrorMessage(true);
            });
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Username" value={username} onChange={handleUsernameChange} onClick={hideErrorMessage}/>
                <input type="password" placeholder="Password" value={password} onChange={handlePasswordChange} onClick={hideErrorMessage}/>
                {showErrorMessage && <p className="Error-message">Invalid username or password</p>}
                <button type="submit" className="Button-login">Login</button>
            </form>
        </div>
    );
}


async function login(username, password) {
    try {
        const response = await fetch(process.env.REACT_APP_BASE_URL + '/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password}),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        throw new Error('Error during login:', error);
    }
}

export default LoginForm;
