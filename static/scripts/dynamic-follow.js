// Follow Button AJAX - dynamic-follow.js
$(document).ready(function () {
    $('#follow-button').click(function (event) {
        event.stopPropagation();
        event.preventDefault();

        const postCreatorUserId = $(this).data('post-creator-id');

        $.ajax({
            type: 'POST',
            url: '/follow/' + postCreatorUserId,
            success: function (data) {
                console.log('Followed successfully');
            },
            error: function (error) {
                console.error('Error following:', error);
            }
        });
    });
});

// Follow Button Dynamic UI
function follow_or_not() {
    const follow_button = document.getElementById("follow-button");
    follow_button.addEventListener("click", function () {
        if (follow_button.classList.contains("followed")) {
            follow_button.innerHTML = "Follow";
        } else {
            follow_button.innerHTML = "Following";
        }
        follow_button.classList.toggle("followed");
    });
}
follow_or_not();