import React, {useState} from 'react';
import './App.css';
import LoginForm from './form/LoginForm';
import OtpForm from "./form/OtpForm";
import SignupForm from './form/SignUpForm';
import UserListView from "./view/Users";

function App() {
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showSignupForm, setShowSignupForm] = useState(false);
    const [showHomeSection, setShowHomeSection] = useState(true);
    const [showOtpSection, setOtpSection] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);


    const handleLoginClick = () => {
        setShowLoginForm(true);
        setShowSignupForm(false);
        setShowHomeSection(false);
    };

    const handleSignupClick = () => {
        setShowLoginForm(false);
        setShowSignupForm(true);
        setShowHomeSection(false);
    };

    const handleLoginSuccess = () => {
        setShowLoginForm(false); // Nascondi il modulo di accesso
        setOtpSection(true); // Mostra il modulo OTP
    };

    const handleOtpSuccess = () => {
        setOtpSection(false);
        setIsLoggedIn(true);// Mostra il modulo OTP
};

    return (
        <div className="App">
            <header className="App-header">
                {showHomeSection &&
                    <div className="Button-container">
                        <h1 className="Welcome-message">Welcome</h1>
                        <button onClick={handleLoginClick} className="Button-login">Login</button>
                        <button onClick={handleSignupClick} className="Button-signup">Sign Up</button>
                    </div>
                }
                {showLoginForm && <LoginForm onLoginSuccess={handleLoginSuccess}/>}
                {showSignupForm && <SignupForm/>}
                {showOtpSection && <OtpForm onLoginSuccess={handleOtpSuccess}/>}
                {isLoggedIn && <UserListView />}
            </header>

        </div>
    );
}

export default App;
