var timeoutID;
var timeout = 1000;

var messageCount = 0;
var exit = 0;

function initializePage(){
	document.getElementById("sendMessage").addEventListener("click", postMessage, true);
	if(document.getElementById("mCount")){
		messageCount = Number(document.getElementById("mCount").innerText);
	}
	timeoutID = window.setTimeout(poller, timeout);
}

function postMessage(){
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}


	var messageText = document.getElementById("messageText").value;
	var user = document.getElementById("username").innerText;
	var userMessage = [user, messageText];

	httpRequest.onreadystatechange = function() { handlePost(httpRequest, userMessage) };
	
	httpRequest.open("POST", "/send_message");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var chatroom = document.getElementById("chatName").innerText;
	reqMessage = "message=" + messageText + "&chatroom=" + chatroom;
	httpRequest.send(reqMessage);
}


function handlePost(httpRequest, userMessage) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			addRow(userMessage);
			messageCount = messageCount + 1;
			clearField();
		} 
		else {
			alert("There was a problem with this request");
		}
	}
}

function poller() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("GET", "/messages");

	httpRequest.send();
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE && exit == 0) {
		if (httpRequest.status === 200) {
			if (Number(JSON.parse(httpRequest.responseText)) == 1){
				exit = 1;
				alert("SORRY! This chatroom no longer exists");
				var newPage = document.getElementById("ifDeleted").innerText; 
				window.location.replace(newPage);
			}
			var allMessages = JSON.parse(httpRequest.responseText);
			var allCount = allMessages.length;
			var newMessages = allCount - messageCount;
			if (newMessages > 0){
				for (var i = messageCount; i < allCount; i++){
					addRow(allMessages[i]);
				}
				messageCount = messageCount + newMessages;
			}
			timeoutID = window.setTimeout(poller, timeout);
			
		} else {
			alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}


function addRow(row) {
	var tableRef = document.getElementById("messageBoard");
	var newRow  = tableRef.insertRow();

	var newCell, newText;
	for (var i = 0; i < row.length; i++) {
		newCell  = newRow.insertCell();
		newText  = document.createTextNode(row[i]);
		newCell.appendChild(newText);
	}
}

function clearField(){
	document.getElementById("messageText").value = "";
}


window.addEventListener("load", initializePage, true);
