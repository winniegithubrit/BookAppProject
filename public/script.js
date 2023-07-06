document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').addEventListener('submit', function(event) {
      event.preventDefault();
  
      var username = document.getElementById('username').value;
      var password = document.getElementById('password').value;
  
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/login', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          var response = JSON.parse(xhr.responseText);
          var messageElement = document.getElementById('message');
  
          if (xhr.status === 200) {
            messageElement.innerHTML = '<span class="success">' + response.message + '</span>';
            window.location.href = '/dashboard';
          } else {
            messageElement.innerHTML = '<span class="error">' + response.message + '</span>';
          }
        }
      };
  
      var data = JSON.stringify({
        username: username,
        password: password
      });
      xhr.send(data);
    });
  });
  