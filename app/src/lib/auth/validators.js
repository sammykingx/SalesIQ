// app/src/lib/auth/validators.js
/**
 * Shared authentication validation utilities
 */

export const isEmailValid = (email = '') => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
};

export const evaluatePassword = (password = '') => {
    const hasMinLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    const isValid = hasMinLength && hasUpper && hasLower && hasNumber && hasSpecial;

    return {
        hasMinLength,
        hasUpper,
        hasLower,
        hasNumber,
        hasSpecial,
        isValid
    };
};

export const doPasswordsMatch = (password = '', confirmPassword = '') => {
    return password === confirmPassword && confirmPassword.length > 0;
};
