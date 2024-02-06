var pinching = false;
var touch_x = 0;
var slide_x = 0;

var d0 = 1;
var d1 = 1;
var dx = 0;
var scale = 1;
//document.getElementById("body").onscroll = function(){
//  var $scrollLeft = this.scrollLeft;
//  document.querySelector("#commands").style.left = $scrollLeft;
//};

document.addEventListener("touchstart", function(e){
//	touch_x = Math.floor(e.originalEvent.touches[0].pageX);
	touch_x = Math.floor(e.touches[0].pageX);
});

document.addEventListener("touchmove", function(e){
  if (e.touches.length == 2) {
    if (!pinching) {
      pinching = true;
      scale = e.originalEvent.scale;
      d0 = Math.sqrt(
        Math.pow(e.touches[1].screenX - e.touches[0].screenX, 2) +
        Math.pow(e.touches[1].screenY - e.touches[0].screenY, 2)
      );
      dx = e.touches[0].screenX;
    } else {
      d1 = Math.sqrt(
        Math.pow(e.touches[1].screenX - e.touches[0].screenX, 2) +
        Math.pow(e.touches[1].screenY - e.touches[0].screenY, 2)
      );
//      document.querySelector("#commands").style.zoom = d1 / d0;
      document.querySelector("#commands").style.width = window.innerWidth;
//      document.querySelector("#commands").style.margin-left = dx;
    }
  }
//  else {
	slide_x = Math.floor(e.touches[0].pageX) - touch_x;
	slide_x = Math.sqrt(Math.pow(slide_x,2));
//  }
});

document.addEventListener("touchend", function(e) {
  pinching = false;
  document.querySelector("#commands").style.width = window.innerWidth;
  document.querySelector("#commands").style.size = window.innerWidth / 7;
//  document.querySelector("#commands").style.left = slide_x;
});
