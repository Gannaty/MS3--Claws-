
// Code adapted from https://github.com/seanyoung247/Plum/blob/main/static/js/recipes.js
// Shows the current selected image in the image box
$( "#post_image_url" ).on('change', function(event) {
    $( '#post_header_image' ).prop("src", $( this ).val());

  });
  

var myWidget = cloudinary.createUploadWidget({
  cloudName: 'dwlkkut0a', 
  uploadPreset: 'p1skzthc'}, (error, result) => { 

    $( '#post_header_image' ).prop("src", result[0].secure_url);
    $( '#post_image_url' ).val(result[0].secure_url);

    if (!error && result && result.event === "success") { 
      console.log('Done! Here is the image info: ', result.info); 
    }
  }
)
  
  document.getElementById("upload_widget").addEventListener("click", function(){
      myWidget.open();
    }, false);

  

  