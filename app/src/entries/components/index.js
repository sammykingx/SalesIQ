import { initSidebarModule } from './sidebar.js';
import { initHeaderModule } from './header.js';
import { initSearchDialogModule } from './search-dialog.js';

export function initComponentsModule(Alpine) {
    initSidebarModule(Alpine);
    initHeaderModule(Alpine);
    initSearchDialogModule(Alpine);
}