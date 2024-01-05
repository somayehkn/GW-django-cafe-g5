   
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

    async function redirectToCheckout(){
        let is_empty = await SendJsonToServer()
        if (is_empty == true){
            alert("سبد خرید شما خالی است.")
        } else{
            await redirect("shoping-cart")
        }
    }

    async function redirectToCat(cat){
        await SendJsonToServer()
        await redirect(`menu?cat=${cat}`);
    }

    function createJson() {
        let dataToSend = {};
        let elements = document.querySelectorAll(".col");        
        elements.forEach(element => {
            let item_name = element.id;
            let item_unit_price = parseFloat(document.getElementById("unitprice_" + item_name).textContent);
            let item_quantity = parseInt(document.getElementById("quantity_"+ item_name).textContent, 10);
            let item_total_price = item_unit_price * item_quantity;

            if (item_quantity > 0){
                dataToSend[item_name] = {
                    item_unit_price: item_unit_price,
                    item_quantity: item_quantity,
                    item_total_price: item_total_price
                };
            }
                
        });
        return dataToSend;
    }

    

    

    

    

    

   
    



