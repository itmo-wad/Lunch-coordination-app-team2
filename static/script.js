document.addEventListener('DOMContentLoaded', function () {

    const voteButtons = document.querySelectorAll('.vote-button');
    if (voteButtons.length > 0) {
        voteButtons.forEach(button => {
            button.addEventListener('click', function () {
                const optionId = this.getAttribute('data-option-id');
                const voteType = this.getAttribute('data-vote-type');
                const buttonsForOption = document.querySelectorAll(`.vote-button[data-option-id="${optionId}"]`);


                buttonsForOption.forEach(btn => {
                    btn.classList.remove('active');
                });


                this.classList.add('active');


                document.getElementById(`vote_${optionId}`).value = voteType;
            });
        });
    }


    const removeOptionButtons = document.querySelectorAll('.remove-option');
    if (removeOptionButtons.length > 0) {
        removeOptionButtons.forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();
                if (confirm('Are you sure you want to remove this option?')) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = this.getAttribute('data-url');


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


    const copyLinkButton = document.getElementById('copy-poll-link');
    if (copyLinkButton) {
        copyLinkButton.addEventListener('click', function (e) {
            e.preventDefault();
            const pollLink = this.getAttribute('data-link');


            const tempInput = document.createElement('input');
            tempInput.value = pollLink;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);


            const originalText = this.textContent;
            this.textContent = 'Link copied!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    }


    const deadlineElement = document.getElementById('poll-deadline');
    if (deadlineElement) {
        const deadlineTime = new Date(deadlineElement.getAttribute('data-deadline')).getTime();


        const countdown = setInterval(function () {
            const now = new Date().getTime();
            const distance = deadlineTime - now;


            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);


            deadlineElement.textContent = `${hours}h ${minutes}m ${seconds}s`;


            if (distance < 0) {
                clearInterval(countdown);
                deadlineElement.textContent = "Voting completed";


                location.reload();
            }
        }, 1000);
    }


    const finishPollButton = document.querySelector('.btn-finish-poll');
    if (finishPollButton) {
        finishPollButton.addEventListener('click', function (e) {
            e.preventDefault();
            if (confirm('Are you sure you want to finish the poll? Voting will be stopped.')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = this.getAttribute('data-url');


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