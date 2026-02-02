// Luxury Shopping Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Cart functionality
    updateCartCount();
    
    // Add to cart animations
    const addToCartButtons = document.querySelectorAll('form[action*="add_to_cart"] button');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent double submission via class check instead of disabled property
            if (this.classList.contains('processing')) {
                e.preventDefault();
                return;
            }

            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading"></span> Adding...';
            this.classList.add('processing');
            // We do NOT set this.disabled = true; as it can prevent form submission in some browsers
            
            // Reset after a short delay (in case navigation doesn't happen)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('processing');
            }, 2000);
        });
    });

    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton && !form.checkValidity()) {
                submitButton.disabled = false;
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Search functionality (if implemented)
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Quantity selector for cart (if implemented)
    const quantitySelectors = document.querySelectorAll('.quantity-selector');
    quantitySelectors.forEach(selector => {
        const decreaseBtn = selector.querySelector('.decrease');
        const increaseBtn = selector.querySelector('.increase');
        const input = selector.querySelector('input[type="number"]');
        
        if (decreaseBtn && increaseBtn && input) {
            decreaseBtn.addEventListener('click', () => {
                if (input.value > 1) {
                    input.value = parseInt(input.value) - 1;
                }
            });
            
            increaseBtn.addEventListener('click', () => {
                input.value = parseInt(input.value) + 1;
            });
        }
    });

    // Admin panel enhancements
    const adminStats = document.querySelectorAll('.stats-card');
    adminStats.forEach(card => {
        card.addEventListener('click', function() {
            // Add pulse animation
            this.style.animation = 'pulse 0.5s';
            setTimeout(() => {
                this.style.animation = '';
            }, 500);
        });
    });

    // Progressive Loading (Load More)
    const loadMoreButtons = document.querySelectorAll('.btn-load-more');
    loadMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            const section = document.querySelector(`.category-section[data-category="${category}"]`);
            const grid = section.querySelector('.product-grid');
            let page = parseInt(section.dataset.page) + 1;
            
            // Add loading state
            const originalButtonContent = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Curating more...';
            this.disabled = true;

            fetch(`/api/products?category=${encodeURIComponent(category)}&page=${page}&per_page=6`)
                .then(response => response.json())
                .then(data => {
                    if (data.products && data.products.length > 0) {
                        data.products.forEach(product => {
                            const productHtml = createProductHtml(product);
                            grid.insertAdjacentHTML('beforeend', productHtml);
                        });
                        
                        section.dataset.page = page;
                        
                        // Add fade-in animation to new cards
                        grid.querySelectorAll('.product-card:not(.fade-in)').forEach(el => {
                            if (typeof fadeObserver !== 'undefined') fadeObserver.observe(el);
                        });

                        if (!data.has_next) {
                            this.remove();
                        } else {
                            this.innerHTML = originalButtonContent;
                            this.disabled = false;
                        }
                    } else {
                        this.remove();
                    }
                })
                .catch(error => {
                    console.error('Error loading products:', error);
                    this.innerHTML = originalButtonContent;
                    this.disabled = false;
                });
        });
    });
});

// Cart count update function
function updateCartCount() {
    // This would typically make an AJAX call to get the current cart count
    // For now, we'll use a placeholder
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        // Update with actual cart count from server
        // element.textContent = cartCount;
    });
}

