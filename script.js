const signin_btn=document.querySelector("#signin_btn");
const signup_btn=document.querySelector("#signup_btn");
const signin_btn2=document.querySelector("#signin_btn2");
const signup_btn2=document.querySelector("#signup_btn2");
const container=document.querySelector(".container");

signup_btn.addEventListener("click", () =>{
    container.classList.add("sign-up-mode");
});
signin_btn.addEventListener("click", () =>{
    container.classList.remove("sign-up-mode");
});
signup_btn2.addEventListener("click", () =>{
    container.classList.add("sign-up-mode2");
});
signin_btn2.addEventListener("click", () =>{
    container.classList.remove("sign-up-mode2");
});
