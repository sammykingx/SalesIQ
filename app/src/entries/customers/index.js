// app/src/entries/customers/index.js
import { addCustomerModal } from "./add-customers.js";
import { allCustomersComponent } from "./all-customers.js";

export function initCustomerModule(Alpine) {
    Alpine.data('addCustomerModal', addCustomerModal);
    Alpine.data('allCustomersComponent', allCustomersComponent);
}