// Search function (placeholder)
function performSearch(query) {
    if (query.length < 2) return;
    
    // This would typically make an AJAX call to search products
    console.log('Searching for:', query);
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function createProductHtml(product) {
    const formattedPrice = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(product.price);

    const sessionUserId = document.body.dataset.userId;

    let cartButtonHtml = '';
    if (sessionUserId) {
        cartButtonHtml = `
            <form action="/add_to_cart/${product.id}" method="POST">
                <button type="submit" class="btn btn-luxury w-100 btn-sm" ${product.stock === 0 ? 'disabled' : ''}>
                    <i class="fas fa-cart-plus me-1"></i> Add to Cart
                </button>
            </form>
        `;
    }

    return `
        <div class="col-md-4 mb-4">
            <div class="card h-100 product-card shadow-sm">
                ${product.image_url ? 
                    `<img src="${product.image_url}" class="card-img-top product-image" alt="${product.name}" loading="lazy">` :
                    `<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 300px;">
                        <i class="fas fa-image fa-3x text-muted"></i>
                    </div>`
                }
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text text-muted smaller">${product.description.substring(0, 100)}${product.description.length > 100 ? '...' : ''}</p>
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="h5 text-primary mb-0">${formattedPrice}</span>
                            <small class="text-muted">Stock: ${product.stock}</small>
                        </div>
                        <div class="d-grid gap-2">
                            <a href="/product/${product.id}" class="btn btn-outline-dark btn-sm">View Details</a>
                            ${cartButtonHtml}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Add fade-in animation to elements as they come into view
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            fadeObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all product cards and cards
document.querySelectorAll('.product-card, .card').forEach(el => {
    fadeObserver.observe(el);
});

// AI Advisor Chat Widget
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatToggle) return; // Only run if widget exists

    // Generate or retrieve persistent session ID
    let sessionId = localStorage.getItem('lux_chat_session_id');
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('lux_chat_session_id', sessionId);
    }

    // Load conversation history on page load
    loadConversationHistory();

    async function loadConversationHistory() {
        try {
            const response = await fetch(`/api/conversation_history?session_id=${encodeURIComponent(sessionId)}`);
            const data = await response.json();
            
            if (data.history && data.history.length > 0) {
                // Rebuild the conversation
                chatMessages.innerHTML = '';
                
                // Always start with the greeting
                addMessage("Hello! I'm Lux, your personal shopping advisor. How can I assist you today?", 'ai');
                
                // Add the conversation history
                data.history.forEach(msg => {
                    addMessage(msg.content, msg.role === 'assistant' ? 'ai' : 'user');
                });
            }
            // If no history, keep the default greeting
        } catch (error) {
            console.log('Could not load conversation history:', error);
            // Keep the default greeting if history can't be loaded
        }
    }

    function toggleChat() {
        if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
            chatWindow.style.display = 'flex';
            chatInput.focus();
        } else {
            chatWindow.style.display = 'none';
        }
    }

    if (chatToggle) chatToggle.addEventListener('click', toggleChat);
    if (chatClose) chatClose.addEventListener('click', toggleChat);

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        
        // Convert URLs to clickable links - match http/https URLs and valid relative paths
        const urlPattern = /(https?:\/\/[^\s]+)|(\/[a-zA-Z0-9\-_\/]+)/g;
        const parts = text.split(urlPattern).filter(Boolean);
        
        parts.forEach(part => {
            if (part && (part.startsWith('http://') || part.startsWith('https://') || (part.startsWith('/') && /^\/[a-zA-Z0-9\-_\/]+$/.test(part)))) {
                const link = document.createElement('a');
                link.href = part;
                link.textContent = part;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.setAttribute('aria-label', part + ' (opens in new tab)');
                link.style.color = type === 'ai' ? '#c0392b' : '#e74c3c';
                link.style.textDecoration = 'underline';
                link.style.fontWeight = '500';
                div.appendChild(link);
            } else if (part) {
                div.appendChild(document.createTextNode(part));
            }
        });
        
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Dev Mode: Allow setting API key locally and detect provider
        if (text.startsWith('/apikey ')) {
            const key = text.substring(8).trim();
            if (key) {
                // Determine provider based on key format
                let provider = 'openai';
                if (key.startsWith('AIza')) {
                    provider = 'gemini';
                }
                
                localStorage.setItem('local_dev_key', key);
                localStorage.setItem('local_dev_provider', provider);
                addMessage(`System: Dev API Key saved for ${provider.toUpperCase()}.`, 'ai');
            }
            chatInput.value = '';
            return;
        }
        if (text === '/clearkey') {
            localStorage.removeItem('local_dev_key');
            localStorage.removeItem('local_dev_provider');
            localStorage.removeItem('openai_dev_key'); // Cleanup old key
            addMessage('System: Dev API Keys removed.', 'ai');
            chatInput.value = '';
            return;
        }
        if (text === '/clearsession') {
            // Generate new session ID
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('lux_chat_session_id', sessionId);
            // Clear chat messages
            chatMessages.innerHTML = '<div class="message ai">Hello! I\'m Lux, your personal shopping advisor. How can I assist you today?</div>';
            addMessage('System: New conversation session started.', 'ai');
            chatInput.value = '';
            return;
        }

        addMessage(text, 'user');
        chatInput.value = '';
        chatInput.disabled = true;

        // Add loading spinner
        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Thinking...';
        chatMessages.appendChild(spinner);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            // Check new key storage first, fallback to old key name if exists
            const devKey = localStorage.getItem('local_dev_key') || localStorage.getItem('openai_dev_key');
            const devProvider = localStorage.getItem('local_dev_provider'); // Might be null
            
            const response = await fetch('/api/ask_advisor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    question: text,
                    api_key: devKey,
                    provider: devProvider,
                    session_id: sessionId
                })
            });

            spinner.remove();
            
            const data = await response.json();
            
            if (data.error) {
                 addMessage('Error: ' + data.error, 'ai');
            } else {
                addMessage(data.answer, 'ai');
            }

        } catch (error) {
            spinner.remove();
            addMessage('Sorry, I encountered an error connecting to the server.', 'ai');
        } finally {
            chatInput.disabled = false;
            chatInput.focus();
        }
    }

    if (chatSend) {
        chatSend.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }
});
