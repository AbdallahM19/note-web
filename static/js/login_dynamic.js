document.addEventListener("DOMContentLoaded", () => {
  const signin_btn = document.querySelector("#signin_btn");
  const signup_btn = document.querySelector("#signup_btn");
  const signin_btn2 = document.querySelector("#signin_btn2");
  const signup_btn2 = document.querySelector("#signup_btn2");
  const container = document.querySelector(".container");

  signup_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
    container.classList.add("signup-mode2");
  });

  signin_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
    container.classList.remove("signup-mode2");
  });

  signup_btn2.addEventListener("click", (e) => {
    e.preventDefault();
    container.classList.add("sign-up-mode");
    container.classList.add("signup-mode2");
  });

  signin_btn2.addEventListener("click", (e) => {
    e.preventDefault();
    container.classList.remove("signup-mode2");
    container.classList.remove("sign-up-mode");
  });
});
