require([
    'jquery',
    'mustache.min'
],function($,Mustache){
	$('#send').attr('disabled','disabled');
    $('#create').attr('disabled','disabled');
    $('#join').attr('disabled','disabled');
    var userId = $('[name=user_pk]').val();

    if(typeof(String.prototype.trim) === "undefined"){
	    String.prototype.trim = function() {
	        return String(this).replace(/^\s+|\s+$/g, '');
	    };
	}

    $('#jointhreads').on('submit',function(e){
        e.preventDefault()

        var jt_template = "<a class='list-group-item' href='{{thread_url}}' >{{subject}}</a> ";
        var $jt_threads = $('#threads_joined');
        var $jt_textfield = $('#join_subject');

        $.ajax({
            type:'POST',
            url:$('#jointhreads').attr('action'),
            data:{
                subject: $jt_textfield.val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(json){

                if(json.status == 'success'){
                    $(".listallthreads ul li:contains("+ json.subject+")").remove();
                    alert('Successfully joined thread')
                    $jt_textfield.val('');
                    $jt_threads.append(Mustache.render(jt_template,json));
                    $('#join').attr('disabled','disabled');
                    window.location.href = json.thread_url;
                }
                else if(json.status == 'error1')
                    alert(json.context)
                
                else
                    alert(json.context)
            }
        })
    });

    $('#createthreads').on('submit',function(e){
        e.preventDefault()
        
        var ct_template = "<a class='list-group-item' href='{{thread_url}}' >{{subject}}</a> ";
        var $ct_threads = $('#threads_joined');
        var $ct_textfield = $('#create_subject');

        $.ajax({
            type:'POST',
            url:$('#createthreads').attr('action'),
            data:{
                subject: $ct_textfield.val(),
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
                    $('#create').attr('disabled','disabled');
                    window.location.href = json.thread_url;
                    
                }                
            }
        })
    });

    $('#send_message').on('submit', function(e){
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
    // create
    $('#create_subject').keyup(function() {
        if($(this).val() == '' || (/^ *$/.test($(this).val()))  ) {
        	$('#create').attr('disabled','disabled');
        }
        else {
        	$('#create').removeAttr('disabled');
        }
    });
    // join
    $('#join_subject').keyup(function() {
        if($(this).val() == '' || (/^ *$/.test($(this).val()))  ) {
            $('#join').attr('disabled','disabled');
        }
        else {
        	$('#join').removeAttr('disabled');
        }
    });

});
