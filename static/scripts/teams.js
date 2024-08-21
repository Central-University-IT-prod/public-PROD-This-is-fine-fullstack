'use strict'

function joinTeam(team, el) {
    el.setAttribute('disabled', '');
    el.firstChild.setAttribute('src', '/static/imgs/checkbox.svg');
    el.firstChild.style.transform = 'none';
    fetch(`/teams/join-to-team/${team}`);
}   
