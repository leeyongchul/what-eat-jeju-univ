$(document).ready(function(){
    $.ajax({
        beforeSend : function(xhr){
            xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded; charset=UTF-8");
        }
    });

    $('#search_btn').on('click', function(){
        searchKeyword( $('#search_keyword_input').val() );
    });

    $('#search_keyword_input').keypress(function() {
        if( $(this).keyCode == 13 ) {
            searchKeyword( $(this).val() );
        }
    });

    $('#login_submit').on('click', function(){
        userLogin( $('#user_id').val(), $('#user_pw').val() );
    });

    $('#sign_submit').on('click', function(){
        userSignup();
    });
});

function userSignup() {
    var id = $('#signup_id').val();
    var pw = $('#signup_pw').val();
    var pw2 = $('#signup_pw_check').val();

    if( pw != pw2 ) {
        alert('비밀번호를 확인해주세요.');
        return;
    }

    $.ajax({
        url : '/signup/',
        type : 'POST',
        data : {'id' : id, 'pw' : pw, 'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()},
        dataType : 'json',
        success : function(data) {
            alert('회원가입 되었습니다.\n로그인 후 서비스를 이용하십시오');
            $('#signup_modal').modal('hide');
            $('#login_modal').modal('show');
        },error : function() {
            alert('아이디를 새로 설정하신후 재시도 하십시오');
        }
    });
}

function userLogin( id, pw ) {
    id = id.trim();
    pw = pw.trim();

    if( id.length == 0 && pw.length == 0 ) {
        alert('아이디와 비밀번호를 입력하셔야 합니다.');
        return;
    }

    $.ajax({
        url : '/login/',
        type : 'post',
        data : { 'id' : id, 'pw' : pw, 'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val() },
        success : function() {
            alert( "로그인 되었습니다." );
            window.location.assign('/');
        },error : function () {
            alert( "아이디와 비밀번호를 확인해주세요." );
        }
    });
}

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


function loginModalView() {
    $('#user_id').val('');
    $('#user_pw').val('');
    $('#login_modal').modal('show');
}

function logout() {
    $.ajax({
        url : '/logout',
        type : 'get',
        success : function () {
            alert('로그아웃 되었습니다.');
            window.location.assign('/');
        }
    });
}

function signupModalView() {
    $('#signup_modal').modal('show');
}