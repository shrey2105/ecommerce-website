function checkUsername(){
$("#username").blur(function () {
    $.ajax({
        url: '/blog/signupcheck',
        type: 'post',
        data: {
          "username": username,
          "csrfmiddlewaretoken": $("form#signup-form input[name=csrfmiddlewaretoken]").val()
        },
        success: function (msg) {
          if ((msg != "OK")) {
            $("span.error_username").html("<span style='font-size: 80%; color: #dc3545;'>Username unavailable.</span>").addClass('validate');
            $("input[name=username]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            $("#username").val("");
          }
          else {
            $("span.error_username").html("<span style='font-size: 80%; color: #28a745;'>Username available.</span>");
            $("input[name=username]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
        
      });
});
}