function validateForm() {
    // Validate image file if selected
    var imageUpload = document.getElementById('image_upload');
    if (imageUpload.files.length > 0) {
        var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
        if (!allowedExtensions.exec(imageUpload.value)) {
            alert('Invalid file type. Please upload a valid image file (jpg, jpeg, png, gif).');
            return false;
        }
    }
    return true;
}