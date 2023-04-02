



input.addEventListener('change', ()=>{
    
  

    $.ajax({
        type:'POST',
        url: imageForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){
            console.log('success', response)
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                    Successfully saved and cropped the selected image
                                </div>`
        },
        error: function(error){
            console.log('error', error)
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                    Ups...something went wrong
                                </div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})
