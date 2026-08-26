import { apiRequest } from '../../lib/http/api.js';
import { payload } from './payload.js';
import { step1 } from './step-one.js';
import { step2 } from './step-two.js';
import { step3 } from './step-three.js';

export class OnboardingManager {
    constructor(endpoint) {
        this.endpoint = endpoint || '/api/v1/onboarding/business/';
        this.payload = payload;
        this.steps = {
            1: step1,
            2: step2,
            3: step3
        };
    }

    isStepValid(stepNumber, formData) {
        const step = this.steps[stepNumber];
        return step ? step.validate(formData) : true;
    }

    processStep(stepNumber, formData) {
        const step = this.steps[stepNumber];
        if (step) {
            step.mutate(this.payload, formData);
        }
    }

    async complete(toastCallback) {
        try {
            const response = await apiRequest(this.endpoint, {
                method: 'POST',
                body: JSON.stringify(this.payload)
            });
            if (typeof toastCallback === 'function') {
                toastCallback('Business profile successfully setup!', 'success');
            }
            return response;
        } catch (error) {
            if (typeof toastCallback === 'function') {
                toastCallback(error.message || 'Failed to complete setup.', 'error');
            }
            throw error;
        }
    }
}
