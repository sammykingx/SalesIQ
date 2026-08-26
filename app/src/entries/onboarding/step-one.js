export const step1 = {
    validate(data) {
        return data.businessName?.trim().length >= 2 && data.officialNumber?.trim().length >= 7;
    },
    mutate(payload, data) {
        payload.business_name = data.businessName.trim();
        payload.official_number = data.officialNumber.trim();
    }
};