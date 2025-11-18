document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('productModal');
    const closeBtn = document.querySelector('.close');
    const quickViewButtons = document.querySelectorAll('.quick-view-btn');
    
    // Элементы модального окна
    const modalProductImage = document.getElementById('modalProductImage');
    const modalProductName = document.getElementById('modalProductName');
    const modalProductDescription = document.getElementById('modalProductDescription');
    const modalProductPrice = document.getElementById('modalProductPrice');
    const modalTotalPrice = document.getElementById('modalTotalPrice');
    const modalAddToCart = document.getElementById('modalAddToCart');
    const modalStockStatus = document.getElementById('modalStockStatus');
    const modalOutOfStock = document.getElementById('modalOutOfStock');
    
    // Переменные для хранения текущего продукта
    let currentProduct = null;
    let basePrice = 0;
    let quantity = 1;
    let productInStock = true;
    let count = 0;
    let scrollPosition = 0;

    function openModal(productCard) {
        // Сохраняем позицию скролла
        scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        
        const productId = productCard.dataset.productId;
        const productName = productCard.dataset.productName;
        const productPrice = parseFloat(productCard.dataset.productPrice);
        const productImage = productCard.dataset.productImage;
        const productDescription = productCard.dataset.productDescription;
        const inStock = parseInt(productCard.dataset.productCount) > 0;
        const productCount = parseInt(productCard.dataset.productCount);
        
        // Заполняем модальное окно данными
        modalProductImage.src = productImage;
        modalProductImage.alt = productName;
        modalProductName.textContent = productName;
        modalProductDescription.textContent = productDescription;
        modalProductPrice.textContent = productPrice.toLocaleString();
        
        // Устанавливаем статус наличия
        productInStock = inStock;
        count = productCount;
        
        if (inStock) {
            modalStockStatus.textContent = `В наличии (${productCount} шт.)`;
            modalStockStatus.className = 'in-stock-modal';
            modalAddToCart.disabled = false;
            modalOutOfStock.style.display = 'none';
        } else {
            modalStockStatus.textContent = 'Отсутствует';
            modalStockStatus.className = 'out-of-stock-modal';
            modalAddToCart.disabled = true;
            modalOutOfStock.style.display = 'block';
        }
        
        // Сохраняем текущий продукт и базовую цену
        currentProduct = productId;
        basePrice = productPrice;
        quantity = 1;
        
        // Сбрасываем количество
        document.querySelector('.quantity').textContent = quantity;
        
        // Обновляем общую цену
        updateTotalPrice();
        
        // Показываем модальное окно
        modal.style.display = 'block';
        document.body.classList.add('modal-open');
        document.body.style.setProperty('--scroll-top', `-${scrollPosition}px`);
        document.body.style.top = `-${scrollPosition}px`;
    }
    
    function closeModal() {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
        document.body.style.top = '';
        
        // Восстанавливаем позицию скролла
        window.scrollTo(0, scrollPosition);
    }
    
    function updateTotalPrice() {
        const totalPrice = parseFloat((basePrice * quantity).toFixed(2));

        modalTotalPrice.textContent = totalPrice.toLocaleString();
        modalAddToCart.innerHTML = `Добавить в корзину - ${totalPrice.toLocaleString()} руб.`;
    }

    // Открытие модального окна при клике на кнопку быстрого просмотра
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Предотвращаем всплытие
            const productCard = this.closest('.product-card');
            
            // Проверяем, есть ли товар в наличии
            const inStock = parseInt(productCard.dataset.productCount) > 0;
            
            if (!inStock) {
                showNotification('Этот товар временно отсутствует', 'warning');
                return;
            }
            
            openModal(productCard);
        });
    });
    
    // Закрытие модального окна
    closeBtn.addEventListener('click', closeModal);
    
    // Закрытие при клике вне модального окна
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Закрытие по ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
    
    // Управление количеством
    document.querySelector('.quantity-btn.minus').addEventListener('click', function() {
        if (quantity > 1) {
            quantity--;
            document.querySelector('.quantity').textContent = quantity;
            updateTotalPrice();
        }
    });
    
    document.querySelector('.quantity-btn.plus').addEventListener('click', function() {
        if (quantity < count) {
            quantity++;
            document.querySelector('.quantity').textContent = quantity;
            updateTotalPrice();
        } else {
            showNotification('Достигнуто максимальное количество товара', 'warning');
        }
    });
    
    // Добавление в корзину
    modalAddToCart.addEventListener('click', function() {
        if (!productInStock) {
            showNotification('Этот товар закончился!', 'error');
            return;
        }
        
        const totalPrice = basePrice * quantity;
        const productName = modalProductName.textContent;

        // Добавляем в корзину через cookies
        document.cookie = `${currentProduct}=${quantity}; path=/; max-age=86400`;
        
        // Показываем уведомление
        showNotification(`"${productName}" добавлен в корзину!`, 'success');
        
        // Обновляем виджет корзины
        if (typeof updateCartWidget === 'function') {
            updateCartWidget();
        }
        
        closeModal();
    });

    // Улучшенная функция показа уведомления
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        const backgroundColor = type === 'success' ? '#10b981' : 
                            type === 'warning' ? '#f59e0b' : '#ef4444';
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px; /* Изменили right на left */
            background: ${backgroundColor};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 1001;
            font-weight: 600;
            transform: translateX(-100%); /* Изменили на отрицательное значение */
            transition: transform 0.3s ease;
            max-width: 300px;
            word-wrap: break-word;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(0)'; /* Остается 0 */
        }, 100);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(-100%)'; /* Изменили на отрицательное значение */
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
});