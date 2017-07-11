$('#send_message').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : $('#send_message').attr('action'),
        type : 'POST',
        data : $('#send_message').serialize(),

        success : function(json){
            $('#messages').append(json.data);
            alert("message sent!")
            window.location.reload(true);
        }
    });
});