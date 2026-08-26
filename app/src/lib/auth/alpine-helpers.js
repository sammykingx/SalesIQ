import { isEmailValid, evaluatePassword, doPasswordsMatch } from './validators.js';

export const createPasswordValidationState = (getPassword, getConfirmPassword = null) => {
    return {
        get passwordRules() {
            return evaluatePassword(getPassword());
        },
        get isPasswordValid() {
            return this.passwordRules.isValid;
        },
        get doPasswordsMatch() {
            if (typeof getConfirmPassword !== 'function') return true;
            return doPasswordsMatch(getPassword(), getConfirmPassword());
        }
    };
};

export { isEmailValid };
