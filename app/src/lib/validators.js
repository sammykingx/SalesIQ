// app/src/lib/validators.js

// Validates names: min 3 chars, alphabets, spaces, and '!' only

export const isNameValid = (name = '') => {
    const trimmed = name.trim();
    if (trimmed.length < 3) return false;
    return /^[A-Za-z\s!]+$/.test(name);
};

// Validates phone number: Optional leading '+', only digits, min 11 digits
export const isPhoneValid = (phone = '') => {
    const digitsOnly = phone.replace(/\D/g, '');
    if (digitsOnly.length < 11) return false;
    // Ensure '+' can only appear as the first character
    return /^\+?[0-9]{11,}$/.test(phone.trim());
};

// Formats phone input live to restrict multiple '+' or non-digit characters
export const sanitizePhoneInput = (val = '') => {
    let cleaned = val.replace(/[^\d+]/g, '');
    if (cleaned.startsWith('+')) {
        return '+' + cleaned.slice(1).replace(/\+/g, '');
    }
    return cleaned.replace(/\+/g, '');
};
