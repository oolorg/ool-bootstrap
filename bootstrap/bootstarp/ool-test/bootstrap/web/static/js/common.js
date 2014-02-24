function page_load(url,method,form){
	if(method=="GET"){
		self.location.href = url;
	}
	else{
    		var f = document.forms[form];
    		f.action = url;
		f.method = "POST";
    		f.submit();
	}
}

function show_dialog(message){
	if(window.confirm(message)){
		return true;
	}
	else{
		return false;
	}
}

function sleep(time){ 
	var d1 = new Date().getTime(); 
   	var d2 = new Date().getTime(); 
   	while( d2 < d1+1000*time ){
       		d2=new Date().getTime(); 
   	} 
   	return; 
}

function set_value(elementId,value){
	document.getElementById(elementId).value=value;
	return;
}

