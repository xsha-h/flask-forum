$(function(){
    // 给新邮箱发送验证码
   $("#captcha-btn").on("click", function(event){
       event.preventDefault();
       var email = $("input[name=email]").val();
       if(!email){
           swal.fire({
               title: "提示",
               type: "info",
               text: "请输入邮箱地址!",
               button: false,
               timer: 2000,
           });
           return;
       }
       cpajax.get({
           "url": "/cms/email_captcha",
           "data": {"email": email},
           "success": function(data){
               if(data["code"] == 200){
                   swal.fire({
                       title: "成功",
                       type: "success",
                       text: "修改邮箱成功",
                       button: false,
                       timer: 2000,
                   });
               }else{
                   swal.fire({
                        type: "error",
                        title: "提示",
                        text: data["message"],
                    })
               }
           },
           "fail": function(error){
                swal.fire({
                    type: "error",
                    title: "提示",
                    text: "网络错误",
                })
            }
       })
   })
});

$(function(){

    // 表单验证输入的验证码和接受的验证码是否一样（处理交给后台，前台只需获取参数即可）
    $("#submit").on("click", function(event){
        event.preventDefault();

        var emailE = $("input[name=email]");
        var captchaE = $("input[name=captcha]");

        var email = emailE.val();
        var captcha = captchaE.val();

        cpajax.post({
            "url": "/cms/resetemail",
            "data": {
                "email": email,
                "captcha": captcha,
            },
            "success": function(data){
                if(data["code"] == 200){
                    swal.fire({
                        title: "成功",
                        type: "success",
                        text: "恭喜！修改邮箱成功",
                        button: false,
                        timer: 2000,
                    });
                    emailE.val("");
                    captchaE.val("");
                }else{
                    swal.fire({
                        type: "error",
                        title: "提示",
                        text: data["message"],
                    })
                }
            },
            "fail": function(error){
                swal.fire({
                    type: "error",
                    title: "提示",
                    text: "网络错误",
                })
            }
        });
    })
});