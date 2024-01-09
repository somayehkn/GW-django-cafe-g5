function redirect(url) {
  window.location.href = url;
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  } 

async function register_order(){
    let selectElement = document.getElementById("table-number-select");
    let selectedValue = selectElement.value;
    // sendTableNumber(selectedValue);
    await register_order_on_db(selectedValue);
    await redirect('/');
}


async function register_order_on_db(tableNum){
    const csrfToken = getCookie('csrftoken');
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ tableNumber: tableNum }) 
    };

    await fetch("/register-order/", requestOptions)
      .then(response => {
        if (!response.ok) {
          throw new Error(`خطا: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        alert('سفارش شما با موفقیت ثبت شد');
      })
      .catch(error => {
        alert('خطا:', error);
      });
}
