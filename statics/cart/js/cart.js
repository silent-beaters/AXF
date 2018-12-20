$(function () {
   $(".ischose").bind("click", function () {
       var cartid = $(this).attr("cartid");
       var data = {
           cartid: cartid
       };
       $.ajax({
           url: "/choiceCart/",
           method: "get",
           data: data,
           success: function (data, status) {
               if (data.error == 0) {
                   $rightSpan = $(document.getElementById("cart"+cartid));
                   infoStr = "";
                   if (data.data){
                       infoStr = "√";
                   }
                   $rightSpan.html(infoStr);
               }
           }
       });
   });


   $("#full").bind("click", function () {
       var flag = $(this).attr("flag");
       var data = {
           flag: flag
       };
       $.ajax({
           url: "/fullRight/",
           data: data,
           method: "get",
           success: function (data, status) {
               console.log(data, status);
               if (data.error == 0) {
                   url = "/cart/?from=cart&flag="+data.data.flag;
                   console.log(url);
                   location.href = "/cart/?from=cart&flag="+data.data.flag;

               }
           }
       })
   });
});