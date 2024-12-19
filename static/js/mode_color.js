document.addEventListener("DOMContentLoaded", () => {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const modeIcon = document.getElementById("modeIcon");

  const panels_container = document.querySelector(".panels-container");
  const left_panel = panels_container.querySelector(".left-panel");
  const left_img_in_panel = left_panel.querySelector(".images");
  const right_panel = panels_container.querySelector(".right-panel");
  const right_img_in_panel = right_panel.querySelector(".images");

  const savedMode = localStorage.getItem("theme");
  if (savedMode === "dark") {
    document.body.classList.add("dark-mode");
    modeIcon.src = "../static/images/sun-icon.png";
    modeIcon.alt = "Light Mode";

    left_img_in_panel.src = "../static/images/user.png";
    right_img_in_panel.src = "../static/images/user.png";
  } else {
    document.body.classList.remove("dark-mode");
    modeIcon.src = "../static/images/dark-mode.png";
    modeIcon.alt = "Dark Mode";

    left_img_in_panel.src = "../static/images/user-2.png";
    right_img_in_panel.src = "../static/images/user-2.png";
  }

  darkModeToggle.addEventListener("click", () => {
    const isDarkMode = document.body.classList.contains("dark-mode");

    document.body.classList.toggle("dark-mode");

    modeIcon.alt = isDarkMode ? "Light Mode" : "Dark Mode";
    modeIcon.src = isDarkMode
      ? "../static/images/dark-mode.png"
      : "../static/images/sun-icon.png";
    left_img_in_panel.src = isDarkMode
      ? "../static/images/user-2.png"
      : "../static/images/user.png";
    right_img_in_panel.src = isDarkMode
      ? "../static/images/user-2.png"
      : "../static/images/user.png";

    localStorage.setItem("theme", isDarkMode ? "light" : "dark");
  });
});
