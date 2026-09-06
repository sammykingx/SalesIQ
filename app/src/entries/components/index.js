// app/entires/components/index.js

import { initSidebarModule } from './sidebar.js';
import { initHeaderModule } from './header.js';
import { initSearchDialogModule } from './search-dialog.js';
import { initModalModule } from './modal.js';

export function initComponentsModule(Alpine) {
    initSidebarModule(Alpine);
    initHeaderModule(Alpine);
    initSearchDialogModule(Alpine);
    initModalModule(Alpine);
}
