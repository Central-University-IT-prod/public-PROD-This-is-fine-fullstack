'use strict'

function toggleForm(el) {
    let parent = el.parentNode;
    let form = document.forms.registration;
    let isValid = true;
    parent.querySelectorAll('input').forEach(item => {
        if (!item.checkValidity()) isValid = false;
    });
    if (form.password1.value != form.password2.value) {
        document.getElementsByName('password2')[0].classList.add('form__input--invalid');
        isValid = false;
    }
    if (isValid) {
        el.parentNode.classList.remove('opened');
        el.parentNode.nextElementSibling.classList.add('opened');
    }
}

let form = document.forms.registration;
form.addEventListener('submit', function (e) {
    this.querySelectorAll('input[name="interest"]').forEach(item => {
        if (item.checked) document.getElementsByName('interests')[0].value += ', ' + item.value;
    });
    this.querySelectorAll('input[name="stack-item"]').forEach(item => {
        if (item.checked) document.getElementsByName('stack')[0].value += ', ' + item.value;
    });
});

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

let image;
async function getAIAvatar() {
    let name = form.login.value;
    let response = await fetch(`/auth/generate_avatar/${name}`);
    let link = await response.text();
    form.avatarai.value = link;
}