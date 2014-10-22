$(function(){
    var drawingboard = new DrawingBoard.Board('canvas');
    var sock = new WebSocket('ws://localhost:8000/echo');
})
