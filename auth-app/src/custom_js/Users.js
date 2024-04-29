const HandleGetUsers = () => {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            console.error('Access token non disponibile.');
            return;
        }

        fetch('http://127.0.0.1:8000/users', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data:', data);
            // Gestisci i dati ottenuti dalla richiesta
        })
        .catch(error => {
            console.error('Error:', error.message);
            // Gestisci gli errori
        });
    };


export default HandleGetUsers;