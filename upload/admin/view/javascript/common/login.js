let form = document.getElementById('form-login');
let alertBox = document.getElementById('alert');

function showAlert(type, message) {
    if (!alertBox || !message) {
        return;
    }

    alertBox.insertAdjacentHTML('afterbegin', '<div class="alert alert-' + type + ' alert-dismissible"><i class="fa-solid fa-circle-' + (type === 'danger' ? 'exclamation' : 'check') + '"></i> ' + message + ' <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>');
}

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        alertBox.innerHTML = '';

        let button = form.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Logging in...';
        }

        try {
            let response = await fetch(form.getAttribute('action').replaceAll('&amp;', '&'), {
                method: 'POST',
                body: new FormData(form),
                credentials: 'same-origin'
            });

            let json = await response.json();

            if (json.redirect) {
                window.location = json.redirect;
                return;
            }

            if (typeof json.error === 'string') {
                showAlert('danger', json.error);
            } else if (json.error && json.error.warning) {
                showAlert('danger', json.error.warning);
            }

            if (json.success) {
                showAlert('success', json.success);
            }
        } catch (error) {
            showAlert('danger', 'Login request failed. Please refresh and try again.');
            console.error(error);
        } finally {
            if (button) {
                button.disabled = false;
                button.innerHTML = button.dataset.originalText || 'Login';
            }
        }
    });
}
