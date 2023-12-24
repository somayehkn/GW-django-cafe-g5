   
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
        calculateTotalPrice();
    }

    function calculateTotalPrice() {
        let elements = document.getElementsByClassName("total_price");
        let total = 0;
        for (let i = 0; i < elements.length; i++) {
            total += parseFloat(elements[i].innerText) || 0;
        }

        document.getElementById('total').innerText = total

    }


