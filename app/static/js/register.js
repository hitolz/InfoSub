/**
 * Created by hypo on 2017/6/23.
 */

$("#captcha").click(function () {
    $(this).html("");
    $.ajax({
        url: '/captcha',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $("#captcha").html('<img src="/captcha/' + data.captcha_id +
                '" width="100%" class="img-rounded">');
            $("input[name='captcha_id']").val(data.captcha_id)
        },
        error: function () {
            alert("ERROR")
        }
    });
});
$("#username").bind('input propertychange', function () {
    var in_name = $(this);
    var class_val = "form-group ";
    var username = in_name.val();
    $.ajax({
        url: '/verification/username',
        type: 'POST',
        data: {username: username},
        dataType: 'json',
        success: function () {
            in_name.parent().attr("class", class_val + "has-success");
        },
        error: function () {
            in_name.parent().attr("class", class_val + "has-error");
        }
    });
});
$("#email").bind('input propertychange', function () {
    var in_email = $(this);
    var class_val = "form-group ";
    var email = in_email.val();
    $.ajax({
        url: '/verification/email',
        type: 'POST',
        data: {email: email},
        dataType: 'json',
        success: function () {
            in_email.parent().attr("class", class_val + "has-success");
        },
        error: function () {
            in_email.parent().attr("class", class_val + "has-error");
        }
    });

});
$("#captcha_code").bind('input propertychange', function () {
    var in_cp = $(this);
    var class_val = "col-md-8 ";
    var cp_code = in_cp.val();
    var cp_id = $("#captcha_id").val();
    $.ajax({
        url: '/verification/captcha',
        type: 'POST',
        data: {captcha_code: cp_code, captcha_id: cp_id},
        dataType: 'json',
        success: function () {
            in_cp.parent().attr("class", class_val + "has-success");
        },
        error: function () {
            in_cp.parent().attr("class", class_val + "has-error");
        }
    });
});