import "../styles/theme.css";
import "../styles/keyframes.css";
import Alpine from 'alpinejs';
import { apiRequest } from '../lib/http/index.js';

const TOAST_STYLES = {
    success: 'bg-success text-white',
    error: 'bg-red-600 text-white',
    warning: 'bg-amber-500 text-white',
};

/**
 * Alpine component for the coming-soon page.
 * Alpine owns UI state (toast, countdown display, form binding).
 * All backend communication goes through apiRequest() from lib/http.
 */
function comingSoon({ launchTimestamp, endpoint }) {
    return {
        // Waitlist form state
        email: '',
        submitting: false,
        endpoint,

        // Toast state
        toastMessage: '',
        toastType: 'success', // options success | error | warning
        showToast: false,

        // Countdown state
        targetDate: launchTimestamp,
        days: '00',
        hours: '00',
        minutes: '00',
        seconds: '00',

        init() {
            // Alpine calls init() automatically on component init — no x-init needed
            this.updateCountdown();
            setInterval(() => this.updateCountdown(), 1000);
        },

        updateCountdown() {
            const now = new Date().getTime();
            const distance = this.targetDate - now;

            if (distance < 0) {
                this.days = this.hours = this.minutes = this.seconds = '00';
                return;
            }

            this.days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
            this.hours = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
            this.minutes = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
            this.seconds = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');
        },

        get toastClasses() {
            return TOAST_STYLES[this.toastType] ?? TOAST_STYLES.success;
        },

        triggerToast(msg, type='success') {
            this.toastMessage = msg;
            this.toastType = type;
            this.showToast = true;
            setTimeout(() => { this.showToast = false; }, 4000);
        },

        async submitWaitlist() {
            if (!this.email) return;
            this.submitting = true;

            try {
                const response = await apiRequest(this.endpoint, 'POST', { email: this.email });

                if (response.ok) {
                    this.triggerToast('Thanks for subscribing! We will keep you updated.');
                    this.email = '';
                } else if (response.status === 403) {
                    this.triggerToast('Session expired — please refresh the page and try again.', 'warning');
                } else if (response.status >= 500) {
                    this.triggerToast('Something went wrong on our end. Please try again shortly.', 'error');
                } else {
                    const body = await response.json().catch(() => null);
                    this.triggerToast(body?.message ?? 'Something went wrong. Please try again.', 'error');
                }
            } catch (err) {
                // Network failure or a thrown validation error from apiRequest
                console.error('submitWaitlist failed:', err);
                this.triggerToast('Network error — please check your connection and try again.', 'warning');
            } finally {
                this.submitting = false;
            }
        },
    };
}

document.addEventListener('alpine:init', () => {
    const launchTimestamp = Number(document.body.dataset.launchTimestamp) * 1000;
    const endpoint = document.body.dataset.endpoint;
    
    Alpine.data('comingSoon', () => comingSoon({ launchTimestamp, endpoint }));
});

window.Alpine = Alpine;
Alpine.start();
