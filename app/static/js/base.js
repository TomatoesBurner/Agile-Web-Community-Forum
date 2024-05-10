let dom = document.getElementsByClassName("word");
let num = 0;
setInterval(function(){
    num++;
    if(num>100){
        num=0;
    }
    dom.innerHTML=num
},100)

document.addEventListener('DOMContentLoaded', function () {
    var avatar = document.getElementById('avatarImage');
    var dropdownMenu = document.getElementById('dropdownMenu');

    // 确保初始隐藏下拉菜单
    dropdownMenu.style.display = 'none';

    avatar.onclick = function () {
      if (dropdownMenu.style.display === 'none') {
        dropdownMenu.style.display = 'block';
      } else {
        dropdownMenu.style.display = 'none';
      }
    };

    // 关闭下拉菜单如果点击头像之外的地方
    window.onclick = function (event) {
      if (!event.target.matches('.avatar')) {
        if (dropdownMenu.style.display === 'block') {
          dropdownMenu.style.display = 'none';
        }
      }
    };
  });