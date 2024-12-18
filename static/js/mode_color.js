export function darkModeDy() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const modeIcon = document.getElementById("modeIcon");

  const savedMode = localStorage.getItem("theme");
  if (savedMode === "dark") {
    document.body.classList.add("dark-mode");
    modeIcon.src = "../static/images/sun-icon.png";
    modeIcon.alt = "Light Mode";
  } else {
    document.body.classList.remove("dark-mode");
    modeIcon.src = "../static/images/dark-mode.png";
    modeIcon.alt = "Dark Mode";
  }

  darkModeToggle.addEventListener("click", () => {
    const isDarkMode = document.body.classList.contains("dark-mode");

    document.body.classList.toggle("dark-mode");

    modeIcon.src = isDarkMode
      ? "../static/images/dark-mode.png"
      : "../static/images/sun-icon.png";
    modeIcon.alt = isDarkMode ? "Light Mode" : "Dark Mode";

    localStorage.setItem("theme", isDarkMode ? "light" : "dark");
  });
}
