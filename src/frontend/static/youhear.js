class InactivityManager {
    constructor() {
        this.inactivityTime = 60 * 1000; // 5 минут
        this.countdownTime = 10 * 1000; // 10 секунд
        this.inactivityTimer = null;
        this.countdownTimer = null;
        this.modal = document.getElementById('inactiveModal');
        this.countdownElement = document.getElementById('countdown');
        this.stayActiveBtn = document.getElementById('stayActive');
        
        this.init();
    }

    init() {
        // Слушатели событий активности
        this.setupEventListeners();
        // Запускаем таймер неактивности
        this.resetInactivityTimer();
    }

    setupEventListeners() {
        // События, которые сбрасывают таймер неактивности
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
        
        events.forEach(event => {
            document.addEventListener(event, () => {
                this.resetInactivityTimer();
            });
        });

        this.stayActiveBtn.addEventListener('click', () => {
            this.hideModal();
            this.resetInactivityTimer();
        });

        this.countdownTimer = setInterval(() => {
            console.log(this.countdownElement.textContent);
            
            if (this.modal.style.display === 'flex') {
                this.updateCountdown();
            }
        }, 1000);
    }

    resetInactivityTimer() {
        clearTimeout(this.inactivityTimer);
        
        this.inactivityTimer = setTimeout(() => {
            this.showModal();
        }, this.inactivityTime);
    }

    showModal() {
        this.modal.style.display = 'flex';
        this.startCountdown();
    }

    hideModal() {
        this.modal.style.display = 'none';
        this.resetCountdown();
    }

    startCountdown() {
        let secondsLeft = this.countdownTime / 1000;
        this.countdownElement.textContent = secondsLeft;

        this.countdownTimer = setTimeout(() => {
            this.executeInactivityAction();
        }, this.countdownTime);
    }

    updateCountdown() {
        let currentSeconds = parseInt(this.countdownElement.textContent);
        if (currentSeconds > 1) {
            this.countdownElement.textContent = currentSeconds - 1;
        }
    }

    resetCountdown() {
        clearTimeout(this.countdownTimer);
    }

    executeInactivityAction() {
        // 1. Сбрасываем куки
        this.clearCookies();
        
        // 2. Включаем камеру
        this.enableCamera();
        
        // 3. Скрываем модалку
        this.hideModal();
        
        // 4. Перенаправляем или обновляем страницу
        window.location.reload();
    }

    clearCookies() {
        const cookies = document.cookie.split(';');
        
        for (let cookie of cookies) {
            const eqPos = cookie.indexOf('=');
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
        }
        
        console.log('Все куки сброшены');
    }

    async enableCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: true 
            });
            
            // Создаем элемент для отображения видео
            const video = document.createElement('video');
            video.srcObject = stream;
            video.autoplay = true;
            video.style.position = 'fixed';
            video.style.top = '0';
            video.style.left = '0';
            video.style.width = '300px';
            video.style.zIndex = '1001';
            
            document.body.appendChild(video);
            
            console.log('Камера активирована');
            
        } catch (error) {
            console.error('Ошибка доступа к камере:', error);
        }
    }
}

// Инициализация когда DOM загружен
document.addEventListener('DOMContentLoaded', () => {
    new InactivityManager();
});