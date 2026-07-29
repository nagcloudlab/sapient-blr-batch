console.log("Hello, World! This is a simple web UI example.");

// ------------------
// using DOM-api
// ------------------

const greetBtn=document.querySelector("#greet-btn");
const cardBody=document.querySelector(".card-body");

greetBtn.addEventListener("click",e=>{
    const hour=new Date().getHours();
    let greeting;
    if(hour<12){
        greeting="Good Morning!";
    }else if(hour<18){
        greeting="Good Afternoon!";
    }else{
        greeting="Good Evening!";
    }
    cardBody.innerHTML=`<h3>${greeting}</h3>`;
});