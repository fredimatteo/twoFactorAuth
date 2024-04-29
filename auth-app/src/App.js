import React, {useState} from 'react';
import './App.css';
import LoginForm from './custom_js/LoginForm';

function App() {
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showSignupForm, setShowSignupForm] = useState(false);
    const [showHomeSection, setShowHomeSection] = useState(true);

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
                {showLoginForm && <LoginForm/>}
                {showSignupForm && <SignupForm/>}
            </header>

        </div>
    );
}

function SignupForm() {
    return (
        <div>
            <h2>Sign Up</h2>
            <form>
                <input type="text" placeholder="First Name"/>
                <input type="text" placeholder="Last Name"/>
                <input type="email" placeholder="Email"/>
                <input type="text" placeholder="Username"/>
                <input type="password" placeholder="Password"/>
                <button type="submit" className="Button-signup">Sign Up</button>
            </form>
        </div>
    );
}

export default App;
