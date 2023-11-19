var imageFile = null;
document.getElementById('upload-btn').addEventListener('change', function (event) {
	const file = event.target.files[0];
	if (file) {
		imageFile = file;
		const reader = new FileReader();
		reader.onload = function (e) {
			const imagePreview = document.getElementById('image-preview');
			imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" width="200">`;
			imagePreview.style.display = 'block';
			document.getElementById('predict-btn').disabled = false;
		};
		reader.readAsDataURL(file);
	}
});

document.getElementById('predict-btn').addEventListener('click', function () {

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(prediction => {
        const predictionText = document.getElementById('predictionText');
        predictionText.innerText = `Prediction: ${prediction.result}`;
        predictionText.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });

});

function uploadImage() {
    var formData = new FormData();
    var file = $('#uploadInput')[0].files[0];
    formData.append('image', file);

    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#result').html(response); // Show response from Flask backend
        }
    });
}
