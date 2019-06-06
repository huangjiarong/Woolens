<%@ page language="java" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsf/html" prefix="h" %>
<%@ taglib uri="http://java.sun.com/jsf/core" prefix="f" %>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    	<title>添加付款单</title>
    	<jsp:include page="cssLoad.jsp"></jsp:include>
    	<style>
    		.paymen{
    		    order-radius:2px;
    			background:gray;
    		}
    	</style>
	</head>
	<body>
	
		<jsp:include page="besize.jsp"></jsp:include>
		<div class="row wrapper border-bottom white-bg page-heading">
                <div class="col-lg-10">
                    <h2>Foo表格</h2>
                    <ol class="breadcrumb">
                        <li>
                            <a href="index.html">主页</a>
                        </li>
                        <li>
                            <a>表格</a>
                        </li>
                        <li class="active">
                            <strong>添加付款单</strong>
                        </li>
                    </ol>
                     <a type="hidden" id='tag' href='javascript:void(0)'></a>
                </div>
        </div>
	<div class="wrapper-content"> 
 	<div class="ibox-content">
    <div class="text-center">
	  <div class="row">
	  	<h4 class="pull-left">单据编号:<span></span></h4>
	  </div>
	  <span>
		  <input id="payunit" type="text" class="typeahead_1 form-control pull-left" style="width: 15%" placeholder="付款单位"/>
	  </span>
	  <!-- <input id="payman" data-type="select" data-title="Select status"></input> -->
	  <div class="btn-group pull-right" role="toolbar" aria-label="...">
	      <input id='sub' type="button" class="btn btn-primary" value='提交' style="margin-right: 2px;"></input>
	      <button id="addRowbtn" type="button" class="btn btn-primary"><i class="fa fa-plus"></i></button>
      </div>
	</div>
		<table class="table-responsive" id="List"></table>	
		<!--  第二个表格-->
    <div class="text-center">
    <div class="btn-group pull-right" role="toolbar" aria-label="...">
      <button type="button" class="btn btn-primary" id="chirdTableaddRowbtn"><i class="fa fa-plus"></i></button>
    </div>
	</div>
    	<table class="table-responsive" id="chirdTable"></table>	
    </div>
    <div class="modal " id="materialNameModal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog" style="width:1000px;">
            <div class="modal-content animated bounceInRight">
                  <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <i class="fa fa-laptop modal-icon"></i>
                        <h4 class="modal-title">模态标题</h4>
                        <i id="indexFlag" style="display: none;"></i>
                  </div>
                  <div class="modal-body">
                      <div class="container-fluid">
                          <div class="row form-horizontal">
                          <div class="form-group">
                                  <h4>标题名:</h4>
                              <div class="col-md-12">
                                <table id="goodsTable"></table>
                              </div>
                          </div>
                          </div>                  
                      </div>                                                  
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-primary" data-dismiss="modal" style="margin-bottom:0px;">关闭</button>
                      <button id="testid" type="button" data-dismiss="modal" class="btn btn-primary" onclick="setpayunit()">选择</button>
                      
                  </div>
             </div>
        </div>
    </div>
    <div class="modal " id="chirdTableModel" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog" style="width:1000px;">
            <div class="modal-content animated bounceInRight">
                 <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <i class="fa fa-laptop modal-icon"></i>
                        <h4 class="modal-title">模态标题</h4>
                        <i id="indexFlag" style="display: none;"></i>
                    </div>
                    <div class="modal-body">
                        <div class="container-fluid">
                            <div class="row form-horizontal">
                            <div class="form-group">
                                    <h4>摇纱回毛:</h4>
                                <div class="col-md-12">
                                  <table id="secondTab"></table>
                                </div>
                            </div>
                            </div>                  
                        </div>                                                  
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-dismiss="modal" style="margin-bottom:0px;">关闭</button>
                        <button id="secondsub" type="button" data-dismiss="modal" class="btn btn-primary" onclick="getValues()">选择</button>
                        
                    </div>
               </div>
            </div>
     </div>
	</div>
		<jsp:include page="footer.jsp"></jsp:include>
	  </div>
		<jsp:include page="jsLoad.jsp"></jsp:include>
		<script type="text/javascript" src="${pageContext.request.contextPath}/js/bootstrap3-typeahead.min.js"></script>
<script>
 $(document).ready(function() {

     $('.footable').footable();
     $('.footable2').footable();
 });

	
 <!-- 随机生成订单号，此方法为别人的，需要进一步改写 -->

