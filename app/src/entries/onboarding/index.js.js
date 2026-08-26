import { OnboardingManager } from './manager.js';

// window.Alpine?.data('onboardingFlow', (config = {}) => {
//     const manager = new OnboardingManager(config.endpoint);

//     return {
//         manager,
//         currentStep: 0,
//         submitting: false,
//         completed: false,

//         formData: {
//             businessName: '',
//             officialNumber: '',
//             businessType: '',
//             address: '',
//             instagram: '',
//             tiktok: '',
//             websiteUrl: ''
//         },

//         get isStep1Valid() { return manager.isStepValid(1, this.formData); },
//         get isStep2Valid() { return manager.isStepValid(2, this.formData); },
//         get isStep3Valid() { return manager.isStep3Valid(3, this.formData); },

//         nextStep() {
//             if (this.currentStep === 1 && !this.isStep1Valid) return;
//             if (this.currentStep === 2 && !this.isStep2Valid) return;
//             if (this.currentStep === 3 && !this.isStep3Valid) return;

//             if (this.currentStep >= 1 && this.currentStep <= 3) {
//                 manager.processStep(this.currentStep, this.formData);
//             }

//             if (this.currentStep < 4) {
//                 this.currentStep++;
//             }
//         },

//         prevStep() {
//             if (this.currentStep > 0 && !this.submitting) {
//                 this.currentStep--;
//             }
//         },

//         async completeOnboarding() {
//             this.submitting = true;
//             try {
//                 const toast = typeof this.triggerToast === 'function' ? this.triggerToast.bind(this) : null;
//                 await manager.complete(toast);
//                 this.completed = true;
//             } finally {
//                 this.submitting = false;
//             }
//         }
//     };
// });
console.log("hello");