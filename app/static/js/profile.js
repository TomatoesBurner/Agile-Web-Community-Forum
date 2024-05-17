// Global function to toggle tabs
function toggleTab(selectedTab) {
    console.log("Toggling tab to:", selectedTab);
    $('.tab').css('background-color', '#d8e6f8'); // Reset all tabs to default color
    if (selectedTab === 'Posts') {
        $('#postsTab').css('background-color', '#adc8f2'); // Highlight the Posts tab
        $('#postsContent').show(); // Show posts content
        $('#commentsContent').hide(); // Hide comments content
    } else if (selectedTab === 'Comments') {
        $('#commentsTab').css('background-color', '#adc8f2'); // Highlight the Comments tab
        $('#postsContent').hide(); // Hide posts content
        $('#commentsContent').show(); // Show comments content
    }
}

$(document).ready(function () {
    $('#usernameForm').on('submit', function (e) {
        e.preventDefault();  // 防止表单的默认提交行为
        var newUsername = $('#username').val().trim();  // 获取并清理输入值
        if (newUsername) {
            console.log("Updating username to:", newUsername);
            this.submit();  // 使用原生的 submit 方法提交表单
        } else {
            alert('Username cannot be empty.');  // 弹出警告如果用户名为空
        }
    });

    $('#avatarChange').click(function () {
        $('#avatarInput').click(); // 触发隐藏的文件输入
    });

    $('#avatarInput').change(function () {
        var file = this.files[0];
        console.log("New avatar selected:", file.name);
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#avatarChange').attr('src', e.target.result); // 预览新的头像
            };
            reader.readAsDataURL(file);
            // 提交表单以更新数据库中的头像
            $('#avatarForm').submit();
        }
    });

    $('#avatarForm').on('submit', function (e) {
        // 设置一个小的延迟以确保预览可以显示
        setTimeout(function () {
            location.reload(); // 提交表单后刷新页面
        }, 1000); // 1秒的延迟时间
    });

    // 鼠标悬停在头像上时更改光标样式
    $('#avatarChange').hover(
        function () {
            $(this).css('cursor', 'pointer');
        },
        function () {
            $(this).css('cursor', 'default');
        }
    );

    // 当点击删除图标时，设置和显示模态框
    $('body').on('click', '.delete-icon', function () {
        var id = $(this).data('id');
        var type = $(this).data('type');
        confirmDelete(id, type);
    });

    // 鼠标悬停时显示删除图标
    $('.post-item, .comment-item').hover(
        function () {
            $(this).find('.delete-container .delete-icon').css('display', 'block');
        },
        function () {
            $(this).find('.delete-container .delete-icon').css('display', 'none');
        }
    );

    const postsTab = document.getElementById('postsTab');
    const commentsTab = document.getElementById('commentsTab');
    const postsContent = document.getElementById('postsContent');
    const commentsContent = document.getElementById('commentsContent');

    function activateTab(tab) {
        if (tab === 'Posts') {
            postsTab.classList.add('active');
            commentsTab.classList.remove('active');
            postsContent.style.display = 'block';
            commentsContent.style.display = 'none';
            postsTab.style.backgroundColor = '#adc8f2';
            commentsTab.style.backgroundColor = '#d8e6f8';
        } else {
            commentsTab.classList.add('active');
            postsTab.classList.remove('active');
            commentsContent.style.display = 'block';
            postsContent.style.display = 'none';
            commentsTab.style.backgroundColor = '#adc8f2';
            postsTab.style.backgroundColor = '#d8e6f8';
        }
    }

    const urlParams = new URLSearchParams(window.location.search);
    const currentTab = urlParams.get('tab') || 'Posts';
    activateTab(currentTab);

    postsTab.addEventListener('click', function () {
        activateTab('Posts');
        window.history.replaceState(null, '', '?tab=Posts');
    });

    commentsTab.addEventListener('click', function () {
        activateTab('Comments');
        window.history.replaceState(null, '', '?tab=Comments');
    });
});

function confirmDelete(id, type) {
    const deleteForm = document.getElementById('deleteForm');
    const deleteId = document.getElementById('deleteId');
    const deleteType = document.getElementById('deleteType');
    const currentTab = new URLSearchParams(window.location.search).get('tab') || 'Posts';

    deleteId.value = id;
    deleteType.value = type;

    $('#deleteConfirmationModal').modal('show');

    deleteForm.action = `/${type}s/delete/${id}?tab=${currentTab}`;
}
