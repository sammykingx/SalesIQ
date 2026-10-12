import { apiRequest } from '../../lib/http/api.js';

export function onboardingForm(endpointUrl = '') {
    return {
        // State
        currentStep: 0,
        submitting: false,
        completed: false,
        sameAsPersonalPhone: false,
        personalPhone: '',
        backendErrors: {},

        // Form Model
        formData: {
            businessName: '',
            officialNumber: '',
            businessType: '', // 'online' | 'physical' | 'both'
            address: '',
            instagram: '',
            tiktok: '',
            websiteUrl: ''
        },

        sanitizePhoneNumber(event) {
            let value = event.target.value;
            value = value.replace(/(?!^\+)[^\d]/g, '');
            if (value.startsWith('+')) {
                value = '+' + value.slice(1).replace(/\D/g, '');
            } else {
                value = value.replace(/\D/g, '');
            }
            this.formData.officialNumber = value;
        },

        toggleSamePhone() {
            if (this.sameAsPersonalPhone) {
                this.formData.officialNumber = this.personalPhone;
            }
        },

        get isStep1Valid() {
            return this.formData.businessName.trim().length >= 5 &&
                this.formData.businessName.trim().length <= 45 &&
                this.formData.officialNumber.trim().length >= 11 &&
                this.formData.officialNumber.trim().length <= 17;
        },

        get isStep2Valid() {
            if (!this.formData.businessType) return false;
            if (this.formData.businessType === 'online') return true;
            return this.formData.address.trim().length >= 5;
        },

        get isStep3Valid() {
            if (!this.formData.websiteUrl.trim()) return true;
            try {
                const url = this.formData.websiteUrl.startsWith('http')
                    ? this.formData.websiteUrl
                    : 'https://' + this.formData.websiteUrl;
                new URL(url);
                return true;
            } catch (_) {
                return false;
            }
        },

        nextStep() {
            if (this.currentStep === 1 && !this.isStep1Valid) return;
            if (this.currentStep === 2 && !this.isStep2Valid) return;
            if (this.currentStep === 3 && !this.isStep3Valid) return;
            if (this.currentStep < 4) {
                this.currentStep++;
            }
        },

        prevStep() {
            if (this.currentStep > 0 && !this.submitting) {
                this.currentStep--;
            }
        },

        formatFriendlyError(field, type) {
            if (field === 'business_name') {
                if (type === 'string_too_long') return 'Your business name is too long. Please keep it under 45 characters.';
                if (type === 'string_too_short') return 'Your business name is too short. Please use at least 2 characters.';
                if (type === 'missing') return 'Please provide your business name.';
            }
            if (field === 'phone_number') {
                if (type === 'string_too_long') return 'Your phone number is too long. Please keep it under 17 digits.';
                if (type === 'string_too_short') return 'Please enter a valid phone number with at least 11 digits.';
                if (type === 'missing') return 'Official phone number is required.';
            }
            if (field === 'address') {
                if (type === 'string_too_short') return 'Please provide a complete physical address for your store.';
            }

            // Clean fallback if any slips through
            return 'Please review this field and correct the data.';
        },

        async completeOnboarding() {
            if (this.submitting || !endpointUrl) return;
            this.submitting = true;

            // Clean up website URL format
            let website = this.formData.websiteUrl.trim();
            try {
                const fullUrl = /^https?:\/\//i.test(website) ? website : `https://${website}`;
                const parsedUrl = new URL(fullUrl);
                let hostname = parsedUrl.hostname;

                if (hostname.startsWith('www.')) {
                    hostname = hostname.slice(4);
                }

                website = hostname;
            } catch (_) {
                website = null;
            }

            // Format social handles safely
            const cleanHandle = (val) => val ? `@${val.trim().replace(/^@/, '')}` : null;

            const payload = {
                business_name: this.formData.businessName.trim(),
                phone_number: this.formData.officialNumber.trim(),
                business_type: this.formData.businessType,
                address: this.formData.businessType === 'online' ? null : this.formData.address.trim(),
                socials: {
                    instagram_url: cleanHandle(this.formData.instagram),
                    tiktok_url: cleanHandle(this.formData.tiktok),
                    website_url: website,
                }
            };

            try {
                const response = await apiRequest(endpointUrl, 'POST', payload);
                if (response?.ok || response?.status === 'success') {
                    this.completed = true;
                    return;
                }

                const errorBody = await response.json().catch(() => { });

                this.completed = false;

                if (errorBody?.errors) {
                    if (Array.isArray(errorBody?.errors)) {
                        errorBody.errors.forEach(err => {
                            const field = err.field;
                            const type = err.type;
                            const rawMessage = err.message;

                            if (field) {
                                this.backendErrors[field] = this.formatFriendlyError(field, type);
                            }
                        });
                    }
                }

                this.triggerToast(
                    errorBody?.title || 'Check Your Input',
                    errorBody?.message || 'An error occurred during onboarding.',
                    errorBody?.status || 'warning'
                );

            } catch (err) {
                this.completed = false;
                this.triggerToast('Network error', 'please check your connection and try again.', 'warning');
            } finally {
                this.submitting = false;
            }
        }
    };
}
