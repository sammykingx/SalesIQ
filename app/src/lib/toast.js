/**
 * Global Toast Dispatcher
 * @param {string} message - Message text to display
 * @param {'success' | 'error' | 'warning' | 'info'} type - Notification style type
 */
export function showToast(message, type = 'success') {
    window.dispatchEvent(
        new CustomEvent('toast', {
            detail: { message, type },
            bubbles: true
        })
    );
}
