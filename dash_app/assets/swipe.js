// swipe.js
// this function is created to send the js browser logs to the flask server logs
console.log('File active. Should work. New');
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

    const matrixLayout = [
        ['overview', 'costs'],
        ['labour', 'materials'],
        ['suppliers', 'suppliers']
        // Add more pages as per your layout
    ];
    

    var hammertime = new Hammer(document.body, {
        recognizers: [
            [Hammer.Swipe, { direction: Hammer.DIRECTION_ALL }]
        ]
    });
    console.log('Hammer.js initialized on document body with all directions');

    hammertime.on('swipeleft', function(ev) {
        console.log('Swipe left detected');
        sendLogToServer('Swipe left detected');
        handleSwipe('left');
    });

    hammertime.on('swiperight', function(ev) {
        console.log('Swipe right detected');
        sendLogToServer('Swipe right detected');
        handleSwipe('right');
    });

    hammertime.on('swipeup', function(ev) {
        console.log('Swipe up detected');
        sendLogToServer('Swipe up detected');
        handleSwipe('up');
    });

    hammertime.on('swipedown', function(ev) {
        console.log('Swipe down detected');
        sendLogToServer('Swipe down detected');
        handleSwipe('down');
    });


    function handleSwipe(direction) {
        var currentPath = window.location.pathname;
        var newPath = getNewPath(currentPath, direction);

        sendLogToServer('Current path: \t', currentPath);
        sendLogToServer('Current path: \t', newPath);
        console.log('\n\nCurrent path: \t', currentPath);
        console.log('\n\nCurrent path: \t', newPath);
        
        if (newPath) {
            console.log('Navigating to new path:', newPath);
            window.location.pathname = newPath;
        }
    }

    function getNewPath(currentPath, direction) {
        // Find current position in the matrix
        var currentPosition = findPosition(currentPath);
        if (!currentPosition) return null;  // Current page not found in matrix
        
        var column = currentPosition.column;
        var row = currentPosition.row;
        
        // Determine new position based on swipe direction
        var newColumn, newRow;
        
        switch (direction) {
            case 'left':
                newColumn = column + 1;
                newRow = row;
                break;
            case 'right':
                newColumn = column - 1;
                newRow = row;
                break;
            case 'up':
                newColumn = column;
                newRow = row + 1;
                break;
            case 'down':
                newColumn = column;
                newRow = row - 1;
                break;
            default:
                return null;  // Invalid direction
        }
        
        // Check bounds of the matrix
        if (newColumn < 0 || newColumn >= matrixLayout[0].length || newRow < 0 || newRow >= matrixLayout.length) {
            return null;  // Out of bounds
        }
        
        // Get new page path
        var newPage = matrixLayout[newRow][newColumn];

        sendLogToServer('NewPage: \t', newPage);
        console.log('\n\nNewPage: \t', newPage);
        return `${newPage}/`;  // Assuming pages are routes in your Flask app
    }

    function findPosition(currentPath) {
        // Loop through matrix to find current page position
        for (var row = 0; row < matrixLayout.length; row++) {
            for (var column = 0; column < matrixLayout[row].length; column++) {
                if (matrixLayout[row][column] === currentPath.replace('/', '')) {
                    return { column: column, row: row };
                }
            }
        }
        return null;  // Current page not found in matrix
    }
});