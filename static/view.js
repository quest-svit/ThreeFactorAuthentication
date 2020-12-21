function myFunction() 
{
	var xhr = new XMLHttpRequest();
	var url = "/";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var json = JSON.parse(xhr.responseText);
			console.log(json.username + ", " + json.password);
					   
		}
	};element_1,element_2
	var data = JSON.stringify({"username": document.getElementById("element_1").value , "password": document.getElementById("element_2").value});
	xhr.send(data);
}
