
// 保存按钮实现
$(function(){
    // 总文件名
    var filename = "";
    //选取的文件名
    var key = "";
    // 存储文件名的前缀
    var domin = "/static/front/images/index_images/";
    //文件信息
    var info = null;
    var formData = new FormData();
    $("#upload-btn").on("click", function(event){
            event.preventDefault();
            var image = $("#image_file");
            image.trigger("click");
        });
        $("#image_file").change(function(){
            info = this.files[0];
            formData.append("image", info);
            key = this.files[0].name;
            filename = domin+key;
            $("input[name=image_url]").val(filename);
            // localfile = window.URL.createObjectURL(document.getElementById("image_file").files.item(0));
            // console.log(localfile);
            // console.log(this);
            // console.log(this.files);
            // console.log(this.value);
        });

    $("#save-banner-btn").on("click", function(event){
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name=name]");
        var imageInput = $("input[name=image_url]");
        var linkInput = $("input[name=link_url]");
        var priorityInput = $("input[name=priority]");

        var name = nameInput.val();
        var image = filename;
        var link = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr("data-type");
        var bannerId = self.attr("data-id");

        var url = "";
        if(submitType == "update"){
            url = "/cms/ubanner"
        }else{
            url = "/cms/abanner"
        }


        cpajax.post({
            "url": url,
            "data": {
                "name": name,
                "image_url": image,
                "link_url": link,
                "priority": priority,
                "bannerId": bannerId,
            },
            "success": function(data){
                dialog.modal("hide");
                if(data["code"] == 200){
                    cpajax.post({
                        "url": "/cms/uploadfile",
                        "data": formData,
                        "processData": false,
                        "contentType": false,
                    });
                    console.log("成功之后：", formData);
                    //重新加载页面
                    window.location.reload();
                }else{
                    swal.fire({
                        type: "error",
                        title: "提示",
                        text: data["message"],
                    })
                }
            },
            "fail": function(){
                swal.fire({
                    type: "error",
                    title: "提示",
                    text: "网络错误",
                })
            }
        })
    })
});

// 编辑按钮实现
$(function(){
    $(".edit-banner-btn").on("click", function(event){
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();

        var name = tr.attr("data-name");
        var image = tr.attr("data-image");
        var link = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name=name]");
        var imageInput = dialog.find("input[name=image_url]");
        var linkInput = dialog.find("input[name=link_url]");
        var priorityInput = dialog.find("input[name=priority]");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image);
        linkInput.val(link);
        priorityInput.val(priority);
        // 绑定属性
        saveBtn.attr("data-type", "update");
        saveBtn.attr("data-id", tr.attr("data-id"));
    })
});

// 删除按钮实现
$(function(){
    $(".delete-banner-btn").on("click", function(){
        var self = $(this);
        var tr = self.parent().parent();
        var bannerId = tr.attr("data-id");
        // swal({
        //     title: "确定删除吗？",
        //     text: "你将无法恢复该虚拟文件！",
        //     type: "warning",
        //     showCancelButton: true,
        //     confirmButtonColor: "#DD6B55",
        //     confirmButtonText: "确定删除！",
        //     cancelButtonText: "取消删除！",
        //     closeOnConfirm: false,
        //     closeOnCancel: false,
        //
        // })
        swal.fire({
            title: '确定删除这个轮播图?',
            text: "您将无法还原资源",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '是的，删除它！'
        }).then((result) => {
            if (result.value) {
                cpajax.post({
                    "url": "/cms/dbanner",
                    "data": {"bannerId": bannerId},
                    "success": function(data){
                        if(data["code"] == 200){
                            swal.fire(
                                '删除！',
                                '轮播图已删除',
                                'success'
                            );
                            window.location.reload();
                        }
                        else{
                            swal({
                                icon: "error",
                                title: "提示",
                                text: data["message"],
                            })
                        }
                    }
                })
            }
        })
    })
});

// 添加图片按钮的实现
// $(function(){
//     // 文件资源名
//     var key = "";
//     // 绑定的域名（这里是测试域名）
//     var domin ="http://pzgczhp1w.bkt.clouddn.com/";
//     // 上传的文件对象
//     var file = "";
//     //token值
//     var token = "";
//     var config = {
//         useCdnDomain: true,
//         region: qiniu.region.z0,
//     };
//     var putExtra = {
//         fname: key,  // 源文件名
//         params: {},
//         mimeType: ["image/png", "image/jpg", "image.gif"]
//     };
//
//     $("#upload-btn").on("click", function(event){
//         event.preventDefault();
//         var image = $("#image_file");
//         image.trigger("click");
//     });
//     $("#image_file").change(function(){
//         key = this.files[0].name;
//         // file = new Blob(key, {type: "image/png"});
//         $("input[name=image_url]").val(domin+key);
//         file = window.URL.createObjectURL(document.getElementById("image_file").files.item(0));
//         console.log(file);
//     });
//     $("#save-banner-btn").on("click", function(){
//         if($("input[name=image_url]") != null){
//             $.get({
//                 "url": "/cms/uptoken",
//                 "success": function(data){
//                     token = data["uptoken"];
//                     var observable = qiniu.upload(file, key, token, putExtra, config);
//                     var observer = {
//                         next(res){
//                             console.log("next:", res);
//                         },
//                         error(err){
//                             console.log("error", err);
//                         },
//                         complete(res){
//                             console.log("complete:", res);
//                         }
//                     };
//                     var subscription = observable.subscribe(observer);
//                 }
//             })
//         }
//     })
// });

