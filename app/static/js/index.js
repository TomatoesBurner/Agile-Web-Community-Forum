let dom = document.getElementsByClassName("word");
let num = 0;
setInterval(function(){
    num++;
    if(num>100){
        num=0;
    }
    dom.innerHTML=num
},100)

// 高亮选中的导航图标
function highlightIcon(selectedElement) {
    $('.nav-link').css('opacity', '0.5').children('i').removeClass('active-icon');
    $(selectedElement).css('opacity', '1').children('i').addClass('active-icon');
}

// 绑定点击事件到所有导航链接
$('.nav-link').click(function () {
    highlightIcon(this);
});