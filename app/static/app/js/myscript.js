$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Plus operation ke liye

$('.plus-cart').click(function () {
    console.log('button click');
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity,
            document.getElementById('amount').innerText = data.amount,
            document.getElementById('shipping').innerText = data.shipping,
            document.getElementById('total').innerText = data.total
        
        },

    })
})

// Minus oparetion ke liye

$('.minus-cart').click(function () {
    console.log('button click');
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity,
            document.getElementById('amount').innerText = data.amount,
            document.getElementById('shipping').innerText = data.shipping,
            document.getElementById('total').innerText = data.total
        
        },

    })
})


$('.remove-cart').click(function () {
    console.log('button click');
    var id = $(this).attr('pid').toString();
    var eml = this
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById('amount').innerText = data.amount,
            document.getElementById('shipping').innerText = data.shipping,
            document.getElementById('total').innerText = data.total
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        
        },

    })
})