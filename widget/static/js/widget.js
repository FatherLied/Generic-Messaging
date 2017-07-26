require([
    'jquery',
    'mustache.min'
],function($,Mustache){
    $('#details').hide();
    $('#item').on('click', function(){
        $('#details').show();
    });
});

$('#send_message').on('keyup', function(e) {
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