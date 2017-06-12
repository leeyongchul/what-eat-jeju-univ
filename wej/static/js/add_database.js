/**
 * Created by leeyoungchul on 2017. 6. 11..
 */

$(document).ready(function(){

});

function saveData( dataType ) {
    var data = {}

    if( dataType == 'store' ) {

        var call_number = $('#store_first_call_number').val() + '-' + $('#store_middle_call_number').val() + '-' + $('#store_last_call_number').val();

        data['call_number'] = call_number;
        data['keyword'] = $('#' + dataType + '_data_form').find( 'input[name=keyword]' ).val();
        data['name'] = $('#' + dataType + '_data_form').find( 'input[name=name]' ).val();

    }else if( dataType == 'menu' ){

    }else if( dataType == 'store_menu' ){

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

        }
    });

}