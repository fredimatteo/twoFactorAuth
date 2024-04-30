// OtpForm.js

import React, {useState} from 'react';
import HandleGetUsers from './Users';

function OtpForm() {
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
                localStorage.setItem("otpToken", response["otp_token"]);
                // HandleGetUsers();
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
        const response = await fetch('http://127.0.0.1:8000/auth/otp', {
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
