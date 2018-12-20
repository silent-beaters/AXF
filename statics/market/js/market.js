$(function () {

    isStr = "yellow" + location.href.split("/")[4];
    var $span = $(document.getElementById(isStr));
    $span.addClass("yellow");


    //点击全部分类、综合排序

    $("#typeBtn").bind("click", function () {
        $("#typeDiv").toggle();
        $("#sortDiv").hide();
    });
    $("#sortBtn").bind("click", function () {
        $("#sortDiv").toggle();
        $("#typeDiv").hide();
    });
    function func() {
        $(this).hide()
    }
    $("#typeDiv").bind("click", func);
    $("#sortDiv").bind("click", func);


    //给类型加背景颜色
    var typeSpanStr = "type" + location.href.split("/")[5];
    var $typeSpan = $(document.getElementById(typeSpanStr));
    $typeSpan.addClass("typeBg");

    //给排序加背景颜色
    var sortSpanStr = "sort" + location.href.split("/")[6];
    var $sortSpan = $(document.getElementById(sortSpanStr));
    $sortSpan.addClass("typeBg");

    urlStr = location.href;
    gid = urlStr.split("/")[4];
    cid = urlStr.split("/")[5];
    sid = urlStr.split("/")[6];
    function add_sub() {
        num = $(this).attr("num");
        pid = $(this).attr("pid");
        var data = {
            num: num,
            pid: pid
        };
        $.ajax({
            url: "/addSubCart/",
            method: "get",
            data: data,
            success: function (data, status) {
                if (data.error == 0){
                    pStr = "product" + data.data.pid;
                    var $span = $(document.getElementById(pStr));
                    $span.html(data.data.num);
                } else if (data.error == -1){
                    location.href = "/login/?from=market/"+gid+"/"+cid+"/"+sid
                }
            }
        })
    }
    // 添加购物车
    $(".addBtn").bind("click", add_sub);
    //减少购物车
    $(".subBtn").bind("click", add_sub);
});