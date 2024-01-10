
function remove(elementId) {
    elementToRemove = document.getElementById(elementId);
    let userConfirmed = window.confirm("Are you sure to delete this element?");
    if (userConfirmed) {
        elementToRemove.remove();
        let rows = document.querySelectorAll('.item_row');
        if (rows.length == 0) {
            let cardBody = document.querySelector('.card-body');
            cardBody.parentNode.removeChild(cardBody);
        
            let newElement = document.createElement('div');
            newElement.className = 'empty-cart-message';
            newElement.innerHTML = '<p>Your shopping cart is empty.</p><p>You can go to the following pages to see more products:</p>';
            newElement.style.fontWeight = "bold"

            
            let menuButton = document.createElement('button');
            menuButton.type = 'button';
            menuButton.className = 'btn btn-lg btn-default md-btn-flat mt-2 mr-3';
            menuButton.style.backgroundColor = '#FFF1CF';
            menuButton.style.marginBottom = '5px';
            menuButton.style.fontWeight = "bold"
            menuButton.innerHTML = 'Categories Page';
            menuButton.onclick = function() {
              let menuPageURL = '/categories/'; 
              window.location.href = menuPageURL;
              SendJsonToServer()
            };
        
            newElement.appendChild(menuButton);
        
            var parentContainer = document.querySelector('.card');
            parentContainer.appendChild(newElement);
            return true;
          }
    }  else {
        return false;
    }
}


function updateTotal(itemId) {
    const quantityElement = document.getElementById('quantity_' + itemId);
    const quantity = parseInt(quantityElement.value, 10);
    if (quantity >= 1) {
        const unitPriceElement = document.getElementById('unitprice_' + itemId);
        const unitPrice = parseFloat(unitPriceElement.innerHTML);
        const total = quantity * unitPrice;
        document.getElementById('total_price_' + itemId).innerText = total;
    } else {
        if (!remove(itemId)) {

            quantityElement.value = 1;
        }
    }
    }
    

async function SendJsonToServer(){
    let data = await createJson();
    let is_empty = await SendToServer(data);
    return is_empty;
}

async function redirectToCheckout(){
    await SendJsonToServer()
    await redirect("/checkout-page/")
}

function createJson() {
    let dataToSend = {};
    let elements = document.querySelectorAll(".item_row");        
    elements.forEach(element => {
        let item_name = element.id;
        let item_unit_price = parseFloat(document.getElementById("unitprice_" + item_name).innerHTML);
        let item_quantity = parseInt(document.getElementById("quantity_"+ item_name).value, 10);
        let item_total_price = item_unit_price * item_quantity;
        let image = document.getElementById("image_"+ item_name).src

        if (item_quantity > 0){
            dataToSend[item_name] = {
                item_unit_price: item_unit_price,
                item_quantity: item_quantity,
                item_total_price: item_total_price,
                image: image
            };
        }
            
    });
    return dataToSend;
}

function redirect(url) {
    window.location.href = url;
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
    await fetch("/save-cart-items-to-sesion/", requestOptions)
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


