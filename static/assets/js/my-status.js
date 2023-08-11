$(function () {
    $('.reason-box').prop('hidden', true)
    $('.reason-label').prop('hidden', true)

    //Ketika N-Ready di click
    $('.checkbox-nready').on('click',function () {
      //Jika tercentang
      if ($(this).prop('checked')) {
        $('.checkbox-ready').prop('checked', false)
        $('.reason-box').prop('hidden', false)
        $('.reason-label').prop('hidden', false)
        $('.submit-nready').prop('disabled', false)
        $('.reason-box').val('')
      }
      //Jika tidak dicentang
      else {
        $('.checkbox-ready').prop('checked', true)
        $('.reason-label').prop('hidden', true)
        $('.reason-box').prop('hidden', true)
        $('.reason-box').val('Available')
      }
    })
    //Ketika Ready di click
    $('.checkbox-ready').on('click',function () {
      //Jika tercentang
      if ($(this).prop('checked')) {
        $('.checkbox-nready').prop('checked', false)
        $('.reason-box').prop('hidden', true)
        $('.reason-label').prop('hidden', true)
        $('.reason-box').val('Available')
        $('.submit-nready').prop('disabled', false)
      }
      //Jika tidak dicentang
      else {
        $('.checkbox-nready').prop('checked', true)
        $('.submit-nready').prop('disabled', false)
        $('.reason-box').prop('hidden', false)
        $('.reason-label').prop('hidden', false)
        $('.reason-box').val('')
      }
    })

    //Progress Value 
    let value_progress = $('#id_progress').val()
    $('.progress-value').text('Progress : '+value_progress)
    $('#id_progress').on('input', function(){
        let value_progress = $('#id_progress').val()
          $('.progress-value').text('Progress : '+ value_progress)
        if (value_progress == 100) {
          $('#submit-mission').text('Finish')
          $('#submit-mission').attr('data-bs-target','#finish-modal')
          $('#submit-mission').attr('type','button')
        
        }else{
          $('#submit-mission').text('Update Mission')
          $('#submit-mission').attr('data-bs-target','')
        }
    } )


  })