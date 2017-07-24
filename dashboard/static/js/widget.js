require([
    'jquery',
    'mustache.min'
],function($,Mustache){
    $('#details').hide();
    $('#item').on('click', function(){
        $('#details').show();
    });
});