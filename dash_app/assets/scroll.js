console.log('File Scroll active. Should work. New');
function sendLogToServer(message) {
    fetch('/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => console.log('Log sent to server:', data))
    .catch((error) => console.error('Error sending log to server:', error));
}
// --------------------------------------------------------------------------------
sendLogToServer('\n\nChecking if the logging works');

document.addEventListener('DOMContentLoaded', function() {

    let lastScrollY = window.scrollY;
    let lastScrollX = window.scrollX;
    let atBottom = false;
    let atTop = false;
    let atLeft = false;
    let atRight = false;

    function checkVerticalScroll() {
        let currentScrollY = window.scrollY;
        atBottom = (window.innerHeight + window.scrollY) >= document.body.offsetHeight;
        atTop = window.scrollY === 0;
        lastScrollY = currentScrollY;
    }

    function checkHorizontalScroll() {
        let currentScrollX = window.scrollX;
        atLeft = window.scrollX === 0;
        atRight = (window.innerWidth + window.scrollX) >= document.body.scrollWidth;
        lastScrollX = currentScrollX;
    }

    window.addEventListener('scroll', function() {
        checkVerticalScroll();
        checkHorizontalScroll();
    });

    window.addEventListener('wheel', function(event) {
        let direction = '';

        if (event.deltaX > 0) {
            direction = 'right';
        } else if (event.deltaX < 0) {
            direction = 'left';
        } else if (event.deltaY > 0) {
            direction = 'down';
        } else if (event.deltaY < 0) {
            direction = 'up';
        }

        let currentPath = window.location.pathname;
        console.log('Vertical Scroll ', direction, ' detected in ', currentPath);
        sendLogToServer('Vertical Scroll ', direction, ' detected in ', currentPath);
        let newPath = getNewPath(currentPath, direction);
        console.log('Will redirect to ', newPath);
        sendLogToServer('Will redirect to ', newPath);

        if (direction === 'down' && atBottom && newPath) {
            window.location.pathname = newPath;
        } else if (direction === 'up' && atTop && newPath) {
            window.location.pathname = newPath;
        } else if (direction === 'right' && atRight && newPath) {
            window.location.pathname = newPath;
        } else if (direction === 'left' && atLeft && newPath) {
            window.location.pathname = newPath;
        }
    });


    function getNewPath(currentPath, direction) {

        const navigationMap = {
            '/overview': {down: '/labour', right: '/costs'},
            '/labour': {up: '/overview', down: '/suppliers', left: '/materials'},
            '/suppliers': {up: '/labour', left: '/reports'},
            '/costs': {down: '/materials', left: '/overview'},
            '/materials': {up: '/costs', down: '/reports', right: '/labour'},
            '/reports': {up: '/materials', left: '/suppliers'}
        };

        if (navigationMap[currentPath] && navigationMap[currentPath][direction]) {
            return navigationMap[currentPath][direction];
        }
        return null;
    }
});