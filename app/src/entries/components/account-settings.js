export function initAccountSettingsModule(Alpine) {
    Alpine.data('accountSettingsManager', () => ({
        activeTab: (() => {
            const hash = window.location.hash.replace('#', '');
            const validTabs = ['profile', 'update-password', 'socials',];

            return validTabs.includes(hash) ? hash : 'profile';
        })(),

        setTab(tabName) {
            this.activeTab = tabName;
            window.location.hash = tabName;
        }
    }));
}
