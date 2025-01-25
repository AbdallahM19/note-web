document.addEventListener("DOMContentLoaded", () => {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const modeIcon = document.getElementById("modeIcon");

  const panels_container = document.querySelector(".panels-container");
  const left_panel = panels_container ? panels_container.querySelector(".left-panel") : null;
  const left_img_in_panel = left_panel ? left_panel.querySelector(".images") : null;
  const right_panel = panels_container ? panels_container.querySelector(".right-panel") : null;
  const right_img_in_panel = right_panel ? right_panel.querySelector(".images") : null;

  const savedMode = localStorage.getItem("theme");
  if (savedMode === "dark") {
    document.body.classList.add("dark-mode");
    modeIcon.src = "/static/images/sun-icon.png";
    modeIcon.alt = "Light Mode";

    if (left_img_in_panel) left_img_in_panel.src = "/static/images/user.png";
    if (right_img_in_panel) right_img_in_panel.src = "/static/images/user.png";
  } else {
    document.body.classList.remove("dark-mode");
    modeIcon.src = "/static/images/dark-mode.png";
    modeIcon.alt = "Dark Mode";

    if (left_img_in_panel) left_img_in_panel.src = "/static/images/user-2.png";
    if (right_img_in_panel) right_img_in_panel.src = "/static/images/user-2.png";
  }

  darkModeToggle.addEventListener("click", () => {
    const isDarkMode = document.body.classList.contains("dark-mode");

    document.body.classList.toggle("dark-mode");

    modeIcon.alt = isDarkMode ? "Light Mode" : "Dark Mode";
    modeIcon.src = isDarkMode
      ? "/static/images/dark-mode.png"
      : "/static/images/sun-icon.png";
    if (left_img_in_panel) left_img_in_panel.src = isDarkMode
      ? "/static/images/user-2.png"
      : "/static/images/user.png";
    if (left_img_in_panel) right_img_in_panel.src = isDarkMode
      ? "/static/images/user-2.png"
      : "/static/images/user.png";

    localStorage.setItem("theme", isDarkMode ? "light" : "dark");
  });
});
