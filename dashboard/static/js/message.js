require([
    'jquery',
    'mustache.min',
    'longpoll'
],function($,Mustache,longpoll){
    var userId = $('[name=user_pk]').val();
    $('#jointhreads').on('submit',function(e){
        e.preventDefault()

        var jt_template = "<a class='list-group-item' href='{{thread_url}}' >{{subject}}</a> ";
        var $jt_threads = $('#threads_joined');
        var $jt_textfield = $('#join_subject');

        $.ajax({
            type:'POST',
            url:'jointhreads/',
            data:{
                subject: $jt_textfield.val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){
                $(".listallthreads ul li:contains("+ json.subject+")").remove();
                alert('Successfully joined thread')
                $jt_textfield.val('');
                $jt_threads.append(Mustache.render(jt_template,json));
            }
        })
    });

    $('#createthreads').on('submit',function(e){
        e.preventDefault()
        
        var ct_template = "<a class='list-group-item' href='{{thread_url}}' >{{subject}}</a> ";
        var $ct_threads = $('#threads_joined');
        var $ct_textfield = $('#create_subject');

        $.ajax({
            type:'POST',
            url:'addnewthread/',
            data:{
                subject: $ct_textfield.val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){
                if(json.thread_url===undefined){
                    alert('The thread already exists!');
                    $ct_textfield.val('');
                }

                else{
                    alert('Successfully created thread');
                    $ct_textfield.val('');
                    $ct_threads.append(Mustache.render(ct_template,json));
                }                
            }
        })
    });

    $('#send_message').on('submit', function(e){
        e.preventDefault();
        longpoll.restart();
      
        var $sm_textarea = $('#send_message');
        var $sm_content = $('#content');
        var $messages = $('.messages');

        $.ajax({
            url : $sm_textarea.attr('action'),
            type : 'POST',
            data : $sm_textarea.serialize(),

            success : function(json){
                $sm_content.val('');
                console.log(userId);
                console.log(json);
                var template = $('#message-template');
                if(userId == json.sender_pk){
                    json.classes = "user-message";
                }
                var render = Mustache.render(template.html(), json);
                console.log(render);
                $('.messages').append(render);
            }
        });
    });
    longpoll.fetch();
});