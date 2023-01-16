function chat(type) {

    // RECUPERATION DU MESSAGE DE L'UTILISATEUR //

    const message = document.getElementById('textAreaExample');


    // PARTIE POUR AFFICHER LE MESSAGE DE L'UTILISATEUR //

    const bulle = document.getElementById('general_chat');

    let div1 = document.createElement('div');
    div1.setAttribute('class','d-flex flex-row justify-content-end mb-4');
    bulle.appendChild(div1);

    let div2 = document.createElement('div');
    div2.setAttribute('class','p-3 me-3 border');
    div2.style.borderRadius = '15px';
    div2.style.backgroundColor = '#fbfbfb';
    div1.appendChild(div2);

    let p = document.createElement('p');
    p.setAttribute('class','small mb-0');
    p.textContent = type+" : "+message.value;
    div2.appendChild(p);

    let img = document.createElement('img');
    img.setAttribute(
  'src',
  "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp",
    );
    img.style.width = "45px";
    img.style.height ="100%";
    div1.appendChild(img);


    // NETTOYE LE TEXTAREA ET BLOQUE LES BOUTONS //
    const msg = message.value;
    document.getElementById('textAreaExample').value = "";
    document.getElementById("speak").disabled = true;
    document.getElementById("do").disabled = true;
    document.getElementById("tell").disabled = true;


    // AFFICHAGE DU GIF DE CHARGEMENT //

    const bulleA = document.getElementById('general_chat');

    let div1A = document.createElement('div');
    div1A.setAttribute('class','d-flex flex-row justify-content-start mb-4');
    bulleA.appendChild(div1A);


    let imgA = document.createElement('img');
    imgA.setAttribute(
  'src',
  "static/image/anastasia-robot-bard.jpg",
    );
    imgA.style.width = "45px";
    imgA.style.height ="100%";
    imgA.style.borderRadius = "50%";
    div1A.appendChild(imgA);


    let div2A = document.createElement('div');
    div2A.setAttribute('class','p-3 ms-3 border');
    div2A.style.borderRadius = '5px';
    div2A.style.marginLeft = '15px';
    div2A.style.backgroundColor = 'rgba(57, 192, 237,.2)';
    div1A.appendChild(div2A);

    let wait = document.createElement('img');
    wait.setAttribute(
  'src',
  "static/image/waiting-texting.gif",
    );
    wait.style.width = "45px";
    wait.style.height ="100%";
    div2A.appendChild(wait);

    // ENVOIE DU MESSAGE A L'IA //
    const dict_values = {type, msg}
    const s = JSON.stringify(dict_values);
    $.ajax({
        url:"/AI",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s)
    }).done(function (AImsg){

        // ENLEVER LE GIF ET AFFICHER lA REPONSE DE L'IA //

        wait.remove();

        let pA = document.createElement('p');
        pA.setAttribute('class','small mb-0');
        pA.textContent = AImsg['AImsg'];
        div2A.appendChild(pA);

    });



    // DEBLOQUE LES BOUTONS //


    document.getElementById("speak").disabled = false;
    document.getElementById("do").disabled = false;
    document.getElementById("tell").disabled = false;


}



