var auth2 = {};
function adduser(email, name) {
    $.ajax({
        url : "/eventhublogin/auth/webapp/", // the endpoint
        type : "POST", // http method
        data : {'name': name,'email':email}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            // console.log(json);
            if(json.success ==1)
            { 
              console.log("Success");
              window.location=window.location+"/events";

            }       
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
        }
});
}

function logoutuser(token) {
    $.ajax({
        url : "/eventhublogin/logoutuser/", // the endpoint
        type : "POST", // http method
        data : {'token': token}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            // console.log(json);
            if(json.success ==1)
            { 
              console.log("Success");
              location.reload();

            }       
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
        }
});
}
var helper = (function() {
  return {
    /**
     * Hides the sign in button and starts the post-authorization operations.
     *
     * @param {Object} authResult An Object which contains the access token and
     *   other authentication information.
     */
    onSignInCallback: function(authResult) {
      $('#authResult').html('Auth Result:<br/>');
      for (var field in authResult) {
        $('#authResult').append(' ' + field + ': ' +
            authResult[field] + '<br/>');
      }
      if (authResult.isSignedIn.get()) {
        $('#authOps').show('slow');
        helper.profile();
      } else {
          if (authResult['error'] || authResult.currentUser.get().getAuthResponse() == null) {
            // There was an error, which means the user is not signed in.
            // As an example, you can handle by writing to the console:
            console.log('There was an error: ' + authResult['error']);
          }
          $('#authResult').append('Logged out');
          $('#authOps').hide('slow');
          $('#gConnect').show();
      }

      console.log('authResult', authResult);
    },

    /**
     * Calls the OAuth2 endpoint to disconnect the app for the user.
     */
    disconnect: function() {
      // Revoke the access token.
      auth2.disconnect();
    },

    /**
     * Gets and renders the currently signed in user's profile data.
     */
    profile: function(){
      gapi.client.plus.people.get({
        'userId': 'me'
      }).then(function(res) {
        console.log(res);
        console.log(res.result.displayName);
        console.log(res.result.emails[0]['value']);
        adduser(res.result.emails[0]['value'],res.result.displayName);
      }, function(err) {
        var error = err.result;
        $('#profile').empty();
        $('#profile').append(error.message);
      });
    },
  };
})();

/**
 * jQuery initialization
 */
$(document).ready(function() {
  $('#disconnect').click(helper.disconnect);
  $('#loaderror').hide();
  if ($('meta')[0].content == 'YOUR_CLIENT_ID') {
    alert('This sample requires your OAuth credentials (client ID) ' +
        'from the Google APIs console:\n' +
        '    https://code.google.com/apis/console/#:access\n\n' +
        'Find and replace YOUR_CLIENT_ID with your client ID.'
    );
  }

  $('#signOut').click(function(){
        auth2.signOut();
        logoutuser("Logout");
  });
});

/**
 * Handler for when the sign-in state changes.
 *
 * @param {boolean} isSignedIn The new signed in state.
 */
var updateSignIn = function() {
  console.log('update sign in state');
  if (auth2.isSignedIn.get()) {
    console.log('signed in');
    helper.onSignInCallback(gapi.auth2.getAuthInstance());
  }else{
    console.log('signed out');
    helper.onSignInCallback(gapi.auth2.getAuthInstance());
  }
}

/**
 * This method sets up the sign-in listener after the client library loads.
 */
function startApp() {
  gapi.load('auth2', function() {
    gapi.client.load('plus','v1').then(function() {
      gapi.signin2.render('signin-button', {
          scope: 'https://www.googleapis.com/auth/plus.login',
          fetch_basic_profile: false });
      gapi.auth2.init({fetch_basic_profile: false,
          scope:'https://www.googleapis.com/auth/plus.login'}).then(
            function (){
              console.log('init');
              auth2 = gapi.auth2.getAuthInstance();
              auth2.isSignedIn.listen(updateSignIn);
              // auth2.then(updateSignIn);
            });
    });
  });
}