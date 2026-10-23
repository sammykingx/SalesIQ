import { invoiceShareComponent } from './share-component.js';

export function initInvoicesModule(Alpine) {
    Alpine.data('invoiceShare', invoiceShareComponent);
}
