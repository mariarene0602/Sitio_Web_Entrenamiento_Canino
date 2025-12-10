// Funcionalidades generales del sitio
document.addEventListener('DOMContentLoaded', function() {
    // Toggle del menú móvil
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            this.querySelector('i').classList.toggle('fa-bars');
            this.querySelector('i').classList.toggle('fa-times');
        });
    }
    
    // Cerrar menú móvil al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.main-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (mainNav.classList.contains('active')) {
                mainNav.classList.remove('active');
                mobileMenuToggle.querySelector('i').classList.remove('fa-times');
                mobileMenuToggle.querySelector('i').classList.add('fa-bars');
            }
        });
    });
    
    // Animación de scroll suave para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Efecto de aparición al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observar elementos para animación
    const elementsToAnimate = document.querySelectorAll('.feature-card, .course-preview-card, .service-card');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
    
    // Verificar si el usuario está autenticado
    checkAuthStatus();
});

// Verificar estado de autenticación
function checkAuthStatus() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    const loginButton = document.querySelector('.nav-login-button');
    
    if (user && loginButton) {
        loginButton.innerHTML = `<i class="fas fa-user"></i> MI CUENTA`;
        loginButton.href = 'perfil.html';
        
        // Agregar opción de cerrar sesión
        const logoutItem = document.createElement('li');
        logoutItem.innerHTML = `<a href="#" id="logout-link">CERRAR SESIÓN</a>`;
        loginButton.parentNode.parentNode.appendChild(logoutItem);
        
        document.getElementById('logout-link').addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}

// Validar formularios
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showInputError(input, 'Este campo es obligatorio');
            isValid = false;
        } else {
            clearInputError(input);
            
            // Validaciones específicas por tipo
            if (input.type === 'email' && !isValidEmail(input.value)) {
                showInputError(input, 'Ingresa un email válido');
                isValid = false;
            }
            
            if (input.type === 'password' && input.value.length < 6) {
                showInputError(input, 'La contraseña debe tener al menos 6 caracteres');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

// Mostrar error en input
function showInputError(input, message) {
    clearInputError(input);
    
    input.classList.add('error');
    
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    
    input.parentNode.appendChild(errorElement);
}

// Limpiar error de input
function clearInputError(input) {
    input.classList.remove('error');
    
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Formatear precio
function formatPrice(price) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(price);
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animación de entrada
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Cerrar notificación
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto cerrar después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}