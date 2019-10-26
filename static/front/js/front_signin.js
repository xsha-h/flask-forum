$(function(){

    //图形验证码的动态刷新
    $("#captcha-img").on("click", function(){
        var self = $(this);
        var src = self.attr("src");
        var newsrc = cpparam.setParam(src, "xx", Math.random());
        self.attr("src", newsrc);
    });

    // 登录按钮的Ajax请求
    $("#submit").on("click", function(event){
        event.preventDefault();

        var telephone_input = $("input[name=telephone]");
        var password_input = $("input[name=password]");
        var remember_input = $("input[name=remember]");
        var graph_captcha_input = $("input[name=graph_captcha]");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.checked ? 1 : 0;
        var graph_captcha = graph_captcha_input.val();

        cpajax.post({
            "url": "/signin",
            "data": {
                "telephone": telephone,
                "password": password,
                "remember": remember,
                "graph_captcha": graph_captcha,
            },
            "success": function(data){
                if(data["code"] == 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = "/";
                    }
                }else{
                    swal.fire({
                        type: "error",
                        title: "提示",
                        text: data["message"],
                    });
                }
            }
        })
    })
});