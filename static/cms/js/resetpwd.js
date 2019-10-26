$(function(){
    // 表单验证输入的旧密码、新密码、确认密码（处理交给后台，前台只需获取参数即可）
    $("#submit").on("click", function(event){
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        //1、要在模板中的meta标签中渲染一个csrf-token
        //2、在ajax请求的头部设置x-CSRFtoken
        cpajax.post({
            "url": "/cms/resetpwd",
            "data": {
                "oldpwd": oldpwd,
                "newpwd": newpwd,
                "newpwd2": newpwd2
            },
            "success": function(data){
                if(data["code"] == 200){
                    swal.fire({
                       title: "成功",
                       type: "success",
                       text: "修改密码成功",
                       button: false,
                       timer: 2000,
                   });
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }else{
                    var message = data["message"];
                    swal.fire({
                        type: "error",
                        title: "提示",
                        text: message,
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