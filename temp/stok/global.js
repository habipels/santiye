/* Global JS Functions for BiadaGO ERP */

// Modal functionality
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Form validation example
function validateForm(formId) {
    var form = document.getElementById(formId);
    var inputs = form.querySelectorAll('input, select, textarea');
    var valid = true;

    inputs.forEach(function(input) {
        if (input.value === '') {
            input.style.border = '1px solid red';
            valid = false;
        } else {
            input.style.border = '';
        }
    });

    return valid;
}

// Toast Notification
function showToast(message) {
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(function() {
        toast.style.opacity = 0;
    }, 3000);

    setTimeout(function() {
        toast.remove();
    }, 3500);
}
