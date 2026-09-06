/**
 * Plain JavaScript App Modal Controller
 */
export function openAppModal() {
    const modal = document.getElementById('app-modal');
    const backdrop = document.getElementById('app-modal-backdrop');
    const card = document.getElementById('app-modal-card');

    if (!modal) return;

    modal.classList.remove('hidden');
    modal.classList.add('flex');
    modal.setAttribute('aria-hidden', 'false');

    // Smooth transition entry
    requestAnimationFrame(() => {
        backdrop?.classList.remove('opacity-0');
        backdrop?.classList.add('opacity-100');

        card?.classList.remove('opacity-0', 'scale-95', 'translate-y-4');
        card?.classList.add('opacity-100', 'scale-100', 'translate-y-0');
    });
}

export function closeAppModal() {
    const modal = document.getElementById('app-modal');
    const backdrop = document.getElementById('app-modal-backdrop');
    const card = document.getElementById('app-modal-card');

    if (!modal || modal.classList.contains('hidden')) return;

    // Smooth transition exit
    backdrop?.classList.remove('opacity-100');
    backdrop?.classList.add('opacity-0');

    card?.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
    card?.classList.add('opacity-0', 'scale-95', 'translate-y-4');

    setTimeout(() => {
        modal.classList.remove('flex');
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
    }, 300);
}

export function initModalModule() {
    // Global window exposure for inline trigger attributes
    window.openAppModal = openAppModal;
    window.closeAppModal = closeAppModal;

    // Delegate click listener for close buttons & backdrop
    document.addEventListener('click', (event) => {
        if (event.target.closest('[data-modal-close]') || event.target.id === 'app-modal-backdrop') {
            closeAppModal();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeAppModal();
        }
    });
}
