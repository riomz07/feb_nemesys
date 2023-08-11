$(function(){

    $('.task-checkbox-default').on('click',function(){
        let task_id = $(this).val()
        console.log(task_id)
        $.ajax({
            type:'GET',
            url:'/daily-task/task-staff-update',
            data:{'task_id':task_id},
            dataType: 'html',
            success:function(){
                console.log('Success update task')
            }
                
        })
    })


})