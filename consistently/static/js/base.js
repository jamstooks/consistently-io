function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

handleToggleRepoConnect = function() {
  
  let githubId = $(this).data()['githubid'];
  let url = $(this).data()['apiaddurl'];
  let urlDel = $(this).data()['apidelurl'];
  let settingsIcon = $("#settings-" + githubId);
  
  let self = $(this);
  
  var putData = {
    github_id: githubId
  };
  
  if($(this).parent().hasClass("connected")) {
    
    // then we're removing a repo
    self.removeClass("fa-toggle-on");
    self.addClass("fa-spinner fa-spin");
    
    fetch(urlDel, {
      method: "delete",
      credentials: "same-origin",
      headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          "Content-Type": "application/json"
      },
    }).then(function(response) {
        
        self.removeClass("fa-spin fa-spinner");
        self.addClass("fa-toggle-off");
        self.parent().toggleClass("connected");
        settingsIcon.addClass("hidden");
        
    }).catch(function(ex) {
        console.log("parsing failed", ex);
    });
    
  }
  else {
  
    self.removeClass("fa-toggle-off");
    self.addClass("fa-spinner fa-spin");
  
    // add a repo
    fetch(url, {
      method: "post",
      credentials: "same-origin",
      headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          "Content-Type": "application/json"
      },
      body: JSON.stringify(putData)
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
      
        // console.log("Data is ok", data);
        self.removeClass("fa-spin fa-spinner");
        self.addClass("fa-toggle-on");
        self.parent().toggleClass("connected");
        settingsIcon.removeClass("hidden")
        
    }).catch(function(ex) {
        console.log("parsing failed", ex);
    });
  }
}