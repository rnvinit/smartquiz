document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add a timer to the quiz page
    if (document.querySelector('.quiz-form')) {
        let timeLeft = 300; // 5 minutes
        const timerDisplay = document.createElement('div');
        timerDisplay.classList.add('text-center', 'mb-4');
        timerDisplay.innerHTML = `Time left: <span id="time-left">5:00</span>`;
        document.querySelector('.quiz-form').prepend(timerDisplay);

        const timerInterval = setInterval(function() {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            document.getElementById('time-left').textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                alert('Time\'s up! Submitting your quiz.');
                document.querySelector('.quiz-form').submit();
            }
        }, 1000);
    }

    // Add confetti effect to the result page
    if (document.querySelector('.result-page')) {
        const score = parseInt(document.querySelector('.score').textContent);
        if (score >= 4) { // Trigger confetti for high scores
            const confettiSettings = { target: 'confetti-canvas', max: 80, size: 2, animate: true };
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            setTimeout(() => confetti.clear(), 3000); // Stop after 3 seconds
        }
    }
});