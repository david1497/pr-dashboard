document.addEventListener('DOMContentLoaded', function () {
    let touchstartX = 0;
    let touchendX = 0;

    function handleGesture() {
        const swipeEventDiv = document.getElementById('swipe-event');
        if (touchendX < touchstartX) {
            console.log('Swiped left');
            swipeEventDiv.innerHTML = 'left'; // Update hidden div
        }
        if (touchendX > touchstartX) {
            console.log('Swiped right');
            swipeEventDiv.innerHTML = 'right'; // Update hidden div
        }
    }

    document.addEventListener('touchstart', function (event) {
        touchstartX = event.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', function (event) {
        touchendX = event.changedTouches[0].screenX;
        handleGesture();
    });
});