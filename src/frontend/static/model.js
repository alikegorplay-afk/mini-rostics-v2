document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('productModal');
    const closeBtn = document.querySelector('.close');
    const productCards = document.querySelectorAll('.product-card');
    
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
    
    function openModal(productCard) {
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
            modalAddToCart.textContent = `Добавить в корзину - ${productPrice.toLocaleString()} руб.`;
        } else {
            modalStockStatus.textContent = 'Отсутствует';
            modalStockStatus.className = 'out-of-stock-modal';
            modalAddToCart.disabled = true;
            modalOutOfStock.style.display = 'block';
            modalAddToCart.textContent = 'Товар отсутствует';
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
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed'; // Предотвращает скролл на iOS
    }
    
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        document.body.style.position = 'static';
    }
    
    function updateTotalPrice() {
        const totalPrice = basePrice * quantity;
        modalTotalPrice.textContent = totalPrice.toLocaleString();
        modalAddToCart.textContent = `Добавить в корзину - ${totalPrice.toLocaleString()} руб.`;
    }
    
    // Открытие модального окна при клике на карточку
    productCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Проверяем, не был ли клик по кнопке или другому интерактивному элементу
            if (!e.target.closest('button') && !e.target.classList.contains('add-to-cart')) {
                openModal(this);
            }
        });
        
        // Добавляем обработчик для тач-событий (для мобильных)
        card.addEventListener('touchend', function(e) {
            if (!e.target.closest('button') && !e.target.classList.contains('add-to-cart')) {
                e.preventDefault();
                openModal(this);
            }
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
    
    // Закрытие при таче вне модального окна (для мобильных)
    modal.addEventListener('touchend', function(e) {
        if (e.target === modal) {
            e.preventDefault();
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
            alert("На складе больше нет данного продукта!");
        }
    });
    
    // Тач-события для кнопок количества (мобильные)
    document.querySelector('.quantity-btn.minus').addEventListener('touchend', function(e) {
        e.preventDefault();
        if (quantity > 1) {
            quantity--;
            document.querySelector('.quantity').textContent = quantity;
            updateTotalPrice();
        }
    });
    
    document.querySelector('.quantity-btn.plus').addEventListener('touchend', function(e) {
        e.preventDefault();
        if (quantity < count) {
            quantity++;
            document.querySelector('.quantity').textContent = quantity;
            updateTotalPrice();
        } else {
            alert("На складе больше нет данного продукта!");
        }
    });
    
    // Добавление в корзину
    modalAddToCart.addEventListener('click', function() {
        if (!productInStock) {
            alert('Этот товар закончился!');
            return;
        }
        
        const totalPrice = basePrice * quantity;
        const productName = modalProductName.textContent;

        // Логика добавления в корзину
        console.log('Добавление в корзину:', {
            productId: currentProduct,
            productName: productName,
            quantity: quantity,
            totalPrice: totalPrice
        });

        // Пример работы с cookies
        document.cookie = `${currentProduct}=${quantity}; path=/; max-age=86400`; // 1 день
        
        // Показываем уведомление
        showNotification(`Товар "${productName}" добавлен в корзину!`);
        
        updateCartWidget();
        closeModal();
    });
    
    // Тач-событие для кнопки добавления в корзину
    modalAddToCart.addEventListener('touchend', function(e) {
        e.preventDefault();
        if (!productInStock) {
            alert('Этот товар закончился!');
            return;
        }
        
        const totalPrice = basePrice * quantity;
        const productName = modalProductName.textContent;

        document.cookie = `${currentProduct}=${quantity}; path=/; max-age=86400`;
        
        showNotification(`Товар "${productName}" добавлен в корзину!`);
        
        closeModal();
    });

    // Функция показа уведомления
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 1001;
            font-weight: 600;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    function getCartData() {
        let cookies = document.cookie.split("; ");
        let orderData = { items: [] };

        cookies.forEach(entry => {
            let [key, value] = entry.split('=');
            key = key?.trim();
            value = value?.trim();
            
            if (key && /^\d+$/.test(key)) {
                let productId = parseInt(key);
                let count = parseInt(value) || 1;
                
                orderData.items.push({
                    product_id: productId,
                    count: count
                });
            }
        });

        return orderData;
    }
});