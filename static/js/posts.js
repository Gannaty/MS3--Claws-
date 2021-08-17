
// Code adapted from https://github.com/seanyoung247/Plum/blob/main/static/js/recipes.js
// Shows the current selected image in the image box
$( "#post_image_url" ).on('change', function(event) {
    $( '#post_header_image' ).prop("src", $( this ).val());

  });
  
  // cloudinary callback. Sets upload image url input
  function imageUploaded(error, result) {
    $( '#post_header_image' ).prop("src", result[0].secure_url);
    $( '#post_image_url' ).val(result[0].secure_url);
    
  }
  
  // Shows the cloudinary image upload widget
  $( "#image_upload_btn" ).click(function(event) {
    event.preventDefault();
  
    cloudinary.openUploadWidget(
      {
        cloud_name: 'dwlkkut0a',
        upload_preset: 'p1skzthc'
      },
      imageUploaded);
  });