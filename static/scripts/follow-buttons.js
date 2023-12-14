const followers_button = document.querySelector('.followers');
followers_button.addEventListener('click', Popup)
const close_button = document.querySelector('.close');
close_button.addEventListener('click', Popup)
let popup = document.getElementById('popup');
function Popup() {
popup.classList.toggle("open-popup");
}

const following_button = document.querySelector('.following');
following_button.addEventListener('click', Popup2)
const close_button2 = document.querySelector('.close2');
close_button2.addEventListener('click', Popup2)
let popup2 = document.getElementById('popup2');
function Popup2() {
popup2.classList.toggle("open-popup");
}