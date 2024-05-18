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
        e.preventDefault();  // Prevent default form submission
        var newUsername = $('#username').val().trim();  // Get and clean input value
        if (newUsername) {
            console.log("Updating username to:", newUsername);
            this.submit();  // Submit the form using the native submit method
        } else {
            alert('Username cannot be empty.');  // Show alert if username is empty
        }
    });

    $('#avatarChange').click(function () {
        $('#avatarInput').click(); // Trigger hidden file input
    });

    $('#avatarInput').change(function () {
        var file = this.files[0];
        console.log("New avatar selected:", file.name);
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#avatarChange').attr('src', e.target.result); // Preview new avatar
            };
            reader.readAsDataURL(file);
            // Submit the form to update the avatar in the database
            $('#avatarForm').submit();
        }
    });

    $('#avatarForm').on('submit', function (e) {
        // Set a small delay to ensure the preview can be displayed
        setTimeout(function () {
            location.reload(); // Refresh the page after submitting the form
        }, 1000); // 1 second delay
    });

    // Change cursor style when hovering over the avatar
    $('#avatarChange').hover(
        function () {
            $(this).css('cursor', 'pointer');
        },
        function () {
            $(this).css('cursor', 'default');
        }
    );

    // Set up and show modal when delete icon is clicked
    $('body').on('click', '.delete-icon', function () {
        var id = $(this).data('id');
        var type = $(this).data('type');
        confirmDelete(id, type);
    });

    // Show delete icon when hovering over post or comment item
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