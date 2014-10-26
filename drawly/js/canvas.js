$(function(){
    var drawingboard = new DrawingBoard.Board('canvas');
    var log = $('#log');
    var users = $('#users');
    var username = $('#username');
    var canvas = $('#canvas canvas, #canvas');
    var sock = io.connect();

    $('#join').click(function() {
        // join the room
        sock.emit('join', {
            'username': username.val()});
        $(this).hide();
        $('#leave').show();
    });

    $('#leave').click(function() {
        // leave the room
        sock.emit('leave', {
            'username': username.val()});
        $(this).hide();
        $('#join').show();
    });

    var log_message =  function (message) {
        // add message to the message log box
        log.append($('<div/>').append(message));
    };

    sock.on('users', function (message) {
        // active users list received from the server
        users.html('');
        users.html($.map(message.users, function(user) {return $('<div/>').append(user);}));
    });

    sock.on('message', function (message) {
        // informational message received from the server
        log_message(message.message);
    });

    sock.on('connect', function() {
        // socket is connected
        log.append('connected');
        sock.emit('message',
            {'message': 'connected'});
    });

    sock.on('broadcast_event', function(message) {
        // replay broadcasted events only if they are not from current user
        var e = jQuery.Event(message.type, message);
        if (message.username != $('#username').val()) {
            canvas.trigger(e);
        }
    });

    canvas.on('mousedown mouseup mousemove click', function(evt) {
        // send the captured event to the server only if it's initiated by current user
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
