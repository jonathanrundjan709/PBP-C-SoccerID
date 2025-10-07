function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');
    
    if (!toastComponent) return;

    // Remove all type classes first
    toastComponent.classList.remove(
        'bg-red-50', 'border-red-500', 'text-red-600',
        'bg-green-50', 'border-green-500', 'text-green-600',
        'bg-blue-50', 'border-blue-500', 'text-blue-600',
        'bg-white', 'border-gray-300', 'text-gray-800'
    );

    // Set type styles and icon
    let icon = '';
    if (type === 'success') {
        toastComponent.classList.add('bg-green-50', 'border-green-500', 'text-green-600');
        toastComponent.style.border = '2px solid #22c55e';
        icon = '✓';
    } else if (type === 'error') {
        toastComponent.classList.add('bg-red-50', 'border-red-500', 'text-red-600');
        toastComponent.style.border = '2px solid #ef4444';
        icon = '✕';
    } else if (type === 'info') {
        toastComponent.classList.add('bg-blue-50', 'border-blue-500', 'text-blue-600');
        toastComponent.style.border = '2px solid #3b82f6';
        icon = 'ℹ';
    } else {
        toastComponent.classList.add('bg-white', 'border-gray-300', 'text-gray-800');
        toastComponent.style.border = '2px solid #d1d5db';
        icon = '●';
    }

    toastIcon.textContent = icon;
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Show toast with slide-up animation
    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    // Auto hide after duration
    setTimeout(() => {
        toastComponent.classList.remove('opacity-100', 'translate-y-0');
        toastComponent.classList.add('opacity-0', 'translate-y-64');
    }, duration);
}

// Alternative: show toast with custom styling
function showCustomToast(options) {
    const {
        title = 'Notification',
        message = '',
        type = 'normal',
        duration = 3000,
        position = 'bottom-right'
    } = options;
    
    showToast(title, message, type, duration);
}