export const step3 = {
    validate(formData) {
        if (!formData.websiteUrl.trim()) return true;
        try {
            const url = formData.websiteUrl.startsWith('http')
                ? formData.websiteUrl
                : 'https://' + formData.websiteUrl;
            new URL(url);
            return true;
        } catch (_) {
            return false;
        }
    },
    mutate(payload, formData) {
        let formattedUrl = formData.websiteUrl.trim();
        if (formattedUrl && !formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
            formattedUrl = 'https://' + formattedUrl;
        }

        payload.socials.instagram = formData.instagram.trim() ? `@${formData.instagram.replace(/^@/, '')}` : null;
        payload.socials.tiktok = formData.tiktok.trim() ? `@${formData.tiktok.replace(/^@/, '')}` : null;
        payload.socials.website = formattedUrl || null;
    }
};
