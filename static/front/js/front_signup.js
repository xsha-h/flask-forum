$(function(){

    //图形验证码的动态刷新
   $("#captcha-img").on("click", function(){
       var self = $(this);
       var src = self.attr("src");
       var newsrc = cpparam.setParam(src, "xx", Math.random());
       self.attr("src", newsrc);
   });

   // 发送手机验证码的实现
   // $("#sms-captcha-btn").on("click", function(event){
   //     event.preventDefault();
   //     var self = $(this);
   //     var telephone = $("input[name=telephone]").val();
   //     if(!(/^1[345789]\d{9}$/.test(telephone))){
   //         swal("请输入正确格式的手机号", {
   //             icon: "error",
   //             button: false,
   //             timer: 2000,
   //         });
   //         return;
   //     }
   //
   //     var timestamp = (new Date).getTime();
   //     var sign = md5(timestamp+telephone+"347tgfreuydx9384t5rei3458923");
   //
   //     cpajax.post({
   //         "url": "/common/sms_captcha",
   //         "data":{
   //              "telephone": telephone,
   //              "timestamp": timestamp,
   //              "sign": sign,
   //         },
   //         "success": function(data){
   //             if(data["code"] == 200){
   //                 swal("短信验证码发送成功", {
   //                     icon: "success",
   //                     button: false,
   //                     timer: 2000,
   //                 });
   //                 self.attr("disables", "disabled");
   //                 var timeCount = 60;
   //                 var timer = setInterval(function(){
   //                     timeCount--;
   //                     self.text("验证码（"+timeCount+"）");
   //                     if(timeCount <= 0){
   //                         self.removeAttr("disabled");
   //                         clearInterval(timer);
   //                         self.text("发送验证码");
   //                     }
   //                 }, 1000)
   //             }else{
   //                 swal({
   //                      icon: "error",
   //                      title: "提示",
   //                      text: data["message"],
   //                  })
   //             }
   //         }
   //     })
   // })

   // 对上面的代码进行加密混淆
   ;window["\x65\x76\x61\x6c"](function(FtgzDn1,sGFikQLZ2,weHJaV3,M4,kbpkZy5,hQGeXjpTF6){kbpkZy5=function(weHJaV3){return(weHJaV3<sGFikQLZ2?'':kbpkZy5(window["\x70\x61\x72\x73\x65\x49\x6e\x74"](weHJaV3/sGFikQLZ2)))+((weHJaV3=weHJaV3%sGFikQLZ2)>35?window["\x53\x74\x72\x69\x6e\x67"]['\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65'](weHJaV3+29):weHJaV3['\x74\x6f\x53\x74\x72\x69\x6e\x67'](36))};if(!''['\x72\x65\x70\x6c\x61\x63\x65'](/^/,window["\x53\x74\x72\x69\x6e\x67"])){while(weHJaV3--)hQGeXjpTF6[kbpkZy5(weHJaV3)]=M4[weHJaV3]||kbpkZy5(weHJaV3);M4=[function(kbpkZy5){return hQGeXjpTF6[kbpkZy5]}];kbpkZy5=function(){return'\\\x77\x2b'};weHJaV3=1};while(weHJaV3--)if(M4[weHJaV3])FtgzDn1=FtgzDn1['\x72\x65\x70\x6c\x61\x63\x65'](new window["\x52\x65\x67\x45\x78\x70"]('\\\x62'+kbpkZy5(weHJaV3)+'\\\x62','\x67'),M4[weHJaV3]);return FtgzDn1}('\x24\x28\x22\x23\x6f\x2d\x70\x2d\x71\x22\x29\x2e\x72\x28\x22\x73\x22\x2c\x61\x28\x68\x29\x7b\x68\x2e\x74\x28\x29\x3b\x32 \x34\x3d\x24\x28\x75\x29\x3b\x32 \x33\x3d\x24\x28\x22\x76\x5b\x77\x3d\x33\x5d\x22\x29\x2e\x78\x28\x29\x3b\x62\x28\x21\x28\x2f\x5e\x31\x5b\x79\x5d\\\x64\x7b\x39\x7d\x24\x2f\x2e\x7a\x28\x33\x29\x29\x29\x7b\x63\x28\x22\u8bf7\u8f93\u5165\u6b63\u786e\u683c\u5f0f\u7684\u624b\u673a\u53f7\x22\x2c\x7b\x65\x3a\x22\x69\x22\x2c\x6a\x3a\x6b\x2c\x35\x3a\x6c\x2c\x7d\x29\x3b\x41\x7d\x32 \x36\x3d\x28\x42 \x43\x29\x2e\x44\x28\x29\x3b\x32 \x66\x3d\x45\x28\x36\x2b\x33\x2b\x22\x46\x22\x29\x3b\x47\x2e\x48\x28\x7b\x22\x49\x22\x3a\x22\x2f\x4a\x2f\x4b\x22\x2c\x22\x37\x22\x3a\x7b\x22\x33\x22\x3a\x33\x2c\x22\x36\x22\x3a\x36\x2c\x22\x66\x22\x3a\x66\x2c\x7d\x2c\x22\x6d\x22\x3a\x61\x28\x37\x29\x7b\x62\x28\x37\x5b\x22\x4c\x22\x5d\x3d\x3d\x4d\x29\x7b\x63\x28\x22\u77ed\u4fe1\u9a8c\u8bc1\u7801\u53d1\u9001\u6210\u529f\x22\x2c\x7b\x65\x3a\x22\x6d\x22\x2c\x6a\x3a\x6b\x2c\x35\x3a\x6c\x2c\x7d\x29\x3b\x34\x2e\x4e\x28\x22\x4f\x22\x2c\x22\x6e\x22\x29\x3b\x32 \x38\x3d\x50\x3b\x32 \x35\x3d\x51\x28\x61\x28\x29\x7b\x38\x2d\x2d\x3b\x34\x2e\x67\x28\x22\u9a8c\u8bc1\u7801\uff08\x22\x2b\x38\x2b\x22\uff09\x22\x29\x3b\x62\x28\x38\x3c\x3d\x30\x29\x7b\x34\x2e\x52\x28\x22\x6e\x22\x29\x3b\x53\x28\x35\x29\x3b\x34\x2e\x67\x28\x22\u53d1\u9001\u9a8c\u8bc1\u7801\x22\x29\x7d\x7d\x2c\x54\x29\x7d\x55\x7b\x63\x28\x7b\x65\x3a\x22\x69\x22\x2c\x56\x3a\x22\u63d0\u793a\x22\x2c\x67\x3a\x37\x5b\x22\x57\x22\x5d\x2c\x7d\x29\x7d\x7d\x7d\x29\x7d\x29',59,59,'\x7c\x7c\x76\x61\x72\x7c\x74\x65\x6c\x65\x70\x68\x6f\x6e\x65\x7c\x73\x65\x6c\x66\x7c\x74\x69\x6d\x65\x72\x7c\x74\x69\x6d\x65\x73\x74\x61\x6d\x70\x7c\x64\x61\x74\x61\x7c\x74\x69\x6d\x65\x43\x6f\x75\x6e\x74\x7c\x7c\x66\x75\x6e\x63\x74\x69\x6f\x6e\x7c\x69\x66\x7c\x73\x77\x61\x6c\x7c\x7c\x69\x63\x6f\x6e\x7c\x73\x69\x67\x6e\x7c\x74\x65\x78\x74\x7c\x65\x76\x65\x6e\x74\x7c\x65\x72\x72\x6f\x72\x7c\x62\x75\x74\x74\x6f\x6e\x7c\x66\x61\x6c\x73\x65\x7c\x32\x30\x30\x30\x7c\x73\x75\x63\x63\x65\x73\x73\x7c\x64\x69\x73\x61\x62\x6c\x65\x64\x7c\x73\x6d\x73\x7c\x63\x61\x70\x74\x63\x68\x61\x7c\x62\x74\x6e\x7c\x6f\x6e\x7c\x63\x6c\x69\x63\x6b\x7c\x70\x72\x65\x76\x65\x6e\x74\x44\x65\x66\x61\x75\x6c\x74\x7c\x74\x68\x69\x73\x7c\x69\x6e\x70\x75\x74\x7c\x6e\x61\x6d\x65\x7c\x76\x61\x6c\x7c\x33\x34\x35\x37\x38\x39\x7c\x74\x65\x73\x74\x7c\x72\x65\x74\x75\x72\x6e\x7c\x6e\x65\x77\x7c\x44\x61\x74\x65\x7c\x67\x65\x74\x54\x69\x6d\x65\x7c\x6d\x64\x35\x7c\x33\x34\x37\x74\x67\x66\x72\x65\x75\x79\x64\x78\x39\x33\x38\x34\x74\x35\x72\x65\x69\x33\x34\x35\x38\x39\x32\x33\x7c\x63\x70\x61\x6a\x61\x78\x7c\x70\x6f\x73\x74\x7c\x75\x72\x6c\x7c\x63\x6f\x6d\x6d\x6f\x6e\x7c\x73\x6d\x73\x5f\x63\x61\x70\x74\x63\x68\x61\x7c\x63\x6f\x64\x65\x7c\x32\x30\x30\x7c\x61\x74\x74\x72\x7c\x64\x69\x73\x61\x62\x6c\x65\x73\x7c\x36\x30\x7c\x73\x65\x74\x49\x6e\x74\x65\x72\x76\x61\x6c\x7c\x72\x65\x6d\x6f\x76\x65\x41\x74\x74\x72\x7c\x63\x6c\x65\x61\x72\x49\x6e\x74\x65\x72\x76\x61\x6c\x7c\x31\x30\x30\x30\x7c\x65\x6c\x73\x65\x7c\x74\x69\x74\x6c\x65\x7c\x6d\x65\x73\x73\x61\x67\x65'['\x73\x70\x6c\x69\x74']('\x7c'),0,{}));

   //注册按钮的实现
    $("#submit").on("click", function(event){
        event.preventDefault();
        var telephone_input = $("input[name=telephone]");
        var sms_captcha_input = $("input[name=sms_captcha]");
        var username_input = $("input[name=username]");
        var password1_input = $("input[name=password1]");
        var password2_input = $("input[name=password2]");
        var graph_captcha_input = $("input[name=graph_captcha]");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        cpajax.post({
            "url": "/signup",
            "data": {
                "telephone": telephone,
                "sms_captcha": sms_captcha,
                "username": username,
                "password1": password1,
                "password2": password2,
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
            },
            "fail": function(){
                swal.fire({
                    type: "error",
                    title: "提示",
                    text: "网络错误",
                });
            }
        })
    })

});
