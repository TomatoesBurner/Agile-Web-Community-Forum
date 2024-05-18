document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form.accept-form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            const action = this.action;
            fetch(action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrf_token'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const heartIcon = this.querySelector('.iconright');
                    heartIcon.src = heart2IconUrl;
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

