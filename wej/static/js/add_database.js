/**
 * Created by leeyoungchul on 2017. 6. 11..
 */

function saveData( dataType ) {
    var data = {}

    if( dataType == 'store' ) {

        var call_number = $('#store_first_call_number').val() + '-' + $('#store_middle_call_number').val() + '-' + $('#store_last_call_number').val();

        data['call_number'] = call_number;
        data['keyword'] = $('#' + dataType + '_data_table').find( 'input[name=keyword]' ).val();
        data['name'] = $('#' + dataType + '_data_table').find( 'input[name=name]' ).val();
        data['img_link'] = $('#' + dataType + '_data_table').find( 'input[name=img_link]').val();

    }else if( dataType == 'menu' ){

        data['name'] = $('#' + dataType + '_data_table').find( 'input[name=name]' ).val();

    }else if( dataType == 'store_menu' ){
        if( $('#store_list_selectbox option:selected').val() == 0  ) {
            alert('입력할 가게를 고르세요.');
            return;
        } if( $('#menu_list_selectbox option:selected').val() == 0  ) {
            alert('입력할 메뉴를 고르세요.');
            return;
        }

        data['store_id'] = $('#store_list_selectbox option:selected').val();
        data['menu_id'] = $('#menu_list_selectbox option:selected').val();
        data['price'] = $('#store_menu_info_table input[name=price]').val();
        data['img_link'] = $('#store_menu_img_link').val();
    }

    data['data_type'] = dataType;

    $.ajax({
        url : '/savedatabase',
        method : 'get',
        data : data,
        success : function() {
            alert('정보가 저장되었습니다.');
            $('#' + dataType + '_data_form').find( 'input' ).val('');

            if ( dataType == 'store' ) {
                $('#' + dataType + '_data_form input[name=call_number]').val('');
            }
        },
        error : function() {
            alert('데이터를 불러오던중 오류가 발생했습니다. 잠시후 다시 시도해 주세요');
        }
    });

}

function loadStoreAndMenu( selectboxOption ) {
    $.ajax({
        url : '/loadstoremenuinfo',
        method : 'get',
        data : {'option' : selectboxOption },
        dataType : 'json',
        success : function(data) {
            $('#store_list_'+ selectboxOption +'_selectbox').html( $('<option value="0" selected>가게</option>') );
            $('#menu_list_'+ selectboxOption +'_selectbox').html( $('<option value="0" selected>메뉴</option>') );
            $('#store_menu_info_table input[name=price]').val('');
            console.log( data );
            if( 'storelist' in data && data['storelist'] )
                $.each(data['storelist'], function(idx){
                   var store = data['storelist'][idx];

                   $('#store_list_'+ selectboxOption +'_selectbox').append( $('<option>' + store['name'] + '</option>').val( store['id'] ));
                });

            if( 'menulist' in data && data['menulist'] )
                $.each(data['menulist'], function(idx){
                   var menu = data['menulist'][idx];

                   $('#menu_list_'+ selectboxOption +'_selectbox').append( $('<option>' + menu['name'] + '</option>').val( menu['id'] ));
                });

            $('#store_list_'+ selectboxOption +'_selectbox').prop('disabled', false);
            $('#menu_list_'+ selectboxOption +'_selectbox').prop('disabled', false);

            if( selectboxOption == 'menu' ) {
                $('#store_menu_info_table input[name=price]').prop('disabled', false);
                $('#store_menu_info_table input[name=img_link]').prop('disabled', false);
            }else if(selectboxOption == 'img') {
                $('#store_img_input').prop('disabled', false);
                $('#menu_img_input').prop('disabled', false);
            }
        },
        error : function() {
            alert('데이터를 불러오던중 오류가 발생했습니다. 잠시후 다시 시도해 주세요');
        }
    });
}