// OtpForm.js

import React, {useState} from 'react';
import HandleGetUsers from '../view/Users';

function OtpForm({ onLoginSuccess }) {
    const [otp_code, setOtp_code] = useState('');
    const [showErrorMessage, setErrorMessage] = useState(false);

    const handleOtpChange = (event) => {
        setOtp_code(event.target.value);
    };

    function hideErrorMessage() {
        setErrorMessage(false)
    }

    const handleSubmit = (event) => {
        event.preventDefault(); // Previeni il comportamento di default del submit

        login_otp(otp_code)
            .then(response => {
                localStorage.setItem("accessToken", response["access_token"]);
                console.log(response["access_token"]);
                onLoginSuccess();
            })
            .catch(error => {
                console.log(error);
                setErrorMessage(true);
            });
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="OtpCode" value={otp_code} onChange={handleOtpChange} onClick={hideErrorMessage} />
                {showErrorMessage && <p className="Error-message">Invalid Otp</p>}
                <button type="submit" className="Button-login">Login</button>
            </form>
        </div>
    );
}


async function login_otp(otp_code) {
    const validation_token = localStorage.getItem("otpToken");

    try {
        const response = await fetch('https://twofactorauth-53av.onrender.com/auth/otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({otp_code, validation_token}),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        throw new Error('Error during otp auth:', error);
    }
}

export default OtpForm;
