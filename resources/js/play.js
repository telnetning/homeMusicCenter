$(document).ready(function(){
	var timer;
	var audio=$("#audio")[0];
	var Songs;
	var index=0;
	var forward=1;  //forward=1下一首 forward=0上一首
	var canvas=$("#canvas");
	var canvas_width=parseInt(canvas.css("width"));
	
	loadSong();

	//	去掉button a input点击时的边框
	$("button,a,input").focus(function(){
		this.blur()
	})

	$("#play").click(function(){
		
		if(audio.paused){
			audio.play();
			$("#play span").removeClass("glyphicon-play").addClass("glyphicon-pause").css("color","rgb(74,0,255)");
			timer=setInterval(playedTime,500);
			$("#img").addClass("rotate");
		}else{
			audio.pause();
			$("#play span").removeClass("glyphicon-pause").addClass("glyphicon-play");
			// $("#img").removeClass("rotate");
			clearInterval(timer);
		}
	})

	//按钮组
	
	$("#repeat").click(function(){
		if(audio.loop){
			audio.loop=false;
			$("#repeat span").css("color","rgba(74,0,255,0.5)");
		}else{
			audio.loop=true;
			$("#repeat span").css("color","rgb(74,0,255)");		
		}

	});
	$("#random").click(function(){
		// if(audio.loop){
		// 	audio.loop=false;
		// 	$("#repeat span").css("color","rgba(74,0,255,0.5)");
		// }else{
		// 	audio.loop=true;
		// 	$("#repeat span").css("color","rgb(74,0,255)");		
		// }

	});

	$("#backward").click(function(){
		nextSong(0);
	});
	$("#forward").click(function(){
		nextSong(1);
	});
	　
///////////////////////

	$(".range").mouseover(function(){

		$(".range_in").css("background-color","rgba(0,0,255,0.6)");
	})
	$(".range").mouseout(function(){
		$(".range_in").css("background-color","rgba(0,0,0,0)");
	})


	//拖拽进度条
	// $(".range_in").mousedown(function(e){
	// 	var e=e || window.event;
	// 	var disX=e.pageX-$(".range_in").offset().left;
	// 	// _x=e.pageX-offset_left;
	// 	console.log(disX)
	// 	$(".range").mousemove(function(e){
	// 		var e=e || window.event;
	// 		var x=e.pageX-disX;
	// 		if (x>=max_width){
	// 			$(".range_in").css("left",max_width);
	// 			audio.ended=true;
	// 		}else{
	// 			$(".range_in").css("left",x);
				
	// 			// audio.ontimeupdate=function(){
	// 			// 	audio.currentTime=audio.currentTime+x/max_width*audio.duration;
	// 			// }

	// 			// console.log(audio.currentTime);

	// 		}
			

	// 		return false; 
	// 	}).mouseup(function(){
	// 		$(".range").off("mousemove");
	// 		$(".range").off("mousedown");
	// 	});

	// });

	var _x;
	var max_width=parseInt($(".range").css("width"));
	var offset_left=parseInt($(".range_in").offset().left);
	
	$(".range").click(function(e){
		// audio.pause();

		var e=e || window.event;
		var _x=e.pageX-offset_left;
		var x=e.pageX-_x;
		
		$(".range_in").css("left",_x-10);

		var left=parseInt($(".range_in").css("left"));
		audio.currentTime=audio.duration*(left/max_width);
		
		// console.log(audio.currentTime)
		// console.log(left+"   "+audio.duration*(left/max_width))

	});

	function loadSong(){
		var url="js/song.json";
		var time;
		$.get(url,function(data){
			
			Songs=data["songs"];

			// console.log(Songs[0].src)

			for (var i=0;i<Songs.length;i++){
				var li='<li class="li list-group-item"><a href="javascript:"><span class="span1 glyphicon glyphicon-music"></span></a><span class="glyphicon glyphicon-heart heart" title="添加到‘我的收藏’"></span><span class="glyphicon glyphicon-remove remove" title="从列表中删除"></span></li>';

				$("#music_list ul").append(li);
				$("#music_list ul li .span1")[i].innerHTML=" "+Songs[i].name+"——"+Songs[i].author;
			}
			
			curSong(Songs[0],0);

		},"json");

	}



	function playedTime(){
		var pre=(audio.currentTime/audio.duration).toFixed(2);
		var totalWidth=$("#played").css("width");
		var Total_min=Math.floor(audio.duration/60);
		var Total_second=parseInt(audio.duration)-Total_min*60;
		var Curr_min=Math.floor(audio.currentTime/60);
		var Curr_second=parseInt(audio.currentTime)-Curr_min*60;
		if(Curr_min<10){
			Curr_min="0"+Curr_min;
		}
		if (Curr_second<10){
			Curr_second="0"+Curr_second;
		}
		if(Total_min<10){
			Total_min="0"+Total_min;
		}
		if (Total_second<10){
			Total_second="0"+Total_second;
		}

		$("#song_time").html(Curr_min+":"+Curr_second+" / "+Total_min+":"+Total_second);

		if(audio.ended){
			$("#play span").removeClass("glyphicon-pause").addClass("glyphicon-play");
			
			clearInterval(timer);
			$("#played span").css("width",totalWidth);

			nextSong(1);

		}else{
			$("#played span").css("width",pre*parseInt(totalWidth));

		}

		$(".range_in").css("left",canvas_width*pre);


		// console.log(left/max_width+"   "+audio.currentTime/audio.duration);

		var gradient=g.createLinearGradient(0,0,canvas_width*pre,0);

			gradient.addColorStop("0","blue");
			gradient.addColorStop("1","magenta");
			// gradient.addColorStop("1","rgba(255,255,255,0)");
			g.strokeStyle=gradient;
					
	} //playedTime


	function nextSong( forward ){

		if(forward=="1"){
			if (index<Songs.length-1){
				index++;
				curSong(Songs[index],1);

			}else{
			  	if(index==Songs.length-1){
					index=0;

					curSong(Songs[index],0);
				}

			}
		}else{

			if (index>0){
				index--;
				curSong(Songs[index],1);

			}else{
				if(index==0){
				
				curSong(Songs[Songs.length-1],0);

				}			
			}
			
		}		

	}//nextSong


	//播放当前歌曲

	function curSong(current,auto){
			// console.log(current);

			audio.src=current.src;

			// time=Math.floor(audio.duration/60)+":"+audio.duration%60
			// console.log(audio.duration)
			$(".song_infor h2").html(current.name);
			$(".song_infor h4").html(current.author);
		
			if (current.cover && current.cover!=" "){
				$("#img").css("background-image",'url('+current.cover+')')
			}

			if(auto){
				$("#play").click();
			}
	}//curSong
		
	//由播放列表选歌	
	$("#music_list").on('click',"li a",function(){
		var cur_index=$(this).parent().index();
		curSong(Songs[cur_index],1);
		console.log(cur_index);

	});
		
	//我的收藏
	$("#myfav").hide();
	
	$("aside .my").children("span").click(function(){
		$("#myfav").toggle();
		if($("#myfav").is(":hidden")){
			$("aside .my").children("span").css('color','#000');
			// $("aside .my span").css('color','#000');

		}else{
			// $("aside .my ").css('color','red');
			$("aside .my").children("span").css('color','red');

		}

	});

	$("#music_list").on('click','.heart',function(){
		var cur_index=$(this).parent().index();
		var len=$("#myfav li").length;
		var flag=0;

		$(this).css("color","red");
		if(len==0){
			add();
			$("#myfav").append('<li class="list-group-item"><span class="span1 glyphicon glyphicon-music"></span><span class="glyphicon glyphicon-remove remove" title="从列表中删除"></span></li>')
			$("#myfav li .span1")[len].innerHTML=Songs[cur_index].name+"——"+Songs[cur_index].author;
			$("#myfav li")[len].id=cur_index;	
		}else{
			for (var i=0;i<len;i++){

				if( $("#myfav li")[i].id==cur_index){
					flag=1;
					add('已经添加！');
				}
			}
			if(!flag){
				add('添加成功！');

				$("#myfav").append('<li class="list-group-item"><span class="span1 glyphicon glyphicon-music"></span><span class="glyphicon glyphicon-remove remove" title="从列表中删除"></span></li>');
				$("#myfav li .span1")[len].innerHTML=Songs[cur_index].name+"——"+Songs[cur_index].author;
				$("#myfav li")[len].id=cur_index;
			
			}
		}

	});

	//从我的收藏中删除
	$("#myfav").on("click",".remove",function(){
		var id=$(this).parent()[0].id;
		$(this).parent().remove();
		var li=$("#music_list li:eq("+id+")");
		// li.css("background-color","#ccc");
		li.find(".heart").css("color","");
		add('删除成功！');
	});
	//播放收藏列表
	$("#myfav").on("click",".span1",function(){
		var id=$(this).parent()[0].id;
		curSong(Songs[id],1);
	});



	function add(txt){
		// alert("haha");
		$("#pop").animate({top:'130px',opacity:'1'},800);
		$("#pop").animate({top:'130px',opacity:'1'},300);
		$("#pop").animate({top:'115px',opacity:'0'},500);
		
		$("#pop p").html(txt);

	}


 })//document



//波形输出

var AudioContext=AudioContext|| webkitAudioContext;
var context=new AudioContext;
//从元素创建媒体节点
var media=context.createMediaElementSource(audio);
//创建脚本处理节点
var processor=context.createScriptProcessor(4096,1,1);
//Canvas初始化
var width=canvas.width,height=canvas.height;
var g=canvas.getContext("2d");
g.translate(0.5,height/2+0.5);
//连接：媒体节点→控制节点→输出源
media.connect(processor);
processor.connect(context.destination);
//控制节点的过程处理
processor.onaudioprocess=function(e){
  //获取输入和输出的数据缓冲区
  var input=e.inputBuffer.getChannelData(0);
  var output=e.outputBuffer.getChannelData(0);
  //将输入数缓冲复制到输出缓冲上
  for(var i=0;i<input.length;i++)output[i]=input[i];
  //将缓冲区的数据绘制到Canvas上
  g.clearRect(-0.5,-height/2-0.5,width,height);
  g.beginPath();
  for(var i=0;i<width;i++)
    g.lineTo(i,height/2*output[output.length*i/width|0]);
	// setInterval(function(){


	// },1000)
	  g.stroke();
};


