$(document).ready(function(){

    $('#star_rate').rateYo({
        normalFill: "#d0d0d0",
        ratedFill: "#fdff80",
        numStars: 5,
    }).on("rateyo.set", function (e, data) {
        $('#menu_rate').val(data.rating);
    });;

    $("#star_rate").rateYo().on("rateyo.click", function (e, data) {
        var rating = data.rating;
        $(this).next().text(rating);
    });

    $('#rate_save_btn').on('click', function(){
        rateAdd();
    });
});

function rateAddView( storeId, menuId ) {
    $('#rate_modal_storename').text( $('#store_name').text() );
    $('#rate_modal_menuname').text( $('#menu_' + menuId + '_name').text() );

    $('#menu_rate').val( 0 );
    $('#modal_menu_id').val( menuId );
    $('#modal_store_id').val( storeId );
    $('#rate_save_modal').modal('show');
}

function rateAdd() {
    $.ajax({
        url : '/ratestore',
        type : 'GET',
        data : { 'store_id':$('#modal_store_id').val(), 'menu_id' : $('#modal_menu_id').val(), 'rate' : $('#menu_rate').val() },
        success : function () {
            alert("평점을 저장했습니다.");
            window.location.reload();
        },error : function() {
            alert("평점을 저장중 오류가 발생했습니다.");
        }
    });
}