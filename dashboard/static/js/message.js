require([
    'jquery',
    'mustache.min'
],function($,Mustache){
    
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
                alert('Successfully joined thread')
                $jt_textfield.val('');
                $threads.append(Mustache.render(jt_template,json));
            }
        })
    });

    $('#createthreads').on('submit',function(e){
        e.preventDefault()
        
        var ct_template = "<a class='list-group-item' href='{{thread_url}}' >{{subject}}</a> ";
        var $ct_threads = $('#threads');
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
                    alert('Successfully created thread')
                    $textfield.val('');
                    $threads.append(Mustache.render(ct_template,json));
                }                
            }
        })
    });

    $('#send_message').on('submit', function(e){
        e.preventDefault();

        var $sm_textarea = $('#send_message');
        var $sm_content = $('#content');
        var $messages = $('.messages');
        var message_template = "<div class='message'><div class='user'>{{sender}}</div>"+
            "<div class='content'><div class='body'>{{content}}</div>";


        $.ajax({
            url : $sm_textarea.attr('action'),
            type : 'POST',
            data : $sm_textarea.serialize(),

            success : function(json){
                date = String(new Date(json.when));
                console.log(date);
                message_template = message_template + "<div class='footer'>"+ date +"</div></div></div>";
                $sm_content.val('');
                $messages.append(Mustache.render(message_template,json));
                alert("message sent!")
            }
        });
    });
});