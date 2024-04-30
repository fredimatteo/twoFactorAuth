import React, {useState, useEffect} from 'react';

const UserListView = () => {
    const [userData, setUserData] = useState([]);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem('accessToken');
                const response = await fetch('http://localhost:8000/users', {
                    headers: {
                        Authorization: `Bearer ${token}` // Includi il token nell'header Authorization
                    }
                });
                if (!response.ok) {
                    throw new Error('Errore durante il recupero dei dati');
                }
                const data = await response.json();
                setUserData(data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchUserData();
    }, []);

    return (
        <div>
            <h1>Dettaglio Utente</h1>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Cognome</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Amministratore</th>
                    <th>Disabilitato</th>
                </tr>
                </thead>
                <tbody>
                {userData.map(user => (
                    <tr key={user.id}>
                        <td>{user.id}</td>
                        <td>{user.first_name}</td>
                        <td>{user.last_name}</td>
                        <td>{user.email}</td>
                        <td>{user.username}</td>
                        <td>{user.is_admin ? 'Sì' : 'No'}</td>
                        <td>{user.disabled ? 'Sì' : 'No'}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default UserListView;
