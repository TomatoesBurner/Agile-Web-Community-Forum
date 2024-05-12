document.addEventListener('DOMContentLoaded', function () {
    var dom = document.getElementsByClassName("word")[0]; // Assuming there's only one element with class "word"
    var num = 0;
    var intervalId = setInterval(function(){
        num++;
        if(num > 100){
            num = 0;
        }
        dom.innerHTML = num;
    }, 100);

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

    // 高亮选中的导航图标
    function highlightIcon(selectedElement) {
        $('.nav-link').css('opacity', '0.5').children('i').removeClass('active-icon');
        $(selectedElement).css('opacity', '1').children('i').addClass('active-icon');
    }

    // 绑定点击事件到所有导航链接
    $('.nav-link').click(function () {
        highlightIcon(this);
    });
});
