$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
});


//Character limit for post captions
$(document).ready(function() {
    $('textarea#textarea2').characterCounter();
  });


// Function for image preview
function imagePreview() {
  $("div").removeClass("hide");
  var url = $("#image").val();
  $('.image-preview').attr('src',url);
}
