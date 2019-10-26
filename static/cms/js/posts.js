$(function(){
    $(".highlight-btn").on("click", function(){
        var self =$(this);
        var tr = self.parent().parent();
        var postId = tr.attr("data-id");
        var hightlight = parseInt(tr.attr("data-highlight"));

        var url = "";
        if(hightlight){
            url = "/cms/uhpost";
        }else{
            url = "/cms/hpost";
        }
        cpajax.post({
            "url": url,
            "data": {
                "postId": postId,
            },
            "success": function(data){
                if(data["code"] == 200){
                    swal.fire({
                        title: '操作成功！',
                        timer: 500,
                        type: "success",
                    });
                    setTimeout(function(){
                        window.location.reload();
                    }, 200);
                }else{
                    swal.fire({
                        type: "error",
                        title: "提示",
                        text: data["message"],
                    })
                }
            }
        })
    })
});