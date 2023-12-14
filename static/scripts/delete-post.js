// Initiate a delete request when the delete button is clicked
$(document).ready(function () {
    $('#delete-post').click(function (e) {
        e.preventDefault();

        const postId = $(this).data('post-id');

        if (confirm('Are you sure you want to delete this post?')) {
            // Create a form
            var form = $('<form>', {
                'method': 'POST',
                'action': '/posts/delete/' + postId
            });

            // Append the form to the body and submit it
            form.appendTo('body').submit();
        }
    });
});