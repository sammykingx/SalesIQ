import { apiRequest } from '../../lib/http/api.js';

export function onboardingForm(endpointUrl = '') {
    return {
        // State
        currentStep: 0,
        submitting: false,
        completed: false,
        sameAsPersonalPhone: false,
        personalPhone: '',

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
            return this.formData.businessName.trim().length >= 2 &&
                this.formData.officialNumber.trim().length >= 7;
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

        async completeOnboarding() {
            if (this.submitting || !endpointUrl) return;
            this.submitting = true;

            // Clean up website URL format
            let website = this.formData.websiteUrl.trim();
            if (website && !/^https?:\/\//i.test(website)) {
                website = `https://${website}`;
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
                    website_url: website || null
                }
            };

            try {
                const response = await apiRequest(endpointUrl, 'POST', payload);

                // If request is successful, bypass parsing and complete right away
                if (response?.ok || response?.status === 'success') {
                    this.completed = true;
                    return;
                }

                // Otherwise, extract error body only when it fails
                const errorBody = (typeof response?.json === 'function')
                    ? await response.json().catch(() => null)
                    : response;

                this.completed = false;
                this.triggerToast(
                    errorBody?.message || 'An error occurred during onboarding.',
                    errorBody?.status || 'warning'
                );

            } catch (err) {
                this.completed = false;
                if (typeof this.triggerToast === 'function') {
                    this.triggerToast('Network error — please check your connection and try again.', 'warning');
                }
            } finally {
                this.submitting = false;
            }
        }
    };
}
