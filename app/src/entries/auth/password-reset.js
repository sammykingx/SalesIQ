import { isEmailValid } from '../../lib/auth/alpine-helpers.js';
import { apiRequest } from '../../lib/http/api.js';
import { showToast } from '../../lib/toast.js';

export function passwordResetForm(endpointUrl = '') {
    return {
        endpoint: endpointUrl,
        submitting: false,
        email: '',

        get isEmailValid() {
            return isEmailValid(this.email);
        },

        async handleSubmit() {
            if (!this.isEmailValid || this.submitting) return;
            this.submitting = true;

            try {
                const payload = { email: this.email.trim() };
                const response = await apiRequest(this.endpoint, 'POST', payload);

                const body = await response.json().catch(() => null);

                if (response.ok || (body && body.status === 'success')) {
                    showToast(
                        body?.msg || body?.message || 'Password reset link has been sent to your email address.',
                        body?.status || 'info'
                    );
                    this.email = '';
                } else {
                    showToast(
                        body?.error || body?.msg || 'Unable to process your request. Please check the email address.',
                        'error'
                    );
                }
            } catch (err) {
                console.error('Password reset error:', err);
                showToast('Network error — please check your connection and try again.', 'warning');
            } finally {
                this.submitting = false;
            }
        }
    };
}