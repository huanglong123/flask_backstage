$(function(){
	//topbar 左侧
	$('.topbar-product-btn').click(function(){
		$(this).find('span.icon-arrow-down').toggleClass('rotate-180');
		$(this).next('.topbar-product-dropdown').toggleClass('topbar-show');
		$(this).toggleClass('active');
	})
	$('.topbar-product-close').click(function(){
		$('.topbar-product-dropdown').removeClass('topbar-show');
	})

	//topbar 右侧
	$('.topbar-info-dropdown').hover(function(){
		$(this).find('.topbar-info-dropdown-menu').css('display', 'block');
	},function(){
		$(this).find('.topbar-info-dropdown-menu').css('display', 'none');
	})

	// 左侧树形导航条上下展开收缩控制
	$('.sidebar-inner .sidebar-nav').first().find('.sidebar-title').addClass('active');
	$('.sidebar-inner .sidebar-nav').first().find('ul').slideDown();
	//if($('.sidebar-title').parent().next('ul.sidebar-trans')){
		$('.sidebar-title').click(function(){
			if(!($(this).hasClass('active'))){
				$('ul.sidebar-trans').stop(true, true).slideUp();
				$(this).parent().next('ul').stop(true, true).slideToggle();
				$('.sidebar-title').removeClass('active');
				if($(this).parent().next().is('ul.sidebar-trans')){
					$(this).addClass('active');
				}

			}else{
				$('.sidebar-title').removeClass('active');
				$(this).parent().next('ul').stop(true, true).slideToggle();
			}
		})
	//}


	//左侧导航条左右展开收缩控制
	$('.sidebar-fold').click(function(){
		if($('.viewFramework-body').hasClass('viewFramework-sidebar-full')){
			console.log(3333)
			$('.viewFramework-body').removeClass('viewFramework-sidebar-full').addClass('viewFramework-sidebar-mini');
		}else{
			$('.viewFramework-body').removeClass('viewFramework-sidebar-mini').addClass('viewFramework-sidebar-full');
		}
	})

	//三级菜单存在的情况
	if($('.viewFramework-product').length){
		$('.viewFramework-body').addClass('content-wrapper-f viewFramework-product-col-1');
		$('.product-navbar-collapse-inner').click(function(){
			if($('.viewFramework-product').hasClass('viewFramework-product-col-1')){
				$('.viewFramework-product').removeClass('viewFramework-product-col-1');
				$('.viewFramework-body').removeClass('viewFramework-product-col-1');

			}else{
				$('.viewFramework-product').addClass('viewFramework-product-col-1');
				$('.viewFramework-body').addClass('viewFramework-product-col-1');
			}
		})
	}


	//菜单栏选中高亮显示封装函数
	function element_highlight(element, cls){
		element.click(function() {
			element.removeClass(cls);
			$(this).addClass(cls);
		});
	}

	// 左侧导航条二级菜单选中高亮显示
	element_highlight($('ul.sidebar-trans .nav-item'), 'current');


	// 三级菜单栏选中TAB切换
	$('.product-nav-list ul li').click(function(){
		var index=$(this).index();
		$(this).addClass("active").siblings().removeClass("active");
		$(".viewFramework-product-body .user-account-wrapper").addClass("content-on").eq(index).siblings(".viewFramework-product-body .user-account-wrapper").removeClass("content-on");
	})

	// 个人设置弹出窗口触发  调用(popup.js)方法: popWindow(弹窗触发按钮，弹窗关闭按钮，遮罩层，弹窗实体) ==>遮罩层和弹窗实体相对于body定位
	// popWindow($('.binding-phone'), $('.close-btn'), $('.pop-shade'), $('.binding-phone-pop'));  //绑定手机
	// popWindow($('.change-email'), $('.close-btn'), $('.pop-shade'), $('.change-email-pop'));    //修改邮箱
	// popWindow($('.change-password'), $('.close-btn'), $('.pop-shade'), $('.change-password-pop'));  //修改密码

})