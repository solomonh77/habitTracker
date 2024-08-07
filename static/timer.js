let countdown; // Declare countdown variable globally to access it in both functions
let remainingTime; // Declare remainingTime variable to keep track of remaining seconds

function startTimer() {
    const inputElement = document.getElementById('timeInput');

    if (!remainingTime) { // If remainingTime is not set, get input time in minutes
        let time = parseInt(inputElement.value) * 60; // Convert minutes to seconds

        if (isNaN(time) || time <= 0) {
            alert('Please enter a valid number of minutes.');
            return;
        }

        remainingTime = time;
    }
    //updating the time that is displayed
    updateDisplay(remainingTime);

    clearInterval(countdown); // Clear any existing interval before starting a new one
    // checks to see if there is any time remaining 
    countdown = setInterval(() => {
        remainingTime -= 1;
        updateDisplay(remainingTime);

        if (remainingTime <= 0) {
            clearInterval(countdown);
            alert('Time\'s up!');
        }
    }, 1000);
}

//stop the timer
function stopTimer() {
    clearInterval(countdown); // Clear the interval to stop the timer
}
// reset the timer
function resetPage() {
    clearInterval(countdown);
    remainingTime = 0;
    updateDisplay(remainingTime);
}
//update the clock display
function updateDisplay(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    document.getElementById('countdownDisplay').textContent =
        `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}