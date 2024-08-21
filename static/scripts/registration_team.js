'use strict'

function toggleForm(el) {
    let parent = el.parentNode;
    let isValid = true;
    parent.querySelectorAll('input').forEach(item => {
        if (!item.checkValidity()) isValid = false;
    });
    if (isValid) {
        el.parentNode.classList.remove('opened');
        el.parentNode.nextElementSibling.classList.add('opened');
    }
}

document.querySelectorAll('input').forEach(el => {
    el.addEventListener('invalid', function () {
        this.classList.add('form__input--invalid');
    });
    el.addEventListener('input', function () {
        if (el.checkValidity() && el.classList.contains('form__input--invalid')) {
            el.classList.remove('form__input--invalid');
        } else if (!el.checkValidity() && !el.classList.contains('form__input--invalid')) {
            el.classList.add('form__input--invalid');
        }
    })
});

function transportCheckbox(el) {
    if (el.checked) {
        let copy = el.parentNode.cloneNode(true);
        el.parentNode.parentNode.previousElementSibling.prepend(copy);
        el.parentNode.remove();
    } else {
        let copy = el.parentNode.cloneNode(true);
        el.parentNode.parentNode.nextElementSibling.prepend(copy);
        el.parentNode.remove();
    }
}


let form = document.forms.create;
form.addEventListener('submit', function (e) {
    this.querySelectorAll('input[name="track"]').forEach(item => {
        if (item.checked) document.getElementsByName('tracks')[0].value += ', ' + item.value;
    });
});
