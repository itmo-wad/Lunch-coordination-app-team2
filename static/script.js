document.addEventListener('DOMContentLoaded', function() {
    // Обработка голосования
    const voteButtons = document.querySelectorAll('.vote-button');
    if (voteButtons.length > 0) {
        voteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const optionId = this.getAttribute('data-option-id');
                const voteType = this.getAttribute('data-vote-type');
                const buttonsForOption = document.querySelectorAll(`.vote-button[data-option-id="${optionId}"]`);

                // Сначала удаляем все активные классы для этой опции
                buttonsForOption.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Добавляем активный класс нажатой кнопке
                this.classList.add('active');

                // Устанавливаем значение в скрытое поле
                document.getElementById(`vote_${optionId}`).value = voteType;
            });
        });
    }

    // Удаление опции при создании опроса
    const removeOptionButtons = document.querySelectorAll('.remove-option');
    if (removeOptionButtons.length > 0) {
        removeOptionButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Вы уверены, что хотите удалить эту опцию?')) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = this.getAttribute('data-url');

                    // Добавляем CSRF токен
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

    // Копирование ссылки на опрос в буфер обмена
    const copyLinkButton = document.getElementById('copy-poll-link');
    if (copyLinkButton) {
        copyLinkButton.addEventListener('click', function(e) {
            e.preventDefault();
            const pollLink = this.getAttribute('data-link');

            // Создаем временный input для копирования текста
            const tempInput = document.createElement('input');
            tempInput.value = pollLink;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);

            // Изменяем текст кнопки на время
            const originalText = this.textContent;
            this.textContent = 'Ссылка скопирована!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    }

    // Обратный отсчет для дедлайна
    const deadlineElement = document.getElementById('poll-deadline');
    if (deadlineElement) {
        const deadlineTime = new Date(deadlineElement.getAttribute('data-deadline')).getTime();

        // Обновляем каждую секунду
        const countdown = setInterval(function() {
            const now = new Date().getTime();
            const distance = deadlineTime - now;

            // Расчет времени
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Отображаем результат
            deadlineElement.textContent = `${hours}ч ${minutes}м ${seconds}с`;

            // Если время истекло
            if (distance < 0) {
                clearInterval(countdown);
                deadlineElement.textContent = "Голосование завершено";

                // Перезагружаем страницу, чтобы показать результаты
                location.reload();
            }
        }, 1000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Обработка завершения опроса
    const finishPollButton = document.querySelector('.btn-finish-poll');
    if (finishPollButton) {
        finishPollButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Вы уверены, что хотите завершить опрос? После этого голосование будет остановлено.')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = this.getAttribute('data-url');

                // Добавляем CSRF токен
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

    // Обработка голосования
    const voteButtons = document.querySelectorAll('.vote-button');
    if (voteButtons.length > 0) {
        voteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const optionId = this.getAttribute('data-option-id');
                const voteType = this.getAttribute('data-vote-type');
                const buttonsForOption = document.querySelectorAll(`.vote-button[data-option-id="${optionId}"]`);

                // Сначала удаляем все активные классы для этой опции
                buttonsForOption.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Добавляем активный класс нажатой кнопке
                this.classList.add('active');

                // Устанавливаем значение в скрытое поле
                document.getElementById(`vote_${optionId}`).value = voteType;
            });
        });
    }

    // Удаление опции при создании опроса
    const removeOptionButtons = document.querySelectorAll('.remove-option');
    if (removeOptionButtons.length > 0) {
        removeOptionButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Вы уверены, что хотите удалить эту опцию?')) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = this.getAttribute('data-url');

                    // Добавляем CSRF токен
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

    // Копирование ссылки на опрос в буфер обмена
    const copyLinkButton = document.getElementById('copy-poll-link');
    if (copyLinkButton) {
        copyLinkButton.addEventListener('click', function(e) {
            e.preventDefault();
            const pollLink = this.getAttribute('data-link');

            // Создаем временный input для копирования текста
            const tempInput = document.createElement('input');
            tempInput.value = pollLink;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);

            // Изменяем текст кнопки на время
            const originalText = this.textContent;
            this.textContent = 'Ссылка скопирована!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    }

    // Обратный отсчет для дедлайна
    const deadlineElement = document.getElementById('poll-deadline');
    if (deadlineElement) {
        const deadlineTime = new Date(deadlineElement.getAttribute('data-deadline')).getTime();

        // Обновляем каждую секунду
        const countdown = setInterval(function() {
            const now = new Date().getTime();
            const distance = deadlineTime - now;

            // Расчет времени
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Отображаем результат
            deadlineElement.textContent = `${hours}ч ${minutes}м ${seconds}с`;

            // Если время истекло
            if (distance < 0) {
                clearInterval(countdown);
                deadlineElement.textContent = "Голосование завершено";

                // Перезагружаем страницу, чтобы показать результаты
                location.reload();
            }
        }, 1000);
    }
});