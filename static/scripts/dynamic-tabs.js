$(document).ready(function () {

    // Reload the page when visibility changes
    document.addEventListener("visibilitychange", function () {
        if (document.visibilityState === "visible") {
            var scrollPosition = window.scrollY;

            // Reload the page
            location.reload();

            // Scroll back to the previous position after the reload
            window.scrollTo(0, scrollPosition);
        }
    });
});