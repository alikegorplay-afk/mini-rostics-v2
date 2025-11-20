// Функции для корзины
function updateCartWidget() {
    const cartData = getCartData();
    const cartCount = document.getElementById('cartCount');
    if (!cartCount) return;
    
    const totalItems = cartData.items.reduce((sum, item) => sum + item.count, 0);
    
    cartCount.textContent = totalItems;
    
    // Анимация при изменении количества
    if (totalItems > 0) {
        cartCount.style.animation = 'none';
        setTimeout(() => {
            if (cartCount) {
                cartCount.style.animation = 'pulse 2s infinite';
            }
        }, 10);
    }
}

function openCartModal() {
    const cartModal = document.getElementById('cartModal');
    if (!cartModal) return;
    
    const cartData = getCartData();
    
    // Сначала показываем модальное окно, потом загружаем данные
    cartModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Загружаем данные товаров и отображаем корзину
    loadCartItems(cartData);
}

function closeCartModal() {
    const cartModal = document.getElementById('cartModal');
    if (!cartModal) return;

    cartModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function getCartElement(id) {
    return document.getElementById(id);
}

async function loadCartItems(cartData) {
    const cartItems = getCartElement('cartItems');
    const emptyCart = getCartElement('emptyCart');
    const cartTotalPrice = getCartElement('cartTotalPrice');
    const orderBtn = getCartElement('orderBtn');
    
    console.log(cartItems, emptyCart, cartTotalPrice, orderBtn);
    

    // Проверяем что все элементы существуют
    if (!cartItems || !cartTotalPrice || !orderBtn) {
        console.error('Cart elements not found');
        return;
    }
    
    if (cartData.items.length === 0) {
        cartItems.innerHTML = '';
        cartTotalPrice.textContent = '0 руб.';
        orderBtn.disabled = true;
        return;
    }
    
    // emptyCart.style.display = 'none';
    orderBtn.disabled = false;
    
    let totalPrice = 0;
    let itemsHTML = '';
    let loadedItems = 0;
    
    // Показываем загрузку
    cartItems.innerHTML = '<div class="empty-cart">Загрузка товаров...</div>';
    
    // Загружаем информацию о каждом товаре
    for (const item of cartData.items) {
        try {
            const product = await getProductInfo(item.product_id);
            const itemTotal = Math.round(product.price * item.count * 100) / 100;
            console.log(itemTotal);
            
            totalPrice += itemTotal;
            loadedItems++;
        
            itemsHTML += `
                <div class="cart-item" data-product-id="${product.id}">
                    <img src="${product.poster}" alt="${product.title}" class="cart-item-image" 
                         onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zMCAzNUMzMi43NjE0IDM1IDM1IDMyLjc2MTQgMzUgMzBDMzUgMjcuMjM4NiAzMi43NjE0IDI1IDMwIDI1QzI3LjIzODYgMjUgMjUgMjcuMjM4NiAyNSAzMEMyNSAzMi43NjE0IDI3LjIzODYgMzUgMzAgMzVaIiBmaWxsPSIjOTlBQUFGIi8+CjxwYXRoIGQ9Ik0zNSAyMEgzNUgyNVY0MEgzNVYyMFoiIGZpbGw9IiM5OUFBQUYiLz4KPC9zdmc+'">
                    <div class="cart-item-info">
                        <div class="cart-item-name">${product.title}</div>
                        <div class="cart-item-price">${product.price} руб. × ${item.count} = ${itemTotal} руб.</div>
                    </div>
                    <button class="cart-item-remove" data-product-id="${product.id}">×</button>
                </div>
            `;
            
        } catch (error) {
            console.error('Error loading cart item:', error);
            loadedItems++;
            
            // Добавляем сообщение об ошибке для этого товара
            itemsHTML += `
                <div class="cart-item" data-product-id="${item.product_id}">
                    <div class="cart-item-info">
                        <div class="cart-item-name">Товар #${item.product_id} (ошибка загрузки)</div>
                        <div class="cart-item-price">0 руб. × ${item.count} = 0 руб.</div>
                    </div>
                    <button class="cart-item-remove" data-product-id="${item.product_id}">×</button>
                </div>
            `;
        }
    }
    
    // Обновляем DOM после загрузки всех товаров
    if (loadedItems === cartData.items.length) {
        cartItems.innerHTML = itemsHTML;
        cartTotalPrice.textContent = `${Math.round(totalPrice * 100) / 100} руб.`;
        
        // Добавляем обработчики событий для новых элементов
        addCartEventListeners();
    }
}

function addCartEventListeners() {
    // Обработчики для кнопок изменения количества
    document.querySelectorAll('.quantity-change.minus').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = parseInt(this.dataset.productId);
            changeCartQuantity(productId, -1);
        });
    });
    
    document.querySelectorAll('.quantity-change.plus').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = parseInt(this.dataset.productId);
            changeCartQuantity(productId, 1);
        });
    });
    
    // Обработчики для кнопок удаления
    document.querySelectorAll('.cart-item-remove').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = parseInt(this.dataset.productId);
            removeFromCart(productId);
        });
    });
}

