// display reply area when reply button is clicked
function reply() {
    const reply_button = document.getElementsByClassName("reply-button");
    const reply_area = document.getElementsByClassName("reply-area");
    for (let i = 0; i < reply_button.length; i++) {
        reply_button[i].addEventListener("click", function () {
            console.log("Button clicked:", i);
            console.log("Reply area:", reply_area[i]);
            reply_area[i].classList.toggle("d-none");
        });
    }
}
reply();