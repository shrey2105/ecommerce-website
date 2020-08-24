$("#send_otp").click(function (event) {
    var formData = {
        "mobile": $("#send_otp_mobile").val(),
        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
    };
    $.ajax({
        url: '/home/send_otp',
        type: 'post',
        data: formData,
        beforeSend: function () {
            $('#otp-message').html(
                '<img src="https://shopnblogbucket.s3.ap-south-1.amazonaws.com/static/home/img/Loader.gif" width="20" height="20"/>'
            );
        },
        success: function (msg) {

            if (msg.status == "success") {
                setTimeout(function () {
                    $("#otp-message").html(`<span style='font-size: 80%; color: #28a745;'>${msg.message}</span>`);
                }, 2000);
            } else {
                setTimeout(function () {
                    $("#otp-message").html(`<span style='font-size: 80%; color: #dc3545;'>${msg.message}</span>`);
                }, 2000);
            }
        }
    });
    event.preventDefault();
});

$(document).ready(function () {
    $("#basic_profile :input").prop("disabled", true);
    $(".update_profile").click(function () {
        if (this.value == "EDIT") {
            this.value = "CANCEL";
            $(".update_profile_button").show();
            $("#basic_profile :input").prop("disabled", false);
        }
        else {
            this.value = "EDIT";
            $(".update_profile_button").hide();
            $("#basic_profile :input").prop("disabled", true);
        }
    });

    $("#form_verify_mobile :input").prop("disabled", true);
    $(".update_mobile").click(function () {
        if (this.value == "EDIT") {
            this.value = "CANCEL";
            $(".update_mobile_button").show();
            $("#form_verify_mobile :input").prop("disabled", false);
        }
        else {
            this.value = "EDIT";
            $(".update_mobile_button").hide();
            $("#form_verify_mobile :input").prop("disabled", true);
        }
    });

    $("#form_update_password :input").prop("disabled", true);
    $(".update_password").click(function () {
        if (this.value == "EDIT") {
            this.value = "CANCEL";
            $(".update_password_button").show();
            $("#form_update_password :input").prop("disabled", false);
        }
        else {
            this.value = "EDIT";
            $(".update_password_button").hide();
            $("#form_update_password :input").prop("disabled", true);
        }
    });
}); 