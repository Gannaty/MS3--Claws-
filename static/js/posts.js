
// Code adapted from https://github.com/seanyoung247/Plum/blob/main/static/js/recipes.js
// Shows the current selected image in the image box
  


// Stops Cloudinary image upload button from sending form before image is uploaded. 
$( ".image_upload_btn" ).click(function(event) {
  event.preventDefault();

});
    
// Cloudinary image upload    
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

  
      
  
// Function for add posts image preview 
$( ".image_upload_btn" ).on('click', function() {
    $("img").removeClass("hide");
    $('.image-preview').attr('src', result.info.secure_url);
});