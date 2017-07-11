$('#send_message').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : $('#send_message').attr('action'),
        type : 'POST',
        data : $('#send_message').serialize(),

        success : function(json){
            date = String(new Date(json.when));
            $('.messages').append('<div class="message"><div class="user">'+json.sender+'</div><div class="content"><div class="body">'+json.content+'</div><div class="footer">'+date+'</div></div></div>')
            $('#messages').append(json.data);
            console.log(json);
            alert("message sent!")
        }
    });
});