url = "http://192.168.62.191:8000/profiles/1";
//TODO make a correct url by backend
async function getProgileData(){
    try{
        const response = await fetch(url);
        const data = await response.json();
        console.log('Recieved data: ', data);
        return data
    }
    catch(e){
        console.error(e)
    }
}

async function drawProfile(){
    data = await getProgileData();

    let login = document.querySelector(".profile__login");
    let grade = document.querySelector(".profile__grade");
    let fio = document.querySelector(".profile__fio");

    let city = document.querySelector(".city__text");
    let interests = document.querySelector(".interests__text");
    let track = document.querySelector(".track__text");
    let stack = document.querySelector(".stack__text");
    let contacts = document.querySelector(".telegram__text");
    let bio = document.querySelector(".profile__description");


    login.innerHTML = data.username + " " + data.grade.toString();
    fio.innerHTML = data.fio;
    console.log("profile title successfully recieved")

    if(data.city != ""){
        city.innerHTML = data.city;
    }

    if(data.interests != ""){
        interests.innerHTML = data.interests;
    }
    track.innerHTML = data.track;

    if(data.stack != ""){
        stack.innerHTML = data.stack;
    }
    
    contacts.innerHTML = data.telegram_handle;
    contacts.href = "https://t.me/" + data.telegram_handle;
    
    if(data.bio != ""){
        bio.innerHTML = data.bio;
    }
    
    console.log("Profile successfully recieved");
}


drawProfile().then(console.log("Rendered"))

