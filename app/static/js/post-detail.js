// post-detail.js
$(document).ready(function () {
    var maxLength = 200;

    // 限制输入长度并实时显示字符数
    $('#comment-textarea').on('input', function () {
        var currentLength = $(this).val().length;
        if (currentLength > maxLength) {
            $(this).val($(this).val().substring(0, maxLength));
        }
        $('#comment-counter').text("Max characters: " + currentLength + "/" + maxLength);
    });

    // 处理粘贴事件
    $('#comment-textarea').on('paste', function (e) {
        var paste = (e.originalEvent || e).clipboardData.getData('text');
        var currentLength = $(this).val().length;
        if (currentLength + paste.length > maxLength) {
            e.preventDefault();
            var textToPaste = paste.substring(0, maxLength - currentLength);
            document.execCommand('insertText', false, textToPaste);
        }
    });
});
