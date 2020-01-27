// Функция для ищменения яркости изображения

var range=document.querySelectorAll('#playground-value-input');
function changeHandler(event){
  var px=(this.value==0)?'':'%';
  document.getElementById('playground-property').style.filter='brightness('+this.value+'%)';
  document.getElementById('playground-code-value').innerText=this.value+px;
}
Array.prototype.forEach.call(range,function(range){
  range.addEventListener('input',changeHandler);
});

function sizePic() {
    size = document.getElementById("size").value;
    img = document.getElementById("pic");
    img.width = 60 + 20*size;
  }

// Функция для input для ссылок

function multi(){
  var srcvid=document.getElementById('srcvid').value
  if (srcvid == "") {
    srcvid="https://www.youtube.com/embed/L_LUpnjgPso"
  }
  document.getElementById('playground-property').src=srcvid;
}
