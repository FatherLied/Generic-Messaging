define([
    'jquery'
],function($){
    function fetch() {
        setInterval(_fetch, 5000);
        function _fetch(){
            var latestId = $('.messages .message:last-child').data('id')
            console.log(latestId);

            $.ajax({
                url: '/messenger/retrieve/',
                type: 'GET',
                data: {
                    latestId: latestId,
                },
                success : function(data){
                    // alert("hey")
                    console.log(data.objects);
                }
            
            });
        }
    }
    return {
        fetch: fetch
    };
});