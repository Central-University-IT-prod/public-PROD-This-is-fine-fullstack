function loadLists(l1, l2) {
    let checkboxList = l1;
    checkboxList = checkboxList.concat(l2);
    console.log(checkboxList);
    checkboxList.forEach((item) => {
        document.querySelector(`input[value="${item}"]`).checked = true;
        transportCheckbox(document.querySelector(`input[value="${item}"]`));
    });
}