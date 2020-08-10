$("form#publish-form button[name=submit]").on("click", function () {

        var validation_holder = 0;
        var title_regex = /^.{10,}$/;
        var heading_regex = /^.{20,}$/;
        var content_regex = /^.{160,}$/;
  
        var title = $("form#publish-form input[name=title]").val(); 
        var first_heading = $("form#publish-form input[name=first_heading]").val();
        var first_content = $("form#publish-form textarea[name=first_content]").val();
        var second_heading = $("form#publish-form input[name=second_heading]").val();
        var second_content = $("form#publish-form textarea[name=second_content]").val();
        var sub_heading = $("form#publish-form input[name=sub_heading]").val();
        var sub_content = $("form#publish-form textarea[name=sub_content]").val();
  
        if (title == "") {
          $("span.error_title").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("input[name=title]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!title_regex.test(title)) {
            $("span.error_title").html("<span style='font-size: 80%; color: #dc3545;'>Min: 10 characters required.</span>").addClass('validate');
            $("input[name=title]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
              $("span.error_title").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("input[name=title]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (first_heading == "") {
          $("span.error_first_heading").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("input[name=first_heading]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!heading_regex.test(first_heading)) {
            $("span.error_first_heading").html("<span style='font-size: 80%; color: #dc3545;'>Min: 20 characters required.</span>").addClass('validate');
            $("input[name=first_heading]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_first_heading").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("input[name=first_heading]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (first_content == "") {
          $("span.error_first_content").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("textarea[name=first_content]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!content_regex.test(first_content)) {
            $("span.error_first_content").html("<span style='font-size: 80%; color: #dc3545;'>Min: 160 characters required.</span>").addClass('validate');
            $("textarea[name=first_content]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_first_content").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("textarea[name=first_content]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (second_heading == "") {
          $("span.error_second_heading").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("input[name=second_heading]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!heading_regex.test(second_heading)) {
            $("span.error_second_heading").html("<span style='font-size: 80%; color: #dc3545;'>Min: 20 characters required.</span>").addClass('validate');
            $("input[name=second_heading]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_second_heading").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("input[name=second_heading]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (second_content == "") {
          $("span.error_second_content").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("textarea[name=second_content]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!content_regex.test(second_content)) {
            $("span.error_second_content").html("<span style='font-size: 80%; color: #dc3545;'>Min: 160 characters required.</span>").addClass('validate');
            $("textarea[name=second_content]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_second_content").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("textarea[name=second_content]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (sub_heading == "") {
          $("span.error_sub_heading").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("input[name=sub_heading]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!heading_regex.test(sub_heading)) {
            $("span.error_sub_heading").html("<span style='font-size: 80%; color: #dc3545;'>Min: 20 characters required.</span>").addClass('validate');
            $("input[name=sub_heading]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_sub_heading").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("input[name=sub_heading]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (sub_content == "") {
          $("span.error_sub_content").html("<span style='font-size: 80%; color: #dc3545;'>This is a required field.</span>").addClass('validate');
          $("textarea[name=sub_content]").focus();
          $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
          validation_holder = 1;
        } else {
          if (!content_regex.test(sub_content)) {
            $("span.error_sub_content").html("<span style='font-size: 80%; color: #dc3545;'>Min: 160 characters required.</span>").addClass('validate');
            $("textarea[name=sub_content]").focus();
            $(":focus").css({ "border-color": "red", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(220, 53, 69)" });
            validation_holder = 1;
          } else {
            $("span.error_sub_content").html("<span style='font-size: 80%; color: #28a745;'>Done.</span>");
            $("textarea[name=sub_content]").focus();
            $(":focus").css({ "border-color": "green", "outline": 0, "box-shadow": "inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgb(40, 167, 69)" });
          }
        }
  
        if (validation_holder == 1) {
          return false;
        } validation_holder = 0;
  
      });


      $('textarea[name=first_content]').keypress(function(){
        if(this.value.length > 160){
            return true;
        }
        $("#remaining_first_content").html("<span style='font-size: 80%; color: #dc3545;'>Min characters: " + (160 - this.value.length) + "</span>");
    });
    
        $('textarea[name=second_content]').keypress(function(){
        if(this.value.length > 160){
            return true;
        }
        $("#remaining_second_content").html("<span style='font-size: 80%; color: #dc3545;'>Min characters: " + (160 - this.value.length) + "</span>");
    });
    
        $('textarea[name=sub_content]').keypress(function(){
        if(this.value.length > 160){
            return true;
        }
        $("#remaining_sub_content").html("<span style='font-size: 80%; color: #dc3545;'>Min characters: " + (160 - this.value.length) + "</span>");
    });