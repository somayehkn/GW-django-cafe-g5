

document.addEventListener("DOMContentLoaded", function() {
    var totalPrices = document.querySelectorAll("[id^='checkout_total_price_item']");

    var sum = 0;
    totalPrices.forEach(function(element) {
        sum += parseFloat(element.textContent || element.innerText);
    });

    var totalPriceElement = document.getElementById("checkout_total_price");
    if (totalPriceElement) {
        totalPriceElement.innerHTML = sum.toString() + "T";
    }
});

