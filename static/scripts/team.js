'use strict'

function deleteTeam(n) {
    fetch(`/teams/delete-team/${n}`).then(() => {
        document.querySelector('.confirmation').close();
        document.location.reload()
    });
}

function leaveTeam(n) {
    fetch(`/teams/leave-from-team/${n}`).then(() => {
        document.querySelector('.confirmation').close();
   	document.location.reload()
    });
    document.location.reload()
}

document.querySelector('.confirmation').addEventListener("click", closeOnBackDropClick);

function closeOnBackDropClick({ currentTarget, target }) {
    const dialogElement = currentTarget;
    const isClickedOnBackDrop = target === dialogElement;
    if (isClickedOnBackDrop) {
        dialogElement.close();
    }
}
