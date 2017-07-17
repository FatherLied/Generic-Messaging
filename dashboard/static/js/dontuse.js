define([
    'jquery'
],function($){
    var latestId = $('.messages .message:last-child').data('id')
    console.log(latestId);
    var len = 0;
        function fetch() {
            var x = 5000;

            function _fetch(){
                $.ajax({
                    url: '/messenger/retrieve/',
                    type: 'GET',
                    data: {
                        latestId: latestId,
                    },
                    success : function(data){
                        len = data.objects.messages.length;
                        console.log(data.objects.messages);
                        console.log(data.objects.messages.length);
                        if(len === 0){
                            console.log("no message");
                        }
                        else{
                            for(var x=0; x < len; x++){
                                var date = String(new Date(data.objects.messages[x].when));
                                $('.messages').append('<div class="message"><div class="user">'+data.objects.messages[x].sender+'</div><div class="content"><div class="body">'+data.objects.messages[x].content+'</div><div class="footer">'+date+'</div></div></div>')
                            }
                            latestId += 1;
                        }
                    }
                });
                if(len === 0){
                    x += 1000;
                    console.log(x);
                }else{
                    x = 5000;
                    console.log(x);
                }
                setTimeout(_fetch, x);
            }
            setTimeout(_fetch, x);
        }   
    return {
        fetch: fetch
    };

});