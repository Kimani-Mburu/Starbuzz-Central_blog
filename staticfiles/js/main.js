// main.js

// Function to truncate text to a specified number of words
function truncateText(text, wordCount) {
    var words = text.split(' ');
    if (words.length > wordCount) {
      var truncatedText = words.slice(0, wordCount).join(' ') + '...';
      return truncatedText;
    }
    return text;
  }
  
  // Function to display a confirmation message before deleting a post
  function confirmDelete() {
    return confirm('Are you sure you want to delete this post?');
  }
  
  // Function to handle AJAX request for submitting a comment
  function submitComment(postId) {
    var commentContent = document.getElementById('comment-content-' + postId).value;
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/comment/submit/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // Comment submitted successfully, handle the response if needed
        console.log(xhr.responseText);
      }
    };
    var data = 'post_id=' + postId + '&comment_content=' + encodeURIComponent(commentContent);
    xhr.send(data);
  }
  