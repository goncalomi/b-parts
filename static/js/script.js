function populateForm() {
    let inputCount = document.getElementById('license-plates').querySelectorAll('.plate-form').length;
    let addButon = document.getElementById('add-license-plate');
    inputCount === 0 && addButon.click();
}

function updateTotalForms() {
    let licensePlatesDiv = document.getElementById('license-plates').querySelectorAll('div').length;
    document.getElementById('id_plates-TOTAL_FORMS').value = licensePlatesDiv;
}

function removePlate(event) {
    event.currentTarget.parentElement.remove()
    updateTotalForms();
}

function addPlates() {
    let licensePlatesDiv = document.getElementById('license-plates');
    let divsCount = licensePlatesDiv.querySelectorAll('div').length
    let emptyFormHtml = document.getElementById('empty-form').innerHTML.replace(/__prefix__/g, divsCount);
    document.getElementById('license-plates').insertAdjacentHTML('beforeend', emptyFormHtml);
    document.getElementById('id_plates-TOTAL_FORMS').value = divsCount+1;
}

document.getElementById('add-customer-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let isValid = true;

    // Validate email
    const emailInput = document.getElementById('id_email');
    if (emailInput) {
        if (!emailInput.value.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/)) {
            emailInput.classList.add('error');
            document.getElementById('email-error').style.display = 'block';
            isValid = false;
        } else {
            emailInput.classList.remove('error');
            document.getElementById('email-error').style.display = 'none';
        }
    }

    // Validate license plates
    const plateForms = document.getElementById('license-plates').querySelectorAll('div');
    plateForms.forEach(form => {
        const plateInput = form.querySelector('[name$="plate_number"]');
        if (!plateInput.value.match(/^(?:[0-9]{2}[A-Z]{2}[0-9]{2}|[0-9]{2}-[0-9]{2}-[A-Z]{2})$/)) {
            plateInput.classList.add('error');
            form.querySelector('.plate-error').style.display = 'block';
            isValid = false;
        } else {
            plateInput.classList.remove('error');
            form.querySelector('.plate-error').style.display = 'none';
        }
    });

    isValid && event.currentTarget.submit()
});

document.getElementById('license-plates').addEventListener('input', function(event) {
    if (event.target.tagName === 'INPUT' && event.target.type === 'text') {
        event.target.value = event.target.value.toUpperCase();
    }
});

window.onload = () => {
    populateForm();
}