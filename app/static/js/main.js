$(document).ready(function () {
  
  // 动态调整首页分级分类选项的大小和位置
  var itemwidth = $(".class-div>ul").width();
  $(".class-div li>ul").css("width", itemwidth);
  $(".class-div li>ul").css("left", itemwidth);
  $(window).resize(function(){
    var itemwidth = $(".class-div>ul").width();
    $(".class-div li>ul").css("width", itemwidth);
    $(".class-div li>ul").css("left", itemwidth);
  });

  // 选择文档类型和国家
  $(".tag-selection .tag").click(function(){
    $(this).parent().siblings().children().removeClass("tag-checked");
    $(this).addClass("tag-checked");
  });

  // 全选or全不选
  $("#website_all_check").click(function(){
    if(this.checked){
      $("#collect table input[name='website']").attr("checked", "checked");
    }else{
      $("#collect table input[name='website']").attr("checked", null);
    }
  });

  $("#policy_all_check").click(function(){
    if(this.checked){
      $("#proofread table input[name='policy']").attr("checked", "checked");
    }else{
      $("#proofread table input[name='policy']").attr("checked", null);
    }
  });
});

