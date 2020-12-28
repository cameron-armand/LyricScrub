$(document).ready(function(){


  $(".submit").click(function () {
      setTimeout(function () { disableButton(); }, 0);
  });

  function disableButton() {
      $("#submit").prop('disabled', true);
      $("#submitsong").prop('disabled', true);
      $(".form-control").prop('disabled', true);
      $("#sp1").attr("class","spinner-border spinner-border-sm");
      $(".error").addClass("d-none");
  }

});


function toggleMode() {
  var checkBox = document.getElementById("toggle-mode");
  var pagestyle = document.getElementById("pagestyle");
  if (checkBox.checked == true){
  	pagestyle.setAttribute('href','../static/dark.css');
  } else {
    pagestyle.setAttribute('href','../static/style.css');
  }
}

function autoFill(artist,album) {
   $('.artist').val(artist);
   $('.album').val(album);
}
