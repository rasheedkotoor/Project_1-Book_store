//-----------------------------------------------------//
//---------cart count adding front and back----------- //
//-----------------------------------------------------//
$(".button").on("click", function() {
    var $button = $(this);
    cartid = $(this).attr("data-cartid");
    var oldValue = $('#qty-'+cartid).val();

    if ($button.text() == "+") {
        var newVal = parseFloat(oldValue) + 1;
    } else {
        if (oldValue > 1) {
            var newVal = parseFloat(oldValue) - 1;
        } else {
            newVal = 1;
        }
    }
    $('#qty-'+cartid).val(newVal);
    $("#here").load(" #here > *");
});
$(".button").click(function() {
    var $button = $(this);
    var cartid = $(this).attr("data-cartid");
    var qty = $('#qty-'+cartid).val();
    var price = $('#price-'+cartid).attr("data-price");
    var disc_price = $('#disc_price-'+cartid).attr("data-disc_price");
    var total = qty * disc_price;
    document.getElementById('total-'+cartid).innerHTML = total;
    $("#here").load(" #here > *");

    var data = {
    'qty' : qty,
    'pk' : cartid,
    }
    $.ajax({
        url:'/cart_count/',
        method:'POST',
        data: data,
        success:function(data){
            if (data == 'true'){
                window.location.replace('/cart/')
            }
        }
    });
});
//$(document).ready(function () {
//    var cartid = $('.button').attr("data-cartid");
//    var qty = $('#qty-'+cartid).val();
//    var price = $('#price-'+cartid).attr("data-price");
//    var disc_price = $('#disc_price-'+cartid).attr("data-disc_price");
//    var total = qty * disc_price;
//    document.getElementById('total-'+cartid).innerHTML = total;
//});
//-----------------------------------------------------//
//-------------------Billing Address ----------------- //
//-----------------------------------------------------//
