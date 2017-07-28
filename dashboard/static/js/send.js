require([
    'jquery',
    'mustache.min'
],function($,Mustache){
    $('#send').attr('disabled','disabled');
    var userId = $('[name=user_pk]').val();
    var threadId;
    var userIp;

    $(document).ready(function(){
        setTimeout(scrollBottom, 700);
    });

    if(typeof(String.prototype.trim) === "undefined"){
        String.prototype.trim = function() {
            return String(this).replace(/^\s+|\s+$/g, '');
        };
    }
    function test(callback){
        $.getJSON('http://jsonip.com/?callback=?', callback);
    }
    test(function(r) {
        userIp = r.ip;
        CreateThread(r.ip);
    })

    function scrollBottom(){
        var scroll = $('.messages')[0].scrollHeight - $('.messages').height();
        $('.messages').scrollTop(scroll);
    }

    function CreateThread(x){
        var $ct_threads = $('#threads_joined');

        $.ajax({
            type: 'POST',
            url:'/widget/createnewthread/',
            data:{
                subject: x,
                ip: x,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){
                len = json.objects.messages.length;
                if(len == 0){
                    console.log("no messages");
                }
                else{
                    for(var x=0; x < len; x++){
                        var template = $('#message-template');
                        var render = Mustache.render(template.html(), json.objects.messages[x]);
                        $('.messages').append(render);
                    }
                }
                threadId = json.thread_id;
                console.log(threadId);
                $('[name=thread_id]').attr('value', threadId);
                var $userIp = $('<input type="hidden" name="ip" value='+ userIp +'>');
                $('#add_message').append($userIp);

            }
        });
    }
    $('#add_message').on('keyup', function(e) {
        if (e.which == 13 && ! e.shiftKey) {
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
                    console.log(userId);
                    console.log(json);
                    var template = $('#message-template');
                    if(userId == json.sender_pk){
                        json.classes = "user-message";
                    }
                    var render = Mustache.render(template.html(), json);
                    console.log(render);
                    $('.messages').append(render);
                    scrollBottom();
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
        // console.log($sm_textarea.serialize());

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
                scrollBottom();
                $('#send').attr('disabled','disabled');
                if(json.threadId != threadId){
                    threadId = json.threadId;
                    $('[name=thread_id]').attr('value', threadId);
                }
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