// Функция для получения информации о товаре
async function getProductInfo(productId) {
    try {
        let url = "/api/v1/product/" + productId;
        console.log("Fetching product from:", url);
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("API response:", data);
        
        if (data.ok === true && data.result) {
            const product = data.result;
            console.log("Found product:", product);
            return {
                id: product.id || productId,
                title: product.title || 'Товар',
                price: parseFloat(product.price) || 0,
                poster: product.poster || '',
                description: product.description || 'Описание отсутствует'
            };
        } else {
            throw new Error('Product not found in response');
        }
        
    } catch (error) {
        console.error('Error fetching product info:', error);
        
        // Пробуем найти товар среди уже загруженных на странице
        const productCards = document.querySelectorAll('.product-card');
        for (const card of productCards) {
            if (parseInt(card.dataset.productId) === productId) {
                console.log("Found product in DOM:", card.dataset.productName);
                return {
                    id: productId,
                    title: card.dataset.productName,
                    price: parseFloat(card.dataset.productPrice),
                    poster: card.dataset.productImage,
                    description: card.dataset.productDescription
                };
            }
        }
        
        // Если ничего не нашли, возвращаем заглушку
        return {
            id: productId,
            title: 'Товар #' + productId,
            price: 0,
            poster: '',
            description: 'Информация о товаре не найдена'
        };
    }
}

function changeCartQuantity(productId, change) {
    const cartData = getCartData();
    const item = cartData.items.find(item => item.product_id === productId);
    console.log(item);
    
    if (item) {
        item.count += change;
        
        if (item.count <= 0) {
            // Удаляем товар если количество стало 0 или меньше
            removeFromCart(productId);
        } else {
            // Обновляем куки
            document.cookie = `${productId}=${item.count}; path=/; max-age=86400`;
            updateCartWidget();
            // Перезагружаем корзину
            const cartData = getCartData();
            loadCartItems(cartData);
        }
    }
}

function removeFromCart(productId) {
    // Удаляем куки
    document.cookie = `${productId}=; path=/; max-age=0`;
    updateCartWidget();
    
    // Перезагружаем корзину
    const cartData = getCartData();
    loadCartItems(cartData);
}

async function placeOrder() {
    const cartData = getCartData();
    
    if (cartData.items.length === 0) {
        alert('Корзина пуста!');
        return;
    }
    
    try {
        // Показываем индикатор загрузки
        const orderBtn = document.getElementById('orderBtn');
        const originalText = orderBtn.innerHTML;
        orderBtn.innerHTML = '<span class="order-btn-text">Оформление...</span><span class="order-btn-icon"></span>';
        orderBtn.disabled = true;
        
        console.log('Отправка заказа:', cartData);
        
        const response = await fetch('/api/v1/order', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(cartData)
        });
        
        console.log('Ответ сервера:', response);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Результат заказа:', result);
        
        if (result.ok) {
            // Очищаем корзину
            cartData.items.forEach(item => {
                document.cookie = `${item.product_id}=; path=/; max-age=0`;
            });
            
            updateCartWidget();
            closeCartModal();
        
            await showQRCode(result);
            orderBtn.innerHTML = `
                    <span class="order-btn-text">Заказать</span>
                    <span class="order-btn-icon">🚀</span>
                    `
        } else {
            throw new Error(result.message || 'Ошибка при оформлении заказа');
        }
        
    } catch (error) {
        console.error('Ошибка оформления заказа:', error);
        
        let errorMessage = 'Ошибка при оформлении заказа';
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            errorMessage = 'Ошибка сети. Проверьте подключение к интернету';
        } else if (error.message.includes('500')) {
            errorMessage = 'Ошибка сервера. Попробуйте позже';
        } else {
            errorMessage = error.message;
        }
        
        showNotification(errorMessage, 'error');
    } finally {
        // Всегда восстанавливаем кнопку
        const orderBtn = document.getElementById('orderBtn');
        if (orderBtn) {
            orderBtn.innerHTML = originalText;
            orderBtn.disabled = false;
        }
    }
}

