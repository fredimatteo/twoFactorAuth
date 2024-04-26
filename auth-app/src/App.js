import React, {useState} from 'react';
import './App.css';

function App() {
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showSignupForm, setShowSignupForm] = useState(false);

    const handleLoginClick = () => {
        setShowLoginForm(true);
        setShowSignupForm(false);
    };

    const handleSignupClick = () => {
        setShowLoginForm(false);
        setShowSignupForm(true);
    };

    return (
        <div className="App">
            <header className="App-header">
                <div className="Button-container">
                    <h1 className="Welcome-message">Welcome</h1>
                    <button onClick={handleLoginClick} className="Button-login">Login</button>
                    <button onClick={handleSignupClick} className="Button-signup">Sign Up</button>
                    {showLoginForm && <LoginForm/>}
                    {showSignupForm && <SignupForm/>}
                </div>
            </header>
        </div>
    );
}

function LoginForm() {
    return (
        <div>
            <form>
                <label>
                    Username:
                    <input type="text"/>
                </label>
                <label>
                    Password:
                    <input type="password"/>
                </label>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

function SignupForm() {
    return (
        <div>
            <h2>Form di Registrazione</h2>
            <form>
                <label>
                    Nome:
                    <input type="text"/>
                </label>
                <label>
                    Email:
                    <input type="email"/>
                </label>
                <label>
                    Password:
                    <input type="password"/>
                </label>
                <button type="submit">Registrati</button>
            </form>
        </div>
    );
}

export default App;
