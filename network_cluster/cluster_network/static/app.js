$(document).ready(function() {
  // Initialize variables
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var $messageInput = $('#message-input');
  var $messageBox = $('#message-box');
  var $userList = $('#user-list');
  // read the project path from the system
  path = window.location.host;
  // read the project name from the system
  console.log(path);




  var username = window.location.host;
  var messageHistory = [];
  
  // Emit join event when socket connects
  socket.on('connect', function() {
    socket.emit('join', {username: username});
  });
  // Emit response message event when socket gets a response message for a command.
  socket.on('response_message', function(data) {
    addMessage(data.name, data.message);
  });
  // Emit leave event when socket disconnects
  socket.on('disconnect', function() {
    socket.emit('leave');
  });
  
  function addMessageToHistory(data) {
    messageHistory.push(data);
    var message = $('<div>').addClass('message');
    var name = $('<span>').addClass('name').text(data.name);
    var content = $('<span>').addClass('content').text(data.message);
    // TODO: fix TypeError: undefined is not an object (evaluating 'data.name.toLowerCase')




    if (data.name.toLowerCase().includes('executed response')) {
      content.addClass('sys-admin');
    }
    message.append(name);
    message.append(content);
    $messageBox.append(message);
    $messageBox.scrollTop($messageBox.prop('scrollHeight'));
  }
  
  
  // Send message and add it to message history
  function sendMessage() {
    var message = $messageInput.val();
    if (message) {
      $messageInput.val('');
      socket.emit('send_message', {message: message});
    }
  }
  
  // Emit send_message event when message form is submitted
  $('#message-form').submit(function(event) {
    event.preventDefault();
    sendMessage();
  });
  
  // Emit send_message event when enter key is pressed in message input field
  $messageInput.keydown(function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendMessage();
    }
  });
  
  // Add user to user list
  function addUserToList(data) {
    var user = $('<div>').addClass('user').text(data.name);
    $userList.append(user);
  }
  
  // Remove user from user list
  function removeUserFromList(data) {
    $userList.children().each(function() {
      if ($(this).text() == data.name) {
        $(this).remove();
      }
    });
  }
  
  // Display message history
  function displayMessageHistory() {
    $messageBox.empty();
    messageHistory.forEach(function(data) {
      addMessageToHistory(data);
    });
  }
  
  // Get message history from server and display it
  socket.on('message_history', function(data) {
    messageHistory = data;
    displayMessageHistory();
  });
  
  // Add received message to message history and display it
  socket.on('chat_message', function(data) {
    addMessageToHistory(data);
  });
  
  // Add user to user list
  socket.on('add_user', function(data) {
    addUserToList(data);
  });
  
  // Remove user from user list
  socket.on('remove_user', function(data) {
    removeUserFromList(data);
  });

  function updateTime() {
    var now = new Date();
    var timeElem = document.getElementById("time");
    timeElem.textContent = now.toLocaleString();
  }

  setInterval(updateTime, 1000);

});
