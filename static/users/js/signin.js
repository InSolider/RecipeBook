const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const mycontainer = document.querySelector(".my-container");

sign_up_btn.addEventListener("click", () => {
  mycontainer.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  mycontainer.classList.remove("sign-up-mode");
});

// Bootstrap toast notifications

var toastElements = document.querySelectorAll('.toast');
for (var i = 0; i < toastElements.length; i++) {
  new bootstrap.Toast(toastElements[i]).show();
}