// Функция для показа QR кода
async function showQRCode(orderResult) {
    const qrModal = document.getElementById('qrModal');
    const qrCodeImage = document.getElementById('qrCodeImage');
    const qrLoading = document.getElementById('qrLoading');
    const orderNumber = document.getElementById('orderNumber');
    const orderTotalAmount = document.getElementById('orderTotalAmount');
    
    if (!qrModal || !qrCodeImage) {
        console.error('QR modal elements not found');
        return;
    }
    
    try {
        // Устанавливаем номер заказа и сумму
        orderNumber.textContent = orderResult.result.id
        orderTotalAmount.textContent = await calculateOrderTotal(orderResult);
        
        // Показываем модальное окно
        qrModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Показываем индикатор загрузки
        qrLoading.style.display = 'block';
        qrCodeImage.style.display = 'none';
        
        // Генерируем данные для QR кода
        const qrData = generateQRData(orderResult);
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=450x450&data=${encodeURIComponent(qrData)}`;
        
        // Загружаем QR код
        qrCodeImage.onload = function() {
            qrLoading.style.display = 'none';
            qrCodeImage.style.display = 'block';
        };
        
        qrCodeImage.onerror = function() {
            qrLoading.style.display = 'none';
            qrCodeImage.style.display = 'block';
            qrCodeImage.alt = 'Ошибка загрузки QR кода';
            console.error('Failed to load QR code');
        };
        
        qrCodeImage.src = qrUrl;
        
    } catch (error) {
        console.error('Error showing QR code:', error);
        qrLoading.textContent = 'Ошибка генерации QR кода';
    }
}

// Функция для генерации данных QR кода
function generateQRData(orderResult) {
    const baseURL = window.location.origin;
    return `${baseURL}/order/${orderResult.result.id}`
}

// Функция для расчета общей суммы заказа
async function calculateOrderTotal(orderResult) {
    try {
        let products = {};
        const productIds = [];
        
        for (let x of orderResult.result.items) {
            products[x.product_id] = x.count;
            productIds.push(x.product_id);
        }
        console.log('Products data:', products);
        console.log(JSON.stringify(productIds));

        // Если API ожидает POST с body
        const response = await fetch('/api/v1/products', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(productIds // Отправляем массив ID
            )
        });
        
        console.log('Ответ сервера:', response);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Products data from API:', data);
        
        let total = 0;
        
        if (data.ok && data.result) {
            for (let product of data.result) {
                if (products[product.id]) {
                    total += product.price * products[product.id];
                }
            }
        }
        
        total = Math.round(total * 100) / 100;

        console.log('Calculated total:', total);
        return total;
        
    } catch (error) {
        console.error('Error calculating order total:', error);
        return 0;
    }
}

// Функции для управления QR модальным окном
function closeQRModal() {
    const qrModal = document.getElementById('qrModal');
    if (qrModal) {
        qrModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function printQRCode() {
    const qrCodeImage = document.getElementById('qrCodeImage');
    if (qrCodeImage) {
        console.log(1231231231);
        
        console.log(document.getElementById('orderTotalAmount'));
        
        const price = Math.round(parseFloat(document.getElementById('orderTotalAmount').textContent) * 100) / 100;
        console.log(price);
        
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>QR Code - Заказ</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            text-align: center; 
                            padding: 2rem;
                        }
                        .qr-code { 
                            max-width: 400px; 
                            height: auto; 
                            margin: 1rem 0;
                        }
                        .order-info {
                            margin: 1rem 0;
                            font-size: 1.2rem;
                        }
                    </style>
                </head>
                <body>
                    <h2>Ваш заказ</h2>
                    <div class="order-info">
                        <p>Номер: ${document.getElementById('orderNumber').textContent}</p>
                        <p>Сумма: ${price} руб.</p>
                    </div>
                    <img src="${qrCodeImage.src}" alt="QR Code" class="qr-code">
                    <p>Сохраните этот QR код для отслеживания заказа</p>
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// Обновленная функция showNotification для разных типов уведомлений
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const backgroundColor = type === 'success' ? '#10b981' : '#ef4444';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${backgroundColor};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1002;
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
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обновляем виджет корзины при загрузке
    updateCartWidget();
    
    // Обработчики для виджета корзины
    const cartWidget = getCartElement('cartWidget');
    const cartClose = document.querySelector('.cart-close');
    const orderBtn = getCartElement('orderBtn');
    const cartModal = getCartElement('cartModal');
    
    if (cartWidget) {
        cartWidget.addEventListener('click', openCartModal);
    }
    
    if (cartClose) {
        cartClose.addEventListener('click', closeCartModal);
    }
    
    if (orderBtn) {
        orderBtn.addEventListener('click', placeOrder);
    }
    
    if (cartModal) {
        // Закрытие модального окна корзины при клике вне его
        cartModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeCartModal();
            }
        });
    }
    document.querySelector('.qr-close')?.addEventListener('click', closeQRModal);
    document.getElementById('qrCloseBtn')?.addEventListener('click', closeQRModal);
    
    // Закрытие QR модального окна при клике вне его
    document.getElementById('qrModal')?.addEventListener('click', function(e) {
        if (e.target === this) {
            closeQRModal();
        }
    });
    
    // Закрытие по ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const cartModal = getCartElement('cartModal');
            if (cartModal && cartModal.style.display === 'block') {
                closeCartModal();
            }
        }
    });
});

// Обновляем функцию getCartData для более надежной работы
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
            
            // Проверяем, что количество положительное
            if (count > 0) {
                orderData.items.push({
                    product_id: productId,
                    count: count
                });
            }
        }
    });

    return orderData;
}