function randomNum(minNum,maxNum){
var today = new Date();
var day   = today.getDate(); //获取当前日(1-31)
var month = today.getMonth() + 1; //显示月份比实际月份小1,所以要加1
var year  = today.getYear();  //获取完整的年份(4位,1970-????)  getFullYear()
var years=today.getFullYear();
years= years<99?"20"+years:years;
month    = month<10?"0"+month:month;  //数字<10，实际显示为，如5，要改成05
day   = day<10?"0"+day:day;
var hh=today.getHours();
hh   = hh<10?"0"+hh:hh;
var ii=today.getMinutes();
ii   = ii<10?"0"+ii:ii;
var ss= today.getSeconds();
ss   = ss<10?"0"+ss:ss;
var dada = years+month+day+hh+ii+ss;//时间不能直接相加，要这样相加！！！14位

    switch(arguments.length){
        case 1:
            return dada+parseInt(Math.random()*minNum+1,10);
            //newOrderId = dada+parseInt(Math.random()*minNum+1,10);
        break;
        case 2:
            return dada+parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
            //newOrderId = dada+parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
        break;
            default:
                return 0;
                //newOrderId = 0;
            break;
    }
}
//var aa=randomNum(1,10000);
//alert(aa);

		 if($('h4.pull-left>span').text()==''){
		 	newOrderId = randomNum(1,1000); 
      	    $('h4.pull-left>span').text(newOrderId);
         }else{
         	newOrderId = $('h4.pull-left>span').text();
         }

//alert(newOrderId);
//var newOrderId = 0;// randomNum(1,1000);//此处不用var，定义了一个全局变量，只有后面的函数执行，此变量才生效。

function addNewId() {
    newOrderId = randomNum(1,1000);
}
/*    	
$('.typeahead_1').typeahead({
    source: function(query,process){
    	return $.ajax({
         	url:'<%=path%>/clientSource.do',
         	type:'post',
         	contentType:'application/json;charset=utf-8',
         	success:function(data){
         		var array = $.map(data,function(value,n){
         			return value['name'];
         		})
         		return array;
         	}
         });
    }
});
*/

function setpayunit(){
	 var  array = selected('goodsTable');
	 $("#payunit").attr('value',array[0]['name']);
	 
}

