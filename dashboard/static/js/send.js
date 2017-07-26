require([
    'jquery',
    'mustache.min'
],function($,Mustache){
    $('#send').attr('disabled','disabled');
    var userId = $('[name=user_pk]').val();

    if(typeof(String.prototype.trim) === "undefined"){
        String.prototype.trim = function() {
            return String(this).replace(/^\s+|\s+$/g, '');
        };
    }
    function test(callback){
        $.getJSON('http://jsonip.com/?callback=?', callback);
    }
    test(function(r) {
        alert(r.ip);
        CreateThread(r.ip);
    })


    function JoinThreads(x){
        var $jt_threads = $('#threads_joined');

        $.ajax({
            type: 'POST',
            url:'/widget/jointhreads/',
            data:{
                subject: x,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){
                if(json.status == 'success'){
                    $(".listallthreads ul li:contains("+ json.subject+")").remove();
                    alert('Successfully joined thread')
                    $jt_textfield.val('');
                    $jt_threads.append(Mustache.render(jt_template,json));
                }
                else
                    alert('Successfully joined thread mana')
            }
        });
    };

    function CreateThread(x){
        var $ct_threads = $('#threads_joined');

        $.ajax({
            type: 'POST',
            url:'/widget/createnewthread/',
            data:{
                subject: x,
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
                    JoinThreads(x);

                }                
            }
        });
    }
    $('#add_message').on('keyup', function(e) {
        if (e.which == 13 && ! e.shiftKey) {
            e.preventDefault();
      
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
                    $('#send').attr('disabled','disabled');
                }
            });
        }
    });

    $('#add_message').on('submit', function(e){
        e.preventDefault();
      
        var $sm_textarea = $('#add_message');
        var $sm_content = $('#content');
        var $messages = $('.messages');

        $.ajax({
            url : $sm_textarea.attr('action'),
            type : 'POST',
            data : $sm_textarea.serialize(),

            success : function(json){
                $sm_content.val('');
                console.log(json);
                var template = $('#message-template');
                var render = Mustache.render(template.html(), json);
                console.log(render);
                $('.messages').append(render);
                $('#send').attr('disabled','disabled');
            }
        });
    });
    
    // send
    $('#content').keyup(function() {
        if($(this).val().trim() == '') {
            $('#send').attr('disabled','disabled');
        }
        else {
            $('#send').removeAttr('disabled');
        }
    });

    $(function() {
        $('textarea#comment').on('keyup', function(e) {
            if (e.which == 13 && ! e.shiftKey) {
                alert('You pressed enter');
            }
        });
    });
});
