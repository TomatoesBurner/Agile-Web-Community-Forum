$(document).ready(function () {
    // 限制输入长度并实时显示字符数 for ideaInput
    $('#ideaInput').on('input', function () {
        var maxLength = 200;
        var currentLength = $(this).val().length;
        if (currentLength > maxLength) {
            $(this).val($(this).val().substring(0, maxLength));
        }
        $('#charCount').text("Max characters: " + currentLength + "/200");
    });

    // 限制输入长度并实时显示字符数 for contentInput
    $('#contentInput').on('input', function () {
        var maxLength = 1000;
        var currentLength = $(this).val().length;
        if (currentLength > maxLength) {
            $(this).val($(this).val().substring(0, maxLength));
        }
        $('#charCountContent').text("Max characters: " + currentLength + "/1000");
    });
    $(document).ready(function () {
        $('.icon-box').click(function () {
            var type = $(this).data('type');  // 使用 .data() 访问 data-* 属性
            $('#sectionTypeInput').val(type);
            $('.icon-box').removeClass('active');
            $(this).addClass('active');
        });

    });


});