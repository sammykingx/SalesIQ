import { recordSaleComponent } from './record-sales.js';
import { listSalesComponent } from './list-sales.js';

export function initSalesModule(Alpine) {
    Alpine.data('recordSaleComponent', recordSaleComponent);
    Alpine.data('listSalesComponent', listSalesComponent);
}
