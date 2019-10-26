$(function(){
    $("#comment-btn").on("click", function(event){
        event.preventDefault();
        var login_tag = $("#login-tag").attr("data-login-tag");
        if(!login_tag){
            window.location = "/signin";
        }else{
            var content = CKEDITOR.instances.content.getData();
            var postId = $("#post-content").attr("data-id");
            cpajax.post({
                "url": "/acomment",
                "data": {
                    "postId": postId,
                    "content": content,
                },
                "success": function(data){
                    if(data["code"] == 200){
                        window.location.reload();
                    }else{
                        swal.fire({
                            type: "error",
                            title: "失败",
                            text: "评论发表失败， 请重新发表...",
                            button: false,
                            timer: 2000,
                       });
                    }
                }
            })
        }
    })
});