require([
    'jquery'
],function($){
    $('#jointhreads').on('submit',function(e){
        e.preventDefault()
        $.ajax({
            type:'POST',
            url:'jointhreads/',
            data:{
                subject:$('#join_subject').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){
                alert('Successfully joined thread')
                $('#join_subject').val('');
                window.location.reload(true);
            }
        })
    });

    $('#createthreads').on('submit',function(e){
        e.preventDefault()
        $.ajax({
            type:'POST',
            url:'addnewthread/',
            data:{
                subject:$('#create_subject').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(){
                alert('Successfully created thread')
                $('#create_subject').val('');
                window.location.reload(true);
            }
        })
    });

});