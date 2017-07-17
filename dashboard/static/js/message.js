require([
    'jquery',
    'longpoll'
],function($, longpoll){
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
                $('#threads_joined').append('<a class="list-group-item" href="'+json.thread_url+'">'+json.subject+'</a>');
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
            success:function(json){
                if(json.thread_url===undefined){
                    alert('The thread already exists!');
                    $('#create_subject').val('');
                }

                else{
                    alert('Successfully created thread')
                    $('#create_subject').val('');
                    $('#threads_joined').append('<a class="list-group-item" href="'+json.thread_url+'">'+json.subject+'</a>');
                }                
            }
        })
    });

    $('#send_message').on('submit', function(e){
        e.preventDefault();
        longpoll.restart();
        $.ajax({
            url : $('#send_message').attr('action'),
            type : 'POST',
            data : $('#send_message').serialize(),

            success : function(json){
                $('#content').val('');
                alert("message sent!")
            }
        });
    });
    longpoll.fetch();
});