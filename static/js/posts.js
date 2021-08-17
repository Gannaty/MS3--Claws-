
// Code adapted from https://github.com/seanyoung247/Plum/blob/main/static/js/recipes.js
// Shows the current selected image in the image box
  
$( "#post_image_url" ).on('change', function(event) {
    $( '#post_header_image' ).prop("src", result.info.secure_url)

  });

 
  var myWidget = cloudinary.createUploadWidget({
    cloudName: 'dwlkkut0a', 
    uploadPreset: 'p1skzthc'}, (error, result) => { 

      if (!error && result && result.event === "success") { 

        console.log('Done! Here is the image info: ', result.info);
        
        
        $( '#post_header_image' ).prop("src", result.info.secure_url);
        $( '#post_image_url' ).val(result.info.secure_url);

      }
    }
  );
    
    document.getElementById("upload_widget").addEventListener("click", function(){
        myWidget.open();
      }, false);

      
  
// Function for image preview
function imagePreview() {
  $("div").removeClass("hide");
  $("#post_header_image").val();
  $('.image-preview').attr('src', result.info.secure_url);
}; 