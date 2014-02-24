new Ajax.Request(
　　　　　"cgi-bin/ajax.py",
　　　　　{ method: 'get',  onComplete: displayData }); 

function displayData(responseHttpObj) {
	//alert(responseHttpObj.responseText);
	document.getElementById("test2").innerHTML = responseHttpObj.responseText;
} 
