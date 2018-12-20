$(function () {
    document.documentElement.style.fontSize = innerWidth / 10 + "px";

    //    http://127.0.0.1:8000/cart/
    urlStr = location.href;
    var idStr = urlStr.split("/")[3];
    var $span = $(document.getElementById(idStr));
    $span.css("background", "url(/static/common/img/"+idStr+"1.png)");
    $span.css("background-size", "0.9rem");
});