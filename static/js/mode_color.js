document.addEventListener("DOMContentLoaded", () => {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const modeIcon = document.getElementById("modeIcon");

  darkModeToggle.addEventListener("click", () => {
    const isDarkMode = document.body.classList.contains("dark-mode");

    document.body.classList.toggle("dark-mode");

    modeIcon.src = isDarkMode
      ? "../static/images/dark-mode.png"
      : "../static/images/sun-icon.png";
    modeIcon.alt = isDarkMode ? "Light Mode" : "Dark Mode";
  });
});
