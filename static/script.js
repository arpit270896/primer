var ctx = null;
var canvas = document.getElementById("tmpImage");
var localMediaStream = null;
var video = document.querySelector('video');

function snapshot() {        
	if (localMediaStream) {
		ctx.drawImage(video, 0, 0);
		console.log($("#MainContainer > img").length);
		if($("#MainContainer > img").length >= 10) {
			console.log($("#MainContainer").find('img:first-child'));
			$("#MainContainer img:first-child").remove();
		}
		var img = document.createElement('img');
		// "image/webp" works in Chrome 18. In other browsers, this will fall back to image/png.
		img.src = canvas.toDataURL('image/jpg');
		$("#MainContainer").prepend(img);

		data = {
			'image_data': img.src
		}

		$.ajax({
			type: 'POST',
			url: "/convert",
			data: data,
			success: function(resultData) {
				img.src = "/static/gifs/" + resultData + ".gif";
				$(img).on('click', function() {
					window.open('/gifs?hash='+resultData, '_blank')
				})
			}
		});
	}
}

function hasGetUserMedia() {
	// Note: Opera builds are unprefixed.
	return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
			navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function onFailSoHard(){

}

function start() {
	if (hasGetUserMedia()) {
		if (navigator.webkitGetUserMedia)
			navigator.getUserMedia = navigator.webkitGetUserMedia;
		//var getUserMedia = navigator.webkitGetUserMedia || navigator.getUserMedia;

		
		//var gumOptions = { video: true, toString: function () { return 'video'; } };    
		if (navigator.getUserMedia) {
			navigator.getUserMedia({ video: true }, function (stream) {
				if (navigator.webkitGetUserMedia) {
					video.src = window.webkitURL.createObjectURL(stream);
				} else {
					video.src = stream; // Opera
				}
				localMediaStream = stream;
			}, onFailSoHard);
		} else {
			video.src = 'somevideo.webm'; // fallback.
		}
	}
}

function stop() {
	video = document.getElementById('sourcevid');
	video.src = "";
}

function ResizeCanvas() {
	canvas.height = video.videoHeight;
	canvas.width = video.videoWidth;
}

$(document).ready(function () {
	start();
	$('.button').button();
	ctx = canvas.getContext('2d');
});
