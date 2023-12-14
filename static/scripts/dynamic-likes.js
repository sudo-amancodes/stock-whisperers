
// Like Button Ajax
$(document).ready(function () {
    $('.like-button').click(function (event) {
        event.stopPropagation();
        var postId = $(this).data('post-id');
        var userId = $(this).data('user-id');

        $.ajax({
            type: 'POST',
            url: '/posts/like',
            data: { post_id: postId, user_id: userId },
            success: function (data) {
                console.log('Like added successfully');
            },
            error: function (error) {
                console.error('Error adding like:', error);
            }
        });
    });

    $('.like-comment').click(function (event) {
        event.stopPropagation();
        var commentId = $(this).data('comment-id');
        var userId = $(this).data('user-id');

        $.ajax({
            type: 'POST',
            url: '/posts/like_comment',
            data: { comment_id: commentId, user_id: userId },
            success: function (data) {
                console.log('Comment added successfully');
            },
            error: function (error) {
                console.error('Error adding Comment:', error);
            }
        });
    });
});

// Like Button Dynamic UI
function liked_or_not() {
    const like_button = document.getElementsByClassName("like-button");
    const like_count = document.getElementsByClassName("like-count");
    for (let i = 0; i < like_button.length; i++) {
        like_button[i].addEventListener("click", function () {
            if (like_button[i].classList.contains("liked")) {
                like_count[i].innerHTML = parseInt(like_count[i].innerHTML) - 1;
            } else {
                like_count[i].innerHTML = parseInt(like_count[i].innerHTML) + 1;
            }
            like_button[i].firstChild.classList.toggle("fa-regular");
            like_button[i].firstChild.classList.toggle("fa-solid");
            like_button[i].classList.toggle("liked");
        });
    }
}
liked_or_not();

function liked_comment_or_not() {
    const like_button = document.getElementsByClassName("like-comment");
    const like_count = document.getElementsByClassName("like-comment-count");
    console.log(like_button.length);
    for (let i = 0; i < like_button.length; i++) {
        like_button[i].addEventListener("click", function () {
            if (like_button[i].classList.contains("liked")) {
                like_count[i].innerHTML = parseInt(like_count[i].innerHTML) - 1;
            } else {
                like_count[i].innerHTML = parseInt(like_count[i].innerHTML) + 1;
            }
            like_button[i].firstChild.classList.toggle("fa-regular");
            like_button[i].firstChild.classList.toggle("fa-solid");
            like_button[i].classList.toggle("liked");
        });
    }
}
liked_comment_or_not();