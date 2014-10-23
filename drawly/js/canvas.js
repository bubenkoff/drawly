$(function(){
    var drawingboard = new DrawingBoard.Board('canvas');
    var log = $('#log');
    var users = $('#users');
    var username = $('#username');
    var canvas = $('#canvas canvas, #canvas');
    var sock = io.connect('ws://' + window.location.host);

    $('#join').click(function() {
        sock.emit('join', {
            'username': username.val()});
        $(this).hide();
        $('#leave').show();
    });

    $('#leave').click(function() {
        sock.emit('leave', {
            'username': username.val()});
        $(this).hide();
        $('#join').show();
    });

    var log_message =  function (message) {
        log.append($('<div/>').append(message));
    };

    sock.on('users', function (message) {
        users.html('');
        users.html($.map(message.users, function(user) {return $('<div/>').append(user);}));
    });

    sock.on('message', function (message) {
        log_message(message.message);
    });

    sock.on('connect', function() {
        log.append('connected');
        sock.emit('message',
            {'message': 'connected'});
    });

    sock.on('broadcast_event', function(message) {
        var e = jQuery.Event(message.type, message);
        if (message.username != $('#username').val()) {
            canvas.trigger(e);
        }
    });

    canvas.on('mousedown mouseup mousemove click', function(evt) {
        if (!evt.username) {
            sock.emit('event', {
                type: evt.type,
                username: username.val(),
                timeStamp: evt.timeStamp,
                pageX: evt.pageX,
                pageY: evt.pageY});
        }
    });
});
