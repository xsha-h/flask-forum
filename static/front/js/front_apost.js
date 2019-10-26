$(function(){
    $("#submit-btn").on("click", function(event){
        event.preventDefault();

        var titleInput = $("input[name=title]");
        var boardSelect = $("select[name=boardId]");

        var title = titleInput.val();
        var boardId = boardSelect.val();
        var content = CKEDITOR.instances.content.getData();

        cpajax.post({
            "url": "/apost",
            "data": {
                "title": title,
                "boardId": boardId,
                "content": content,
            },
            "success": function(data){
                console.log(data["code"]);
                if(data["code"] == 200){
                    swal.fire({
                        title: 'OK',
                        text: "恭喜，您的帖子发表成功！",
                        type: 'success',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: '再发一篇',
                        cancelButtonText: '返回首页',
                    }).then((result) => {
                        if (result.value) {
                            titleInput.val();
                            boardId.val();
                            CKEDITOR.instances.content.setData();
                        }else {
                            window.location = "/"
                        }
                    })
                }
            },
        });
    })
});