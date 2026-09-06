import { apiRequest } from '../../lib/http/api.js';
import { evaluatePassword, doPasswordsMatch } from '../../lib/auth/validators.js';
import { inAppToast } from "../../lib/in-app-toast.js";
/**
 * Personal Profile Form Component
 */
export function profileSettings() {
    return {
        phoneNumber: '',
        userTimezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
        userLanguage: (navigator.language || navigator.userLanguage || 'en-US').toUpperCase(),
        isSubmitting: false,

        init() {
            const phoneInput = this.$el.querySelector('[name="phone_number"]');
            if (phoneInput) {
                // Sanitize initial server value on mount
                this.phoneNumber = phoneInput.value.replace(/[^0-9+]/g, '');
            }
        },

        handlePhoneInput(event) {
            // Strip any character that is not a digit or a '+' symbol
            const sanitized = event.target.value.replace(/[^0-9+]/g, '');
            this.phoneNumber = sanitized;
            event.target.value = sanitized;
        },

        get isValidPhone() {
            // Must contain only digits and '+' and meet the 11-character minimum limit
            return /^[0-9+]+$/.test(this.phoneNumber) && this.phoneNumber.length >= 11;
        },

        get isValidForm() {
            return this.isValidPhone && !this.isSubmitting;
        },

        async submitProfile(event) {
            if (!this.isValidForm) return;

            const form = event.target;
            const endpoint = form.getAttribute('action') || window.location.pathname;

            const payload = {
                phone_number: this.phoneNumber,
            };

            this.isSubmitting = true;
            try {
                const response = await apiRequest(endpoint, 'PATCH', payload);
                if (response && !response.ok) {
                    inAppToast(
                        "Update Blocked 🚧",
                        "Your profile update didn't go through. Double-check your details and try again.",
                        "warning",
                    );
                    return;
                }
                inAppToast("Looks Sharp! ✨", "Your profile just got a glow-up.");
            } catch (error) {
                if (!navigator.onLine || error.message?.includes('network')) {
                    inAppToast("Ghost Signal 👻", "The internet gremlins stole your request. Check your connection!", "info");
                } else {
                    inAppToast("Plot Twist! 🛑", "That didn't quite work. Blame our servers, not you.", "error");
                }
            } finally {
                this.isSubmitting = false;
            }
        }
    };
}

/**
 * Password & Security Component
 */
export function updatePasswordSettings(targetTimestamp = 0) {
    return {
        newPassword: '',
        confirmPassword: '',
        showNewPass: false,
        showConfirmPass: false,
        cooldownSeconds: 0,
        cooldownActive: false,
        isSubmitting: false,

        init() {
            const target = Number(targetTimestamp) || 0;
            const currentTimestamp = Math.floor(Date.now() / 1000);

            if (target > currentTimestamp) {
                this.cooldownSeconds = target - currentTimestamp;
                this.cooldownActive = true;
                this.startCooldownTimer();
            }
        },

        startCooldownTimer() {
            const interval = setInterval(() => {
                if (this.cooldownSeconds > 0) {
                    this.cooldownSeconds--;
                } else {
                    this.cooldownActive = false;
                    clearInterval(interval);
                }
            }, 1000);
        },

        get passwordEvaluation() {
            return evaluatePassword(this.newPassword);
        },
        get hasMinLength() { return this.passwordEvaluation.hasMinLength; },
        get hasLowercase() { return this.passwordEvaluation.hasLower; },
        get hasUppercase() { return this.passwordEvaluation.hasUpper; },
        get hasNumber() { return this.passwordEvaluation.hasNumber; },
        get hasSpecial() { return this.passwordEvaluation.hasSpecial; },
        get isMatch() { return doPasswordsMatch(this.newPassword, this.confirmPassword); },
        get isValidForm() {
            return this.passwordEvaluation.isValid && this.isMatch && !this.cooldownActive;
        },

        async submitPassword(event) {
            if (!this.isValidForm) return;

            const form = event.target;
            const endpoint = form.getAttribute('action') || window.location.pathname;
            const payload = {
                password: this.newPassword,
                confirm_password: this.confirmPassword
            };

            this.isSubmitting = true;
            try {
                const response = await apiRequest(endpoint, 'PATCH', payload);
                this.newPassword = '';
                this.confirmPassword = '';

                if (response && !response.ok) {
                    inAppToast("Update Failed 🔒", "Your password update didn't go through. Check your entries and try again.", "warning");
                    return;
                }
                inAppToast("Password Updated! 🛡️", "Your new password is locked in and secure.");
                
            } catch (error) {
                if (!navigator.onLine || error.message?.includes('network')) {
                    inAppToast("Ghost Signal 👻", "The internet gremlins stole your request. Check your connection!", "info");
                } else {
                    inAppToast("Plot Twist! 🛑", "That didn't quite work. Blame our servers, not you.", "error");
                }
            } finally {
                this.isSubmitting = false;
            }
        }
    };
}

/**
 * Social Links Form Component
 */
export function socialsSettings(initialData = {}) {
    return {
        websiteUrl: initialData.websiteUrl || '',
        instagramHandle: initialData.instagramHandle || '',
        tiktokHandle: initialData.tiktokHandle || '',
        whatsappNumber: initialData.whatsappNumber || '',
        twitterHandle: initialData.twitterHandle || '',
        isSubmitting: false,

        async submitSocials(event) {
            const form = event.target;
            const endpoint = form.getAttribute('action') || window.location.pathname;
            const payload = {
                website_url: this.websiteUrl,
                instagram_url: this.instagramHandle,
                tiktok_url: this.tiktokHandle,
                whatsapp_number: this.whatsappNumber,
                twitter_url: this.twitterHandle
            };

            this.isSubmitting = true;
            try {
                const response = await apiRequest(endpoint, 'PATCH', payload);
                if (response && !response.ok) {
                    inAppToast("Update Failed 🔗", "Your social links update didn't go through. Check your URLs and try again.");
                    return;
                }

                inAppToast("Connected! 🌐", "Your social links are live and ready to click.");
            } catch (error) {
                if (!navigator.onLine || error.message?.includes('network')) {
                    inAppToast("Ghost Signal 👻", "The internet gremlins stole your request. Check your connection!", "info");
                } else {
                    inAppToast("Plot Twist! 🛑", "That didn't quite work. Blame our servers, not you.", "error");
                }
            } finally {
                this.isSubmitting = false;
            }
        }
    };
}
