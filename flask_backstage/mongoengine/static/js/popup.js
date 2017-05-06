function popWindow(show_btn, close_btn, shade, pop){
    /**
     *
     *  show_btn: 弹窗触发按钮
     *  close_btn: 弹窗关闭按钮
     *  shade: 遮罩层
     *  pop：弹出窗口窗体
     *
     */
     //窗口水平居中
    $(window).resize(function(){
        popup_center();
    });

    function popup_center(){
        var _top = ($(window).height() - pop.height()) / 2;
        var _left = ($(window).width() - pop.width()) / 2;

        pop.css({
            top: _top,
            left: _left
        });
    }
    //窗口效果
    //点击弹出窗口显示按钮
    show_btn.click(function(){
        shade.fadeIn(); //遮罩层显示
        pop.fadeIn(); //弹出窗口实体显示
        popup_center();
    });

    //点击关闭按钮
    close_btn.click(function(){
        shade.fadeOut(); //遮罩层隐藏
        pop.fadeOut(); //弹出窗口隐藏
    });



}
