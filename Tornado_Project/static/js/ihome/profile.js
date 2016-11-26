function showSuccessMsg() {
    $('.save_success').fadeIn('fast', function() {
        setTimeout(function(){
            $('.save_success').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    //上传头像
    $("#form-avatar").submit(function(e){
        e.preventDefault();
        $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }
            }
        };
        $(this).ajaxSubmit(options);
    });
    //保存用户名
    $("#form-name").submit(function(e){
        e.preventDefault();
        name = $("#user-name").val()
        var req_data ={
            user_name:name
        }
        if (!name) {
            $(".error-msg").text("请填写用户名！");
            $(".error-msg").show();
            return;
        }
        var options = {
            url:"/api/profile/name",
            type:"POST",
            data:JSON.stringify(req_data),
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success:function(data){
                if ("4003" == data.errno){
                    $(".error-msg").show();
                    return;
                }
                else {
                    $(".popup_con").fadeIn("fast");
                    location.href = "/";
                    return;
                }
            }
        } 
    })
    
})