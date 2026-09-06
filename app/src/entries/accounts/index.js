// app/src/entries/accounts/index.js
import { profileSettings, updatePasswordSettings, socialsSettings } from './settings.js';

export function initAccountsModule(Alpine) {
    Alpine.data('profileSettings', profileSettings);
    Alpine.data('securitySettings', updatePasswordSettings);
    Alpine.data('socialsSettings', socialsSettings);
}
