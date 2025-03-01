document.addEventListener('DOMContentLoaded', function() {
    // Poll voting handling
    const voteButtons = document.querySelectorAll('.vote-button');
    if (voteButtons.length > 0) {
        voteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const optionId = this.getAttribute('data-option-id');
                const voteType = this.getAttribute('data-vote-type');
                const buttonsForOption = document.querySelectorAll(`.vote-button[data-option-id="${optionId}"]`);

                // First remove all active classes for this option
                buttonsForOption.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Add active class to clicked button
                this.classList.add('active');

                // Set value in hidden field
                document.getElementById(`vote_${optionId}`).value = voteType;
            });
        });
    }

    // Remove option when creating poll
    const removeOptionButtons = document.querySelectorAll('.remove-option');
    if (removeOptionButtons.length > 0) {
        removeOptionButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Are you sure you want to remove this option?')) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = this.getAttribute('data-url');

                    // Add CSRF token
                    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                    const csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.name = 'csrf_token';
                    csrfInput.value = csrfToken;
                    form.appendChild(csrfInput);

                    document.body.appendChild(form);
                    form.submit();
                }
            });
        });
    }

    // Copy poll link to clipboard
    const copyLinkButton = document.getElementById('copy-poll-link');
    if (copyLinkButton) {
        copyLinkButton.addEventListener('click', function(e) {
            e.preventDefault();
            const pollLink = this.getAttribute('data-link');

            // Create temporary input for copying text
            const tempInput = document.createElement('input');
            tempInput.value = pollLink;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);

            // Change button text temporarily
            const originalText = this.textContent;
            this.textContent = 'Link copied!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    }

    // Countdown for deadline
    const deadlineElement = document.getElementById('poll-deadline');
    if (deadlineElement) {
        const deadlineTime = new Date(deadlineElement.getAttribute('data-deadline')).getTime();

        // Update every second
        const countdown = setInterval(function() {
            const now = new Date().getTime();
            const distance = deadlineTime - now;

            // Calculate time
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Display result
            deadlineElement.textContent = `${hours}h ${minutes}m ${seconds}s`;

            // If time has expired
            if (distance < 0) {
                clearInterval(countdown);
                deadlineElement.textContent = "Voting completed";

                // Reload page to show results
                location.reload();
            }
        }, 1000);
    }

    // Poll finishing handling
    const finishPollButton = document.querySelector('.btn-finish-poll');
    if (finishPollButton) {
        finishPollButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to finish the poll? Voting will be stopped.')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = this.getAttribute('data-url');

                // Add CSRF token
                const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                document.body.appendChild(form);
                form.submit();
            }
        });
    }
});