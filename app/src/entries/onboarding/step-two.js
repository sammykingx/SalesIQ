export const step2 = {
    validate(data) {
        if (!data.businessType) return false;
        if (data.businessType === 'online') return true;
        return data.address?.trim().length >= 5;
    },
    mutate(payload, data) {
        payload.business_type = data.businessType;
        payload.address = data.businessType === 'online' ? null : data.address.trim();
    }
};