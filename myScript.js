var onFireTime = 10;
var getUrl = "http://localhost:4180/getUpdated";
function OnLoad(){
    Main();

}

async function Main(){

    while(true){
       await GetUpdated();
    }

}


async function GetUpdated(){

   var backendResponse = await GetFromBackend();
   $(".photosContainer").html("");
       backendResponse.users.forEach(element => {
        var onFire = false;
        if ((Date.now() - element.last) > onFireTime && element.ir == true){
            onFire = true;
        }
        addUserById(element.id, element.ir, onFire);
    });


}

function addUserById(id, inRoom, onFire){
    
    var modeClass = "";
    var classForOnFire = "";
    var extraClass = `style="bottom: 26rem;"`;
    if (inRoom){
        modeClass = "photoContainer-ImInside";
    }
    if(onFire){
        classForOnFire = `<img src="Photos/fire.gif" class="ImOnFireBaby" alt="">`;
        extraClass = "";
        
    }
    switch (id) {
        case 1:
            var myName = `<div class="maName" ${extraClass}>Eli</div>`;

            $(".photosContainer").append(`<div class="photoContainer ${modeClass}" > <img src="Photos/eli.jpg" alt="">  ${classForOnFire} ${myName}</div>`);
            break;
        case 2:
            var myName = `<div class="maName" ${extraClass}>Tal</div>`;
            $(".photosContainer").append(`<div class="photoContainer ${modeClass}" >  <img src="Photos/tal.jpg" alt="">  ${classForOnFire} ${myName} </div>`);
            break;
        case 3:
            var myName = `<div class="maName" ${extraClass}>Yoni</div>`;
            $(".photosContainer").append(`<div class="photoContainer ${modeClass}" >  <img src="Photos/yonatan.jpg" alt="">  ${classForOnFire} ${myName}</div>`);
            break;
        case 4:
            var myName = `<p class="maName">Daniel</p>`;
            $(".photosContainer").append(`<div class="photoContainer ${modeClass}" >  <img src="Photos/pam.jpg" alt="">  ${classForOnFire} ${myName}</div>`);
            break;            
    
        default:
            break;
    }

}

async function GetFromBackend(){

    await timeout(1000);
    postResult = await Promise.resolve($.get(getUrl));
    return postResult;
    return ({"users":[{"id": 1, "ir": true, "last": 1653393503}, {"id": 2, "ir": false, "last": 1653393504}, {"id": 3, "ir": true, "last": 1653393504}]});

}

function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}






