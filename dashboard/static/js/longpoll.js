require([
    'jquery',
    'mustache.min'
],function($, Mustache){
    var latestId = $('.messages .message:last-child').data('id');
    if(!latestId){
        latestId = 0;
    }
    var threadId = $('[name=thread_id_ref]').val();
    if(!threadId){
        threadId = 0;
    }
    console.log(threadId);
    var userId = $('[name=user_pk]').val();
    var x = 2000;
    var len = 0;
    
    function ajaxCall(callback, errorCallback){
        $.ajax({
            url: '/messenger/retrieve/',
            type: 'GET',
            data: {
                latestId: latestId,
                threadId: threadId,
            },
            success : function(data){
                len = data.objects.messages.length;
                if(len === 0){
                    console.log("no message");
                }
                else{
                    for(var x=0; x < len; x++){
                        if(latestId <= data.objects.messages[x].pk){
                            latestId = data.objects.messages[x].pk;
                        }
                        if($(".message[data-id=" + data.objects.messages[x].pk + "]").length === 0){
                            var template = $('#message-template');
                            if(userId == data.objects.messages[x].sender_pk){
                                data.objects.messages[x].classes = "user-message";
                            }
                            var render = Mustache.render(template.html(), data.objects.messages[x]);
                            $('.messages').append(render);
                        }
                    }
                }
                if (typeof callback === "function"){
                    callback(data);
                }
            },
            error : function(e){
                console.log(e);
                if (typeof errorCallback === "function"){
                    errorCallback(e);
                }
            }
        });
    }

    function longpoll() {
        ajaxCall(function(data) {
            if (data.objects.messages.length === 0){
                x += 100;
                if(x>3000){
                    x = 3000;
                }
            } else{
                x = 2000;
            }
            setTimeout(longpoll, x);
        });
    }

    function fetch() {
        setTimeout(longpoll, x);
    }

    fetch();

});
