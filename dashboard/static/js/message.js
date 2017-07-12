require([
    'jquery',
    'mustache.min'
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

        $.ajax({
            url : $('#send_message').attr('action'),
            type : 'POST',
            data : $('#send_message').serialize(),

            success : function(json){
                date = String(new Date(json.when));
                $('#content').val('');
                $('.messages').append('<div class="message"><div class="user">'+json.sender+'</div><div class="content"><div class="body">'+json.content+'</div><div class="footer">'+date+'</div></div></div>')
                $('#messages').append(json.data);
                console.log(json);
                alert("message sent!")
            }
        });
    });
});