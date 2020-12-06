var updBtns = document.getElementsByClassName("update-cart")

for(var i = 0; i<updBtns.length; i++){
    updBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product_id
        var action = this.dataset.action

        if(user == 'AnonymousUser'){
            cookieHandle(productId, action)
        }else{
            doSomething(productId, action)
         }
    })
}
function cookieHandle(productId, action){
    console.log(productId, action)
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity'] <= 0){
                delete cart[productId]
            }
    }
    if(action=='delete'){
        delete cart[productId]
    }
    console.log('Cart',cart)
    document.cookie = 'cart='+ JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function doSomething(productId, action){
    console.log("user  logged in... yes!!", productId, action)
    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers: {
        'Content-Type': 'application/json',
         'X-CSRFToken': csrftoken,
        },
          body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        location.reload()
    })
}