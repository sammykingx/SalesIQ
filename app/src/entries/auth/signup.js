import { createPasswordValidationState, isEmailValid } from '../../lib/auth/alpine-helpers.js';
import { apiRequest } from '../../lib/http/api.js';
import { showToast } from '../../lib/toast.js';

export function signUpForm(endpointUrl = '') {
    return {
        endpoint: endpointUrl,
        submitting: false,
        showPassword: false,
        showConfirmPassword: false,
        prevValid: false,
        form: {
            first_name: '',
            last_name: '',
            email: '',
            password: '',
            confirm_password: ''
        },

        get isFirstNameValid() {
            const name = this.form.first_name.trim();
            return name.length >= 2 && /^[A-Za-z\s'-]+$/.test(name);
        },
        get isLastNameValid() {
            const name = this.form.last_name.trim();
            return name.length >= 2 && /^[A-Za-z\s'-]+$/.test(name);
        },

        get isEmailValid() {
            return isEmailValid(this.form.email);
        },

        // Password helper state
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
            return (
                this.isFirstNameValid &&
                this.isLastNameValid &&
                this.isEmailValid &&
                this.isPasswordValid &&
                this.doPasswordsMatch
            );
        },

        async handleSubmit() {
            if (!this.isFormValid || this.submitting) return;
            this.submitting = true;

            try {
                const response = await apiRequest(this.endpoint, 'POST', this.form);
                const body = await response.json().catch(() => null);

                if (response.ok || (body && body.status === 'success')) {
                    showToast(
                        body?.message || "Account created successfully!",
                        body?.status || "success"
                    );

                    if (body?.redirect && body?.url) {
                        setTimeout(() => {
                            window.location.assign(body.url);
                        }, 1700)
                    }
                } else {
                    showToast(
                        body?.error || body?.message || "Something went wrong. Please check your data.",
                        "error"
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

