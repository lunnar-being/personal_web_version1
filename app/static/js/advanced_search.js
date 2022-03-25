function addBox(obj){
    console.log('ewf')
	html = '<div class="input-group saltIp" style="width:100%;padding:0 0 1px 0;">'+
						'<label class="input-group-addon">IP:</label>'+
						'<input type="text" class="form-control" id="saltIp" style="max-width:145px;">'+
						'<label class="input-group-addon">API端口:</label>'+
						'<input type="text" class="form-control" id="apiPort" style="max-width:90px;">'+
						'<label class="input-group-addon">类型:</label>'+
						'<select class="form-control" id="saltType" style="min-width:70px;">'+
							'<option value="0">master</option>'+
							'<option value="1">代理</option>'+
						'</select>'+
						'<label class="input-group-addon">区域:</label>'+
						'<select class="form-control" id="overSeas" style="min-width:70px;">'+
							'<option value="0">大陆</option>'+
							'<option value="1">海外</option>'+
						'</select>'+
						'<span class="input-group-btn">'+
    						'<button class="btn btn-info" type="button" data-toggle="tooltip" title="删除" id="delSaltIpGrp"><span class="glyphicon glyphicon-minus"></span></button>'+
    					'</span>'+
					'</div>'
	obj.insertAdjacentHTML('beforebegin',html)
}
// function Test1(){
//     console.log("sdwuji")
// };
$(document).on('click','#delSaltIpGrp',function(){
	var el = this.parentNode.parentNode
	var saltIp = $(this).parent().parent().find('#saltIp').val()
	if (saltIp == ""){
		el.parentNode.removeChild(el)
		return
	}
	alertify.confirm('您确定要删除选中的命令？',
	function(e){
		if(e){
			$.ajax({
				'url':'/url',
				'type':'POST',
				'async':false,
				'dataType':'json',
				'data':{'type':'delSaltIp','projectId':projectId,'saltIp':saltIp},
				'success':function(result){
					if (result.code){
						el.parentNode.removeChild(el)
					}else {
						showError(result.msg)
					}
				}
			})

		}
	})

})