document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle sidebar toggle on mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-open');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && document.querySelector(targetId)) {
                e.preventDefault();
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            const closeBtn = message.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });

    // Career goal progress update
    const progressInputs = document.querySelectorAll('.progress-input');
    if (progressInputs) {
        progressInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const goalId = this.dataset.goalId;
                const progressValue = this.value;
                const progressBar = document.querySelector(`#progress-bar-${goalId}`);
                
                if (progressBar) {
                    progressBar.style.width = `${progressValue}%`;
                    progressBar.setAttribute('aria-valuenow', progressValue);
                    document.querySelector(`#progress-text-${goalId}`).textContent = `${progressValue}%`;
                }
                
                // In a real app, we'd send an AJAX request to update the progress
                console.log(`Updating goal ${goalId} progress to ${progressValue}%`);
                // Example AJAX request (commented out)
                /*
                fetch('/update-goal-progress', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        goal_id: goalId,
                        progress: progressValue
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
                */
            });
        });
    }

    // Search functionality
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');
            
            items.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Filter courses
    const filterForm = document.querySelector('#filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select, input');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Countdown timer for timed tests
    const timerElement = document.querySelector('#test-timer');
    if (timerElement && timerElement.dataset.timeLimit) {
        const timeLimit = parseInt(timerElement.dataset.timeLimit) * 60; // Convert to seconds
        let timeRemaining = timeLimit;
        
        const timer = setInterval(function() {
            timeRemaining--;
            
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            
            timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            // Add hidden input to track time taken
            const timeTakenInput = document.querySelector('#time-taken');
            if (timeTakenInput) {
                timeTakenInput.value = timeLimit - timeRemaining;
            }
            
            if (timeRemaining <= 0) {
                clearInterval(timer);
                // Auto-submit the test
                const testForm = document.querySelector('#test-form');
                if (testForm) {
                    testForm.submit();
                }
            }
        }, 1000);
    }

    // Chat message scroll to bottom
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
