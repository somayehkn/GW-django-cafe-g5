
function redirect( url , param) {
    let redirectURL = url;
    window.location.href = redirectURL;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    } 

async function SendToServer(jsonData){
    const csrfToken = getCookie('csrftoken');
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(jsonData) 
    };
    let is_empty;
    await fetch('save-menu-items-to-sesion', requestOptions)
        .then(response => response.json()) 
        .then(data => {
            if (data["empty"] == true){
                is_empty = true;
            }
            else {
                is_empty = false;
            }
        })
        .catch(error => {
            console.error('Response error: ', error);
        });  
    return is_empty;       
}