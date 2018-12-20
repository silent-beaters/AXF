$(function () {
    $("#smsBtn").bind("click", function () {
        var data = {
            "phone": $("#phone").val()
        };
        $.ajax({
            url: "/verifycode/",
            data: data,
            method: "get",
            success: function (data, status) {
                console.log(data.data)
            }
        });
    });
});