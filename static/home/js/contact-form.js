function contact_form_home_validation() {

  $("form#form-contact button[name='submit']").click(function () {

    var validation_holder = 0;
    var full_name = $("form#form-contact input[name='name']").val();
    var name_regex = /^[A-Za-z. ]{5,20}$/;
    var email = $("form#form-contact input[name='email']").val();
    var email_regex = /^[\w%_\-.\d]+@[\w.\-]+.[A-Za-z]{2,6}$/;
    var mobile = $("form#form-contact input[name='mobile']").val();
    var mobile_regex = /^[0-9]{10}$/;
    var message = $("form#form-contact textarea[name='message']").val();
    var message_regex = /^[ A-Za-z0-9_@.\#&+-]{20,}$/;

    if (full_name == "") {
      $("span.error_name").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
      $("input[name=name]").focus();
      $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
      validation_holder = 1;
    } else {
      if (!name_regex.test(full_name)) {
        $("span.error_name").html("<span style='font-size: 80%; color: #dc3545;'>Please enter a valid name.</span>").addClass('validate');
        $("input[name=name]").focus();
        $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
        validation_holder = 1;
      } else {
        $("span.error_name").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
        $("input[name=name]").focus();
        $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
      }
    }

    if (email == "") {
      $("span.error_email").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
      $("input[name=email]").focus();
      $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
      validation_holder = 1;
    } else {
      if (!email_regex.test(email)) {
        $("span.error_email").html("<span style='font-size: 80%; color: #dc3545;'>Please enter a valid email address.</span>").addClass('validate');
        $("input[name=email]").focus();
        $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
        validation_holder = 1;
      } else {
        $("span.error_email").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
        $("input[name=email]").focus();
        $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
      }
    }

    if (mobile == "") {
      $("span.error_mobile").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
      $("input[name=mobile]").focus();
      $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
      validation_holder = 1;
    } else {
      if (!mobile_regex.test(mobile)) {
        $("span.error_mobile").html("<span style='font-size: 80%; color: #dc3545;'>Please enter a valid mobile number.</span>").addClass('validate');
        $("input[name=mobile]").focus();
        $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
        validation_holder = 1;
      } else {
        $("span.error_mobile").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
        $("input[name=mobile]").focus();
        $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
      }
    }

    if (message == "") {
      $("span.error_message").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
      $("textarea[name=message]").focus();
      $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
      validation_holder = 1;
    } else {
      if (!message_regex.test(message)) {
        $("span.error_message").html("<span style='font-size: 80%; color: #dc3545;'>Please enter a valid message greater than 20 characters.</span>").addClass('validate');
        $("textarea[name=message]").focus();
        $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
        validation_holder = 1;
      } else {
        $("span.error_message").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
        $("textarea[name=message]").focus();
        $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
      }
    }

    if (validation_holder == 1) {
      return false;
    } validation_holder = 0;



    // $("#submit-button").click(function () {
    var str = $("#form-contact").serialize();

    $.ajax({
      url: "/home/contact",
      data: str,
      type: 'post',
      beforeSend: function () {
        $('#contact-message').html(
          '<img src="/static/home/img/Loader.gif" width="25" height="25"/>'
        );
      },
      success: function (response) {
        console.log(response)
        response = JSON.parse(response);
        if (response['status'] == "success") {
          setTimeout(function () {
            $("#contact-message").html("<span style='font-size: 100%; color: #28a745;'>Your response has been successfully recorded.</span>");
          }, 2000);
          $("#name").val("");
          $("#email").val("");
          $("#mobile").val("");
          $("#message").val("");
        }
        else {
          setTimeout(function () {
            $("#contact-message").html("<span style='font-size: 100%; color: #dc3545;'>Something went wrong. Kindly fill correct details.</span>");
          }, 2000);
        }
      }

    });
    event.preventDefault();
  });
}