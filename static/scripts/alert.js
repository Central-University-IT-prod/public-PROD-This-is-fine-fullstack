'use strict'

async function applyAlert(user, team) {
    await fetch('/teams/accept-apply/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        body: JSON.stringify({'user': user, 'team': team}) 
    })
    window.location.reload();
}

async function rejectAlert(user, team) {
    await fetch('/teams/decline-apply/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        body: JSON.stringify({'user': user, 'team': team}) 
    });
    window.location.reload();

}


async function applyInvite(user, team) {
    await fetch('/teams/accept-invite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        body: JSON.stringify({'user': user, 'team': team}) 
    });
    window.location.reload();

}

async function rejectInvite(user, team) {
    await fetch('/teams/decline-invite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        body: JSON.stringify({'user': user, 'team': team}) 
    });
    window.location.reload();

}