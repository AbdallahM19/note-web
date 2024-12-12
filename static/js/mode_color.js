document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.getElementById("darkModeToggle");

    console.log(darkModeToggle);

    darkModeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
    });
});
