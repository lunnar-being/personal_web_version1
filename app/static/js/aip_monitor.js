// AIP监测的显示数量控制
function AipMonitorNum(){
      var shownum = $("#entityshownum").val();
      $.ajax({
        url: "/aip_monitor_entity",
        type: "POST",
        data: {"num":shownum},
        dataType: "json",
        success: function (data){
          // drawCloud(data)
          console.log(data);
          window.location.reload();
          // console.log(shownum);
          $("#entityshownum").val(shownum);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
                            console.log(XMLHttpRequest.status);
                            console.log(XMLHttpRequest.readyState);
                            console.log(textStatus);
       }
  });
};
function AipInsNum(){
      var shownum = $("#insshownum").val();
      $.ajax({
        url: "/aip_monitor_ins",
        type: "POST",
        data: {"num":shownum},
        dataType: "json",
        success: function (data){
          // drawCloud(data)
          console.log(data);
          window.location.reload();
          // console.log(shownum);
          $("#insshownum").val(shownum);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
                            console.log(XMLHttpRequest.status);
                            console.log(XMLHttpRequest.readyState);
                            console.log(textStatus);
       }
  });
};
function AipLinkNum(){
      var shownum = $("#linkshownum").val();
      $.ajax({
        url: "/aip_monitor_link",
        type: "POST",
        data: {"num":shownum},
        dataType: "json",
        success: function (data){
          // drawCloud(data)
          console.log(data);
          window.location.reload();
          // console.log(shownum);
          $("#linkshownum").val(shownum);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
                            console.log(XMLHttpRequest.status);
                            console.log(XMLHttpRequest.readyState);
                            console.log(textStatus);
       }
  });
};


function ExportEntity(){
    var num = $("#entityshownum").val();
     var form = $("<form>");
     form.attr('style', 'display:none');
     form.attr('target', '');
     form.attr('method', 'get');
     form.attr('action', '/export_entity');//导出对应格式的相应数量

     var input1 = $('<input>');
     input1.attr('type', 'hidden');
     input1.attr('name', 'num');
     input1.attr('value', num);      /* JSON.stringify($.serializeObject($('#searchForm'))) */

     $('body').append(form);
     form.append(input1);

     form.submit();
     form.remove();
}
function ExportIns(){
    var num = $("#insshownum").val();
     var form = $("<form>");
     form.attr('style', 'display:none');
     form.attr('target', '');
     form.attr('method', 'get');
     form.attr('action', '/export_ins');//导出对应格式的相应数量

     var input1 = $('<input>');
     input1.attr('type', 'hidden');
     input1.attr('name', 'num');
     input1.attr('value', num);      /* JSON.stringify($.serializeObject($('#searchForm'))) */

     $('body').append(form);
     form.append(input1);

     form.submit();
     form.remove();
}
function ExportLink(){
    var num = $("#linkshownum").val();
     var form = $("<form>");
     form.attr('style', 'display:none');
     form.attr('target', '');
     form.attr('method', 'get');
     form.attr('action', '/export_link');//导出对应格式的相应数量

     var input1 = $('<input>');
     input1.attr('type', 'hidden');
     input1.attr('name', 'num');
     input1.attr('value', num);      /* JSON.stringify($.serializeObject($('#searchForm'))) */

     $('body').append(form);
     form.append(input1);

     form.submit();
     form.remove();
}
