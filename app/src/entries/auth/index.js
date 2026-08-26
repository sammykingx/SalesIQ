import { signUpForm } from './signup.js';
import { passwordResetForm } from './password-reset.js';
import { passwordChangeForm } from './password-change.js';

export function initAuthModule(Alpine) {
    Alpine.data('signUpForm', signUpForm);
    Alpine.data('passwordResetForm', passwordResetForm);
    Alpine.data('passwordChangeForm', passwordChangeForm);
}
