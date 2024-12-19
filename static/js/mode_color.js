export function darkModeDy() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const modeIcon = document.getElementById("modeIcon");

  const panels_container = document.querySelector(".panels-container");
  const left_panel = panels_container.querySelector(".left-panel");
  const left_img_in_panel = left_panel.querySelector(".images");
  const right_panel = panels_container.querySelector(".right-panel");
  const right_img_in_panel = right_panel.querySelector(".images");

  console.log('-------------------------');
  console.log(container);
  console.log(panels_container);
  console.log(left_panel);
  console.log(right_panel);
  console.log('-------------------------');

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

    modeIcon.alt = isDarkMode ? "Light Mode" : "Dark Mode";
    modeIcon.src = isDarkMode
      ? "../static/images/dark-mode.png"
      : "../static/images/sun-icon.png";
    left_img_in_panel.src = isDarkMode
      ? "../static/images/social-media.gif"
      : "../static/images/sign-in.jpeg";
    right_img_in_panel.src = isDarkMode
      ? "../static/images/social-media.gif"
      : "../static/images/sign-up.jpeg";

    localStorage.setItem("theme", isDarkMode ? "light" : "dark");
  });
}
