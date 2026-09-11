import { recordSaleComponent } from './record-sales.js';

export function initSalesModule(Alpine) {
    Alpine.data('recordSaleComponent', recordSaleComponent);
}
