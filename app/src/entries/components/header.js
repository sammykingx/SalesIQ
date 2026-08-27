export function initHeaderModule(Alpine) {
    // Shared UI state used by the language switcher (both the lg+ dropdown and the mobile "More" menu)
    Alpine.store('ax', {
        lang: 'EN',
        setLang(code) {
            this.lang = code;
        },
    });

    // Generic dropdown behavior — reused by language, apps, cart, notifications, profile, and "More"
    Alpine.data('axDropdown', () => ({
        open: false,
        toggle() {
            this.open = !this.open;
        },
        close() {
            this.open = false;
        },
    }));

    Alpine.data('axHeader', () => ({
        theme: 'light',

        init() {
            const stored = localStorage.getItem('vireo-theme');
            this.theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
            document.documentElement.classList.toggle('dark', this.theme === 'dark');
        },

        toggleTheme() {
            this.theme = this.theme === 'dark' ? 'light' : 'dark';
            document.documentElement.classList.toggle('dark', this.theme === 'dark');
            localStorage.setItem('vireo-theme', this.theme);
        },
    }));
}
