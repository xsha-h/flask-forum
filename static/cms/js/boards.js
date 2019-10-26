$(function(){
    // 添加板块的实现
    $("#add-board-btn").on("click", function(event){
        event.preventDefault();
        swal.fire({
            title: '请输入板块名称',
            input: 'text',
            inputAttributes: {
                autocapitalize: 'off'
            },
            cancelButtonText: "取消",
            showCancelButton: true,
            confirmButtonText: '创建',
            showLoaderOnConfirm: true
        }).then((result) => {
            if (result.value) {
                console.log(result.value);
                cpajax.post({
                    "url": "/cms/aboard",
                    "data": {"name": result.value},
                    "success": function(data){
                        if(data["code"] == 200){
                            window.location.reload()
                        }else{
                            swal.fire({
                                type: "error",
                                title: "提示",
                                text: data["message"],
                            })
                        }
                    }
                })
            }
        })
    });
});

$(function(){
    // 编辑按钮的实现
    $(".edit-board-btn").on("click", function(){
        var self = $(this)
        var tr = self.parent().parent();

        var boardId = tr.attr("data-id");
        var name = tr.attr("data-name");


        swal.fire({
            title: '请输入板块名称',
            input: 'text',
            inputAttributes: {
                autocapitalize: 'on',
                placeholder: name,
            },
            cancelButtonText: "取消",
            showCancelButton: true,
            confirmButtonText: '修改',
            showLoaderOnConfirm: true
        }).then((result) => {
            if (result.value) {
                console.log(result.value);
                cpajax.post({
                    "url": "/cms/uboard",
                    "data": {"boardId": boardId, "name": result.value},
                    "success": function(data){
                        if(data["code"] == 200){
                            window.location.reload()
                        }else{
                            swal.fire({
                                type: "error",
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


$(function(){
    // 删除按钮实现
    $(".delete-board-btn").on("click", function(){
        var self = $(this);
        var tr = self.parent().parent();
        var boardId = tr.attr("data-id");
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
            title: '确定删除这个板块?',
            text: "您将无法还原资源",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '是的，删除它！'
        }).then((result) => {
            if (result.value) {
                cpajax.post({
                    "url": "/cms/dboard",
                    "data": {"boardId": boardId},
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
