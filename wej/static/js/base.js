$(document).ready(function(){
    $('#search_btn').on('click', function(){
        searchKeyword( $('#search_keyword_input').val() );
    });

    $('#search_keyword_input').keypress(function() {
        if( $(this).keyCode == 13 ) {
            searchKeyword( $(this).val() );
        }
    });
});

function searchKeyword( keyword ) {
    keyword = keyword.trim();

    if( keyword.length == 0 ) {
        alert('검색 키워드는 공백이 될 수 없습니다.\n키워드 입력후 다시 시도해 주세요');
        return;
    }

    // var searchform = $('<form action="/searchrestaurant" method="POST"></form>').append( $('<input name="keyword"></input>').val(keyword) );
    $('#keyword_input').val( keyword );
    $('#search_keyword_form').submit();
}
