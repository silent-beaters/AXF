$(function () {
        var $li = $("#slide ul li");
        var len = $li.length;//获取标签的数量
        var $prev = $(".prev");//点击会轮播上一张
        var $next = $(".next");//点击轮播下一张
        var timer = null;//定义一个时间变量 给一个null(空值)
        var nowli = 0;//准备轮播运动过来的(下一张)
        var prevli = 0;//当前要离开的
        $li.not(":first").css({left:365});//除了第一个li标签中的图片不移动，其他每张图片都往右偏移720px
        //创建小圆点可以通过点击和自动轮播关联此小圆点 引入each()有几个li标签就会创建几个小圆点(span标签)
        $li.each(function (index) { //每一个
            var $sli = $("<span>");
            if (index==0){
                $sli.addClass("active");
            }
            $sli.appendTo(".points")
        });

        $points = $(".points span");    //获取小圆点
        $points.click(function () {     //点击小圆点切换到当前圆点的图片
            nowli = $(this).index(); //拿到将要移动的图片的索引值
            if(nowli==prevli){ return;} //判断如果当前图片就是将要移动过来的图片，则不进行重复的切换，减去bug 直接给一个返回值
            move();//定义一个move函数方法
            $(this).addClass("active").siblings().removeClass("active"); //给小圆点增加一个active(之前设置的样式)以及删除同级中的其余class中的class
        });
        $prev.click(function () {   //点击得到上一张
            nowli--;
            move();
            $points.eq(nowli).addClass("active").siblings().removeClass("active");
        });
        $next.click(function () {   //得到下一张
            nowli++;
            move();
            $points.eq(nowli).addClass("active").siblings().removeClass("active");
        });
        //定义一个函数 自动播放功能
        function autoplay() {
            nowli++;
            move();
            $points.eq(nowli).addClass("active").siblings().removeClass("active");
        }
        timer = setInterval(autoplay,3000);//给一个定时器关联   autoplay()
        $("#slide").mouseenter(function () {    //鼠标悬停图片区域 清除定时器 使得图片停止自动播放
           clearInterval(timer);
        });
        $("#slide").mouseleave(function () {        //鼠标离开图片区域 启动定时器
           timer = setInterval(autoplay,3000);
        });

        function move() {
            if(nowli<0){
                nowli = len-1;
                prevli = 0;
                $li.eq(nowli).css({left:-365});
                $li.eq(prevli).stop().animate({left:365});
                $li.eq(nowli).stop().animate({left:0});
                prevli=nowli;
                return;
            }
            if(nowli>len-1){
                nowli = 0;
                prevli = len-1;
                $li.eq(nowli).css({left:365});
                $li.eq(prevli).stop().animate({left:-365});
                $li.eq(nowli).stop().animate({left:0});
                prevli=nowli;
                return;
            }
            if(nowli>prevli){
                $li.eq(nowli).css({left:365});
                $li.eq(prevli).stop().animate({left:-365});
            }else {
               $li.eq(nowli).css({left:-365});
                $li.eq(prevli).stop().animate({left:365});
            }
            $li.eq(nowli).stop().animate({left:0});
            prevli=nowli;
        }
    });