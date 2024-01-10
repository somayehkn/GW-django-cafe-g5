
    function incrementQuantity(itemId) {

        let quantityElement = document.getElementById('quantity_' + itemId);
        let quantity = parseInt(quantityElement.innerText, 10);
        quantity++;        
        quantityElement.innerText = quantity;
        updateTotal(itemId);

    }
    
    function decrementQuantity(itemId) {
        const quantityElement = document.getElementById('quantity_' + itemId);
        let quantity = parseInt(quantityElement.innerText, 10);
        if (quantity > 0) {
            quantity--;        
        }
        
        quantityElement.innerText = quantity;
        updateTotal(itemId);
    }

    function updateTotal(itemId) {
        const quantityElement = document.getElementById('quantity_' + itemId);
        const quantity = parseInt(quantityElement.innerText, 10);
        const unitPriceElement = document.getElementById('unitprice_' + itemId);
        const unitPrice = parseFloat(unitPriceElement.innerText);
        const total = quantity * unitPrice;
        document.getElementById('total_price_' + itemId).innerText = total;
    }

    async function SendJsonToServer(){
        let data = await createJson();
        let is_empty = await SendToServer(data);
        return is_empty;
    }

    async function redirectToCart(){
        let is_empty = await SendJsonToServer()
        if (is_empty == true){
            alert("Your shopping cart is empty.")
        } else{
            await redirect("/shoping-cart/")
        }
    }

    async function redirectToCat(foo){
        await SendJsonToServer()
        let url = '/menu/' + encodeURIComponent(foo);
        console.log(url)
        await redirect(url)
        }

    function createJson() {
        let dataToSend = {};
        let elements = document.querySelectorAll(".col");        
        elements.forEach(element => {
            let item_name = element.id;
            let item_unit_price = parseFloat(document.getElementById("unitprice_" + item_name).textContent);
            let item_quantity = parseInt(document.getElementById("quantity_"+ item_name).textContent, 10);
            let item_total_price = item_unit_price * item_quantity;
            let image = document.getElementById("image_"+ item_name).src

            dataToSend[item_name] = {
                item_unit_price: item_unit_price,
                item_quantity: item_quantity,
                item_total_price: item_total_price,
                image: image
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
        await fetch("/save-menu-items-to-sesion/", requestOptions)
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


    function search(cat) {
        let searchQuery = document.getElementById('search-input').value;
        let url = '/menu/' + encodeURIComponent(cat) + "?search=" + encodeURIComponent(searchQuery);
        console.log(url)
        redirect(url)
      }