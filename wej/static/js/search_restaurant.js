function rateStoreView( storeId, menuId ) {
    $.ajax({
        url : '/ratestore',
        type : 'GET',
        data : { 'store_id':storeId, 'menu_id' : menuId},
        success : function (data) {
            //modal show, storeId, menuId 저장
        }
    });
}

function rateStoreMenu() {
    //가게번호,

    $.ajax({
        url : '/ratestore',
        type : 'GET',
        data : { 'store_id':storeId, 'menu_id' : menuId, 'rate' : rate},
        success : function (data) {
            if( 'resultStatus' in data && data['resultStatus'] ) {
                alert('평점이 저장되었습니다.');
                //modal hide, storeId, menuId 삭제
            }
        }
    });
}