function KeywordNum(){
      var shownum = $("#keywordshownum").val();
      $.ajax({
        url: "/ana_keyword",
        type: "POST",
        data: {"num":shownum},
        dataType: "json",
        success: function (data){
          // drawCloud(data)
          console.log(data);
          window.location.reload();
          // console.log(shownum);
          $("#keywordshownum").val(shownum);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
                            console.log(XMLHttpRequest.status);
                            console.log(XMLHttpRequest.readyState);
                            console.log(textStatus);
       }
  });
};

    function ExportKeyword(){
    var num = $("#keywordshownum").val();
     var form = $("<form>");
     form.attr('style', 'display:none');
     form.attr('target', '');
     form.attr('method', 'get');
     form.attr('action', '/export_keyword');//导出对应格式的相应数量

     var input1 = $('<input>');
     input1.attr('type', 'hidden');
     input1.attr('name', 'num');
     input1.attr('value', num);      /* JSON.stringify($.serializeObject($('#searchForm'))) */

     $('body').append(form);
     form.append(input1);

     form.submit();
     form.remove();
}