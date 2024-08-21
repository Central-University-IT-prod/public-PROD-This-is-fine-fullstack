let form = document.forms.filter;
form.addEventListener('submit', function (e) {
    this.querySelectorAll('input[name="stack-item"]').forEach(item => {
        if (item.checked) document.getElementsByName('stack')[0].value += ', ' + item.value;
    });
});

document.querySelector('.filter').addEventListener("click", closeOnBackDropClick);

function closeOnBackDropClick({ currentTarget, target }) {
    const dialogElement = currentTarget;
    const isClickedOnBackDrop = target === dialogElement;
    if (isClickedOnBackDrop) {
        dialogElement.close();
    }
}


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


function inviteUser(id, el) {
    el.setAttribute('disabled', '');
    el.firstChild.setAttribute('src', '/static/imgs/checkbox.svg');
    el.firstChild.style.transform = 'none';
    fetch(`/teams/add-to-team/${id}`);
}   
