document.onreadystatechange = () => {
    if (document.readyState === 'complete') {
        document.getElementById("container-loader").classList.add('hide');

        setTimeout(function () {
            document.getElementById("container-loader").style.display = 'none';
        }, 1000);
    }
};
