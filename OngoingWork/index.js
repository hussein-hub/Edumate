var canvas = document.getElementById("draw");
canvas.width = 500;
canvas.height = 500;

var ctx = canvas.getContext("2d");

// draw an image inside the canvas 
var img = new Image();
img.src = "https://thumbs.dreamstime.com/b/gateway-india-mumbai-gateway-india-arch-monument-built-th-century-mumbai-india-monument-was-138091856.jpg";
img.onload = function() {
    ctx.drawImage(img, 0, 0);
}

var element = document.getElementById("draw");
var rect = element.getBoundingClientRect();
console.log(rect.top, rect.right, rect.bottom, rect.left);

var c = 0;

// resize canvas when window is resized
// function resize() {
//   ctx.canvas.width = window.innerWidth;
//   ctx.canvas.height = window.innerHeight;
// }

// initialize position as 0,0
var pos = { x: 0, y: 0, a: 0, b: 0 };
var actualPos = { x: 0, y: 0, a: 0, b: 0 };

// new position from mouse events
function setPosition(e) {
  if (c == 0) {
  	pos.x = e.clientX - 12 - rect.left + 8;
  	pos.y = e.clientY - 30 - rect.top + 29 ;
  } else {
  	pos.a = e.clientX - 12 - rect.left + 8;
  	pos.b = e.clientY - 30 - rect.top + 29;
  }
}

function draw(e) {
  if (e.buttons !== 1) return; // if mouse is not clicked, do not go further

  else if (c == 1) {
    var color = document.getElementById("hex").value;

    ctx.beginPath(); // begin the drawing path

    ctx.lineWidth = 1.5; // width of line
    ctx.lineCap = "round"; // rounded end cap
    ctx.strokeStyle = color; // hex color of line
    setPosition(e);
    ctx.rect(pos.x, pos.y, (pos.a-pos.x), (pos.b-pos.y));
    console.log(pos, actualPos, "inside draw");
    actualPos.x = pos.x;
    actualPos.y = pos.y;
    actualPos.a = pos.a;
    actualPos.b = pos.b;
    ctx.stroke(); // draw it!
    c = 0;
  }
  else {
  	setPosition(e);
  	c++;
  }
}

// clear canvas when clicked
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var img = new Image();
    img.src = "https://thumbs.dreamstime.com/b/gateway-india-mumbai-gateway-india-arch-monument-built-th-century-mumbai-india-monument-was-138091856.jpg";
    img.onload = function() {
        ctx.drawImage(img, 10, 10);
    }
}

// crop the image when clicked
function cropImage() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // ctx.drawImage(img, pos.x, pos.y, (pos.a-pos.x), (pos.b-pos.y), 0, 0, (pos.a-pos.x), (pos.b-pos.y));
    console.log(pos, actualPos, "inside crop");
    ctx.drawImage(img, actualPos.x, actualPos.y, (actualPos.a-actualPos.x), (actualPos.b-actualPos.y), 0, 0, (actualPos.a-actualPos.x), (actualPos.b-actualPos.y));

}



// add window event listener to trigger when window is resized
// window.addEventListener("resize", resize);

// add event listeners to trigger on different mouse events
document.addEventListener("mousedown", draw);
document.addEventListener("mouseup", setPosition);
document.addEventListener("click", setPosition);