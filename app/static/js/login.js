/**
 * Created by hypo on 2017/7/11.
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
