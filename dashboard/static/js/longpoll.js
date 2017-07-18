define([
    'jquery'
],function($){
    var latestId = $('.messages .message:last-child').data('id');
    if(!latestId){
        latestId = 0;
    }
    var threadId = $('[name=thread_id_ref]').val();
    var x = 3000;
    var len = 0;
    var timer;

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
                console.log(data.objects.messages);
                if(len === 0){
                    console.log("no message");


                }
                else{
                    for(var x=0; x < len; x++){
                        if(latestId <= data.objects.messages[x].pk){
                            latestId = data.objects.messages[x].pk;
                        }
                        var date = String(new Date(data.objects.messages[x].when));
                        if($(".message[data-id=" + data.objects.messages[x].pk + "]").length === 0){
                            $('.messages').append('<div class="message" data-id="' + data.objects.messages[x].pk + '"><div class="user">'+data.objects.messages[x].sender+'</div><div class="content"><div class="body">'+data.objects.messages[x].content+'</div><div class="footer">'+date+'</div></div></div>')   
                        }
                    }
                    console.log(latestId);
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
            console.log(x);
            if (data.objects.messages.length === 0){
                x += 1000;
                if(x>5000){
                    x = 5000;
                }
            } else{
                x = 3000;
            }
            console.log(x);
            timer = setTimeout(longpoll, x);
        });
    }

    function fetch() {
        timer = setTimeout(longpoll, x);
    }

    function restartTimer(){
        clearTimeout(timer);
        fetch();
    }

    return {
        fetch: fetch,
        restart: restartTimer
    };

});