<!-- 随机生成订单号，end-->
		 function modeldata(){
                    this.id='';
                    this.number=newOrderId;
                    this.account='';
                    this.paysum= '';
                    this.settlenumber='';
                    this.dealdate='';
                    this.remarks='';
                    this.drawee='';
                    this.paytype='';
                    this.paynumber='';
			    };
			    
			    function childTableData(){
			       this.id='';
                   this.sourcenumber='';
                   this.businesstype='';
				   this.dealdate='';
				   this.amountmoney='';
				   this.havecancel='';
				   this.nocancel='';
				   this.cancel='';
				
			    }
     
      $(function () {
				$.fn.bootstrapTable.columnDefaults.valign = 'middle';//设置垂直居中    
                $.fn.editable.defaults.mode = 'inline';//编辑方式为内联方式
                $.fn.editable.defaults.showbuttons = false;//设置所有的元素不显示按钮
                $.fn.editable.defaults.emptytext = '   ';//设置默认空文本
                $.fn.editable.defaults.onblur = "submit";//当失去焦点时自动提交
                $.fn.editable.defaults.inputclass="inputclass";//定义input的样式
                $.fn.editable.defaults.defaultValue='';
                $.fn.bootstrapTable.columnDefaults.class='not-wrap';
                <!--table start-->
			    $('#List').bootstrapTable({
			    	method:'POST',
			        dataType:'json',
			        contentType: "application/x-www-form-urlencoded",
			        cache: false,
			        striped: true,                              //是否显示行间隔色
			        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
			    //    showColumns:true,
			        pagination:true,
			        minimumCountColumns:2,
			        pageNumber:1,                       //初始化加载第一页，默认第一页
			        pageSize: 8,                       //每页的记录行数（*）
			        pageList: [10, 15, 20, 25],        //可供选择的每页的行数（*）
			        uniqueId: "id", //每一行的唯一标识，一般为主键列
            		data:[new modeldata(),new modeldata(),new modeldata()],
			        columns: [
			        	{
			        		checkbox:'true'
			        	},
			         	{//为每一行添加index的方法
                            field:'index',
                            title:'index', 
                            formatter:function (value,row,index){
                                row.index = index;
                                return index;
                            }
                        },{
				                field: 'id',
								title: 'id'
				    	},
						{
									field: 'number',
									title: '单据编号',
									visible:'false'
						},
						{
											field: 'account',
											title: '付款账号',
											editable: {
									     	type: 'select',
                                   			autotext:'always',
                                   			defaultValue:1,
									     	source:"<%=path%>/accountsource.do",
		                                	noeditFormatter: function (value,row,index) {
		                                        var result={filed:"account",value:value,class:"badge",style:"padding:5px 10px;"};
		                                        return result;
		                                          },
		                                   validate:function(value){
						     					if($.trim(value)==""){
						     					return "不能为空!";
		                                    }
						     		}
						     	}  
							},{
								
											field: 'paytype',
											title: '结算方式',
											editable: {
									     	type: 'select',
                                   			autotext:'always',
                                   			defaultValue:1,
									     	source:getSelect('settletype','settletype'),
		                                	noeditFormatter: function (value,row,index) {
		                                        var result={filed:"paytype",value:value,class:"badge",style:"padding:5px 10px;"};
		                                        return result;
		                                          },
		                                   validate:function(value){
						     					if($.trim(value)==""){
						     					return "不能为空!";
		                                    }
						     		}
						     	}  
							},{
                                    field: 'paysum',
                                    title: '付款金额',
                                    editable:{
										type:'text',
										validate:function(value){
											if($.trim(value)==""){
												return "不能为空!";
											}else if(isNaN(Number(value))){
												return "请输入数字!";
											}
										}
									}
                        },{ 
                                    field: 'settlenumber',
                                    title: '结算号',
                                    editable:{
										type:'text',
										validate:function(value){
											if($.trim(value)==""){
												return "不能为空!";
											}else if(isNaN(Number(value))){
												return "请输入数字!";
											}
										}
									}
                        },{
											field: 'drawee',
											title: '付款人',
											editable: {
									     	type: 'select',
                                   			autotext:'always',
                                   			defaultValue:1,
									     	source:"<%=path%>/staffSource.do",
		                                	noeditFormatter: function (value,row,index) {
		                                        var result={filed:"drawee",value:value,class:"badge",style:"padding:5px 10px;"};
		                                        return result;
		                                          },
		                                   validate:function(value){
						     					if($.trim(value)==""){
						     					return "不能为空!";
		                                    }
						     		}
						     	}  
							},{
                            field: 'dealdate',
                            title: '日期',
                            /*class: 'not-wrap',*/
                            editable: {
                                //添加设置为弹出式,将显示在右边
                                mode:'popup',
                                placement:'left',
                                showbuttons:true,
                                type: 'date',
                                format: 'yyyy-mm-dd',    
                                viewformat: 'yyyy-mm-dd',    
                                datetimepicker: {
                                    weekStart: 1
                                },
                                validate:function(value){
						     		if($.trim(value)==""){
						     			return "不能为空!";
						     		}
						     	} 
                            } 
                        },{
                                    field: 'remarks',
                                    title: '备注',    
                                    editable: {
                                    type: 'text',  
                            } 
                        }
					]
				});
				 $('#chirdTable').bootstrapTable({
							method:'POST',
								dataType:'json',
								contentType: "application/x-www-form-urlencoded",
								cache: false,
								striped: true,                              //是否显示行间隔色
								sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
						//    showColumns:true,
								pagination:true,
								minimumCountColumns:10,
								pageNumber:1,                       //初始化加载第一页，默认第一页
								pageSize: 10,                       //每页的记录行数（*）
								pageList: [10, 15, 20, 25],        //可供选择的每页的行数（*）               //
								data: [
								new childTableData(),
								new childTableData(),
								new childTableData()
							],
							onEditableSave: function (field, row, oldValue, $el) {
			         //判断改变的是否为颜色,如果是的话更新色号这一项
			         if (field=="color") {
                            var cell = {
                                index:row['index'],
                                field:'colornum',
                                value:row['color']
                            };
                        $('#chirdTable').bootstrapTable("updateCell",cell);  
                        };
			         if(field=="processcost"){
			         	if(row['weight']!=''){
			         	var cell = {
                                index:row['index'],
                                field:'totalprocess',
                                value:row['weight']*row[field]
                            };
			         	$('#chirdTable').bootstrapTable("updateCell",cell);
			         	if(row['totalcost']!=''){
				         	var cell = {
	                                index:row['index'],
	                                field:'sum',
	                                value:(row['totalcost']-0)+(row['totalprocess']-0)
	                            };
				         	$('#chirdTable').bootstrapTable("updateCell",cell);
				         	} 
			         	} 
			         };
			         if(field=="unitcost"){
			         	if(row['weight']!=''){
			         	var cell = {
                                index:row['index'],
                                field:'totalcost',
                                value:row['weight']*row[field]
                            };
			         	$('#chirdTable').bootstrapTable("updateCell",cell);
			         	if(row['totalprocess']!=''){
				         	var cell = {
	                                index:row['index'],
	                                field:'sum',
	                                value:(row['totalcost']-0)+(row['totalprocess']-0)
	                            };
				         	$('#chirdTable').bootstrapTable("updateCell",cell);
				         	} 
			         	} 
			         };
			         if(field=="weight"){
			         	if(row['unitcost']!=''){
			         	var cell = {
                                index:row['index'],
                                field:'totalcost',
                                value:row['unitcost']*row[field]
                            };
			         	$('#chirdTable').bootstrapTable("updateCell",cell);
			         	if(row['processcost']!=''){
			         	var cell = {
                                index:row['index'],
                                field:'totalprocess',
                                value:row['processcost']*row[field]
                            };
			         	$('#chirdTable').bootstrapTable("updateCell",cell);
			         	} 
			         	var cell = {
                                index:row['index'],
                                field:'sum',
                                value:(row['totalcost']-0)+(row['totalprocess']-0)
                            };
			         	$('#chirdTable').bootstrapTable("updateCell",cell);
			         	};
			         };
            		},
							columns: [
                            {
                                checkbox:true,
                            },{
                            field:'index',
                            title:'index', 
                            formatter:function (value,row,index){
                                row.index = index;
                                return index;
                            },
                            },
                            {
									field: 'id',
									title: 'id'
							},{
									field:'sourcenumber',
									title:'源单号'
							},{
									field:'businesstype',
									title:'业务类别'
							},{
									field:'dealdate',
									title:'单据日期'
							},{
									field:'amountmoney',
									title:'单据金额'
							},{
									field:'havecancel',
									title:'已核销金额'
							},{
									field:'nocancel',
									title:'未核销金额'
							},{
									field:'cancel',
									title:'本次核销金额',
									editable:{
										type:'text',
										validate:function(value){
											if($.trim(value)==""){
												return "不能为空!";
											}else if(isNaN(Number(value))){
												return "请输入数字!";
											}
										}
									}
							}
						]
					});


					$('#chirdTableaddRowbtn').click(function(){
									$('#chirdTable').bootstrapTable('append',new childTableData());
							});
					<!--table end-->   
					//子表的取货表
					$('#secondTab').bootstrapTable({
                                method:'POST',
                                dataType:'json',
                                contentType: "application/x-www-form-urlencoded",
                                cache: false,
                                striped: true,                              //是否显示行间隔色
                                sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
                                showColumns:true,
                                pagination:true,
                                minimumCountColumns:2,
                                pageNumber:1,                       //初始化加载第一页，默认第一页
                                pageSize: 9,                       //每页的记录行数（*）
                                pageList: [10, 15, 20, 25],        //可供选择的每页的行数（*）
                                search:true,
                        columns: [
                        {
                            checkbox:true,
                        },
                        {   
                            field:'id',
                            title:'id'
                        },
                        {
                                    field: 'number',
                                    title: '单据编号',          
                        },{
                        			field:'sourcenumber',
                        			title:'源单号'
                        },
                     {
                        field: 'businesstype',
                        title: '业务类别'
                    },
                    {
                        field: 'dealdate',
                        title: '单据日期',
                    },
                     {
                        field: 'amountmoney',
                        title: '单据金额',
                       
                    },
                    {
                        field: 'havecancel',
                        title: '已核销金额',
                        
                    },{
                    	field:'nocancel',
                    	title:'未核销金额'
                    }
                        ]
                    });
					
			});
			
		
		$('#goodsTable').bootstrapTable({
								url:'<%=path%>/clientSource.do',
                                method:'POST',
                                dataType:'json',
                                contentType: "application/x-www-form-urlencoded",
                                cache: false,
                                striped: true,                              //是否显示行间隔色
                                sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
                                showColumns:true,
                                pagination:true,
                                minimumCountColumns:2,
                                pageNumber:1,                       //初始化加载第一页，默认第一页
                                pageSize: 9,                       //每页的记录行数（*）
                                pageList: [10, 15, 20, 25],        //可供选择的每页的行数（*）
                                uniqueId: "id",   
                                search:true,
                  
                        data: [],
                        columns: [
			        	{
			        		checkbox:'true'
			        	},
			         	{//为每一行添加index的方法
                            field:'index',
                            title:'index', 
                            formatter:function (value,row,index){
                                row.index = index;
                                return index;
                            }
                        },{
				                field: 'id',
								title: 'id'
				    	},
						{
									field: 'number',
									title: '客户编号',
						},
                        {
                                    field: 'name',
                                    title: '客户名称'
                        },{
                                    field: 'telephone',
                                    title: '电话'
                        },{
                            
                                    field: 'clienttype',
                                    title: '客户类别',
                                    editable: {
                                        type: 'select',
                                        pk: 1,
                                        defaultValue:1,
                                        autotext:'always', //添加该标签使得html显示text
                                        source: getSelect('clientType','clientType'),
                                        noeditFormatter: function (value,row,index) {
                                                        var result={filed:"clienttype",value:value,class:"badge",style:"padding:5px 10px;"};
                                                        return result;
                                                }
                            }
                            
                        },{
                                    field: 'trnumber',
                                    title: '纳税人识别号'
                        }
                        ]
                    });
                      
         function getValues(){
	         var values = $("#secondTab").bootstrapTable('getSelections');//获取select的值
	         var dataSum = values.map(function (item,index,array){
				var arr = [];
				arr['0'] = true;
				arr['id'] = item['id'];
				arr['sourcenumber'] = item['sourcenumber'];
				arr['businesstype'] = item['businesstype'];
				arr['dealdate'] = item['dealdate'];
				arr['amountmoney'] = item['amountmoney'];
				arr['havecancel'] = item['havecancel'];
				arr['nocancel'] = item['nocancel'];
				arr['cancel'] = item['nocancel'];
				return arr;
			 })
	         //更新一行
	         $('#chirdTable').bootstrapTable('updateRow',{index:$('#indexFlag').text(),row:dataSum[0]});
         }
		//为basicTable添加双击事件
	    $("#List").on('dbl-click-cell.bs.table',function (field,value,row,$element,target){
	        if(value == 'materialname')//双击时无法绑定是哪一个单元格,所以需要对单元格进行验证
	        {
	            var cellIndex = target[0].parentElement.rowIndex-1;//获取当前双击单元格的index
	            $('#indexFlag').text(cellIndex);//将点击的单元的index传给模态对话款
	            $('#materialNameModal').modal('toggle');//调用模态对话框
	             $('#goodsTable').bootstrapTable('refresh',{silent:true});
	        }   
	    });	
	    
	    //为chirdTable添加双击事件
	    $("#chirdTable").on('dbl-click-cell.bs.table',function (field,value,row,$element,target){
	        if(value == 'sourcenumber')//双击时无法绑定是哪一个单元格,所以需要对单元格进行验证
	        {
	        	var client = $("#payunit").val();
	            $('#secondTab').bootstrapTable('refresh',{url:"<%=path%>/getDueByClient.do?client="+client});
	            var cellIndex = target[0].parentElement.rowIndex-1;//获取当前双击单元格的index
	            $('#indexFlag').text(cellIndex);//将点击的单元的index传给模态对话款
	            $('#chirdTableModel').modal('toggle');//调用模态对话框
					
	        }   
	    });
	    
		
		
		function selected(tableid){
        var array = $('#'+arguments[0]).bootstrapTable('getSelections');
        if(array.length==0)return false;
        //console.log(JSON.stringify(array));
        return array;
    	}
		
		
	
		//<div class="editable-error-block help-block" style="">不能为空!</div>
		//向后台服务器获取数据,将其放在select中
		function getSelect(selectName,selectId){
			var selects = [];
			$.ajax({
				type:'post',
				url:"<%=path%>/assisttable.do?tableName="+selectName,
				contentType:'application/json;charset=utf-8',
				async:false,
				success:function(data){
					$.each(data,function(n,value){
						var jsontemp = {};
						jsontemp['value'] = value.id;
						jsontemp['text'] = value.name;
						selects.push(jsontemp);
					});
					//selectValue[selectId] = jsontemp['value'];
				}
			});
	
			return selects; 
		}
		
		$('#addRowbtn').click(function addOreder(){
                $('#List').bootstrapTable('prepend',new modeldata());
         });	    
            window.onkeydown = function(e){
            	if(9 == e.keyCode&&e.target.tagName=="INPUT"){
            		console.log(e.target.tagName);
            		/*$(e.target).closest('td').find('a').editable('hide');*/
            		//console.log($(e.target).closest('td').next('a'));
            		$(e.target).closest('td').next().find('a').editable('show');
            	}
            }
        //验证是否有填字段  
         //验证是否有填字段  
        $('#sub').click(function (e){
        $("#tag").click();
        //获取所选择的数据,为了得到被选择了的列array[i]['index']
        // var  array = getSelect('basicTable');
        var  array = selected('List');
        //获取table下面的所有的td数组
        // var aList = $('#basicTable tr');
        var trList = $('#List tr');
        /*console.log(trList);*/
        if(!validate(trList,array))
       	 e.stopImmediatePropagation();
       	 var  array = selected('chirdTable');
        //获取table下面的所有的td数组
        // var aList = $('#basicTable tr');
        var trList = $('#chirdTable tr');
        /*console.log(trList);*/
        if(!validate(trList,array))
       	 e.stopImmediatePropagation();
        return false;
    });
    
    	function validate(trList,array){
    	 var flag = true;
        for(var i=0;i<array.length;i++){
           var index = array[i]['index'] + 1;
           var tdList = trList[index].getElementsByTagName('td');
           for(var j=0;j<tdList.length;j++){
           		//判断是否合法,来觉定是否打开输入框,在添加一个flag来标识本次输入是否合法
           		var $a = $(tdList[j]).find('a');
           		/*console.log($a.editable('validate'));*/
           		if(JSON.stringify($a.editable('validate'))!='{}'){
                	$a.editable('show',false);
                	flag = false;
                	}
           }
           setTimeout('$("#tag").click()',200);
        }
        setTimeout('$("#tag").click()',200);
        return flag;
    	}
    var SUBITEM = false;
    //提交数据
    $("#sub").click(function(event){
    			if(SUBITEM){
    				return false;
    			}
    			SUBITEM = true;
				var array = selected('List').slice(0);
				$.each(array,function(n,value){
					if(value.hasOwnProperty('error'))
					$('#List').bootstrapTable("updateCell",{index:value.index,field:'error',value:false});
				})
  				var copy = JSON.parse(JSON.stringify(array));
  				var indexArr = $.map(array,function(value,n){
  					return value['index'];
  				}) 
				$.each(copy,function(n,value){
		        	delete value['0'];
		        	delete value['index'];
		        	delete value['error'];
		        });
		        var data = {indexArr:indexArr,t:copy};
		        var json = JSON.stringify(data);
		        console.log(json);
				$.ajax({
					type:"post",
					url:"<%=path%>/addReelingList.do",
					contentType:'application/json;charset=utf-8',
					data:json,
					success:function(data){
					SUBITEM = false;
					console.log(data)
					if(data.length<=0){
						$("#List").bootstrapTable("refresh",{url:"<%=path%>/findReelingByNumber.do?number="+newOrderId});
						alert('添加成功!');
						}else{
							console.log('进入错误判断区');
						for(var i=0;i<data.length;i++){	
							if(data[i].fieldString==null){
							    alert(data[i].message);
						    }else{
								$('#List').bootstrapTable("updateCell",{index:data[i].index,field:data[i].fieldString,value:data[i].message});
								$('#List').bootstrapTable("updateCell",{index:data[i].index,field:'error',value:true});
							}
							}
						}
					},
					error:function(request,error,errorThrown){
						SUBITEM = false;
						if(error!=null){
							alert(error);
						}else{
							alert('出现错误!');
						}
					}
					
				});
			
			
		});
	
		/*function getNumber(number){
			var flag;
			$.ajax({
				async:false,
				type:'post',
				url:"<%=path%>/processNumber.do?newNumber="+number,
				contentType:'application/json;charset=utf-8',
				success:function(data){
					flag = data;
					console.log(data);
				}
			})
			return flag;
		}*/
		
	$("#payunit").dblclick(function(){
		  $('#materialNameModal').modal('toggle');//调用模态对话框
	});
		
</script>
	</body>
</html>