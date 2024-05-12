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

function highlightIcon(selectedElement) {
    // 存储活动项
    localStorage.setItem('activeNavItem', $(selectedElement).attr('href'));

    updateActiveNav();
}

function updateActiveNav() {
    // 重置所有导航链接的透明度和样式
    $('.nav-link').css({
        'opacity': '0.5' // 半透明效果
    }).children('i').css({
        'color': '' // 保持原有颜色
    });

    // 获取存储的活动项并应用活动样式
    var activeNavItem = localStorage.getItem('activeNavItem');
    if (activeNavItem) {
        $('a.nav-link[href="' + activeNavItem + '"]').css({
            'opacity': '1' // 完全不透明
        });
    }
}

$(document).ready(function() {
    $('.nav-link').click(function() {
        highlightIcon(this); // 调用highlightIcon函数
    });

    // 页面加载时更新活动状态
    updateActiveNav();
});
