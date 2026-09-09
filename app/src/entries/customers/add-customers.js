// app/src/entries/customers/add-customers.js
import { apiRequest } from '../../lib/http/api.js';
import { isNameValid, isPhoneValid, sanitizePhoneInput } from '../../lib/validators.js';
import { isEmailValid } from '../../lib/auth/validators.js';
import { inAppToast } from '../../lib/in-app-toast.js';
import { closeAppModal } from '../components/modal.js';

export function addCustomerModal(endpointUrl = '') {
    return {
        firstName: '',
        lastName: '',
        customDisplayName: '',
        email: '',
        phone: '',
        loading: false,
        errorMessage: '',

        get computedDisplayName() {
            if (this.customDisplayName.trim().length > 0) {
                return this.customDisplayName;
            }
            const capitalize = (str) => str ? str.trim().charAt(0).toUpperCase() + str.trim().slice(1).toLowerCase() : '';

            const first = capitalize(this.firstName);
            const last = capitalize(this.lastName);
            const full = `${first} ${last}`.trim();
            return full || 'Customer Name';
        },

        get isFirstNameValid() {
            return isNameValid(this.firstName);
        },
        get isLastNameValid() {
            return isNameValid(this.lastName);
        },
        get isEmailValid() {
            return isEmailValid(this.email);
        },
        get isPhoneValid() {
            return isPhoneValid(this.phone);
        },
        get isFormValid() {
            return this.isFirstNameValid && this.isLastNameValid && this.isEmailValid && this.isPhoneValid;
        },

        resetForm() {
            this.firstName = '';
            this.lastName = '';
            this.customDisplayName = '';
            this.email = '';
            this.phone = '';
            this.errorMessage = '';
        },

        handlePhoneInput(e) {
            this.phone = sanitizePhoneInput(e.target.value);
        },

        async handleSubmit() {
            if (!this.isFormValid || this.loading) return;

            this.loading = true;
            this.errorMessage = '';

            const payload = {
                first_name: this.firstName.trim(),
                last_name: this.lastName.trim(),
                display_name: this.computedDisplayName,
                email: this.email.trim(),
                phone_number: this.phone.trim()
            };

            try {
                const response = await apiRequest(endpointUrl, 'POST', payload);
                const data = await response.json().catch(() => ({}));
                if (!response.ok) {
                    if (response.status === 422) {
                        const errorDetails = Array.isArray(data.error)
                            ? data.error.map(err => {
                                const formattedField = err.field
                                    ? err.field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                                    : 'Field';
                                return `${formattedField}: ${err.message}`;
                            }).join(' | ')
                            : (data.error || '')

                        inAppToast(
                            'Customer Identity Rejected 🚫',
                            `${data.message}`,
                            'warning',
                            4500
                        );
                    } else {
                        inAppToast('Ecosystem Glitch ⚠️', data.message || 'An unexpected error occurred.', 'error');
                    }
                    return;
                }
                this.resetForm();
                inAppToast('Added to the fold ✨', data.message || 'Customer successfully added!', 'success', 4700);
                closeAppModal();
            } catch (err) {
                inAppToast('Connection Void 🌪️', err.message || 'Failed to reach the server. Check your network connection.', 'error');
            } finally {
                this.loading = false;
            }
        }
    };
}
