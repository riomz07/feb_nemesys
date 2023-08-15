$(function(){

    $('#button-create').on('click',function () { 
        $('#form-create').attr('hidden',false)
        $(this).attr('hidden',true)
     })


    $('#select-edit-device').on('change',function(){
        let device_id = $('#select-edit-device').find(":selected").val();
        $.ajax({
            type:'GET',
            url:"/configure/",
            data:{'device_id':device_id},
            dataType: 'html',
            success: function(data){
                $('body').html(data);
                $('#form_edit_network_device').attr('hidden',false)
            },
            error:function(data){
                console.log('error'+data)
            }

        })
    })

    
    $('#select-titles-delete').on('change',function(){
        $('#delete-modal-trigger').attr('hidden',false)
    })


    $('#delete-device').on('click',function(){
        let device_id = $('#select-titles-delete').find(":selected").val();
        $.ajax({
            type:'GET',
            url:"/delete_network_device",
            data:{'device_id':device_id,'delete':'yes'},
            dataType: 'html',
            success: function(data){
                window.scrollTo(0, 0);
                $('body').html(data);
            },
            error:function(data){
                console.log('Gagal Delete Device')
            }

        })
    })


$('#select-task-delete').on('change',function(){
    $('#delete-task-modal-trigger').attr('hidden',false)
})


$('#delete-task').on('click',function(){
    let task_id = $('#select-task-delete').find(":selected").val();
    $.ajax({
        type:'GET',
        url:"/manager/delete-task",
        data:{'task_id':task_id},
        dataType: 'html',
        success: function(data){
            $('body').html(data);
        },
        error:function(data){
            console.log('Gagal Delete Task')
        }

    })
})


$('#select-service-delete').on('change',function(){
    $('#delete-service-modal-trigger').attr('hidden',false)
})


$('#delete-service').on('click',function(){
    let service_id = $('#select-service-delete').find(":selected").val();
    $.ajax({
        type:'GET',
        url:"/manager/delete-service",
        data:{'service_id':service_id},
        dataType: 'html',
        success: function(data){
            $('body').html(data);
        },
        error:function(data){
            console.log('Gagal Delete Service')
        }

    })
})

var myModal = document.getElementById('modal-all-device')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

    
})

