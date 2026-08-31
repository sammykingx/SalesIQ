import { createPasswordValidationState } from '../../lib/auth/alpine-helpers.js';
import { apiRequest } from '../../lib/http/api.js';
import { showToast } from '../../lib/toast.js';

export function passwordChangeForm(endpointUrl = '') {
    return {
        endpoint: endpointUrl,
        submitting: false,
        showPassword: false,
        showConfirmPassword: false,
        form: {
            password: '',
            confirm_password: ''
        },

        // Delegate password validation rules & getters using the helper state
        get passwordState() {
            return createPasswordValidationState(
                () => this.form.password,
                () => this.form.confirm_password
            );
        },
        get passwordRules() {
            return this.passwordState.passwordRules;
        },
        get isPasswordValid() {
            return this.passwordState.isPasswordValid;
        },
        get doPasswordsMatch() {
            return this.passwordState.doPasswordsMatch;
        },
        get isFormValid() {
            return this.isPasswordValid && this.doPasswordsMatch;
        },

        async handleSubmit() {
            if (!this.isFormValid || this.submitting) return;
            this.submitting = true;

            try {
                const response = await apiRequest(this.endpoint, 'POST', this.form);
                const body = await response.json().catch(() => null);
                console.log(JSON.stringify(response, null, 2));

                if (response.ok || (body && body.status === 'success')) {
                    showToast(
                        body?.message || 'Your password has been changed successfully.',
                        body?.status || 'success'
                    );
                    this.form.password = '';
                    this.form.confirm_password = '';

                    if (body?.redirect && body?.url) {
                        setTimeout(() => {
                            window.location.assign(body.url);
                        }, 2300);
                    }
                } else {
                    showToast(
                        body?.message || 'Failed to change password. Please ensure requirements are met.',
                        body?.status || 'error'
                    );
                }
            } catch (err) {
                showToast('Network error — please check your connection and try again.', 'warning');
            } finally {
                this.submitting = false;
            }
        }
    };
}