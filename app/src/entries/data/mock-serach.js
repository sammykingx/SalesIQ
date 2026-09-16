// Stand-in for a Django search endpoint. Shape matches what the real one should
// return: an array of { group, label, meta, href }. Swap this module out for
// remote-search.js (fetch-based) when the backend endpoint exists — nothing
// in search-dialog.js needs to change beyond the import.

import { demoCustomers } from "../customers/demo-data";
import { demoProductsData } from "../products/demo-data";

const invoices = [
    { id: 'INV-1042', customer: 'Acme Ltd', amount: '482.00' },
    { id: 'INV-1043', customer: 'Northwind Traders', amount: '129.50' },
    { id: 'INV-1091', customer: 'Acme Ltd', amount: '1,204.00' },
    { id: 'INV-2049', customer: 'Bright Retail Co', amount: '1,280.00' },
];

const customers = demoCustomers;
const products = demoProductsData;

function wait(ms, signal) {
    return new Promise((resolve, reject) => {
        const t = setTimeout(resolve, ms);
        signal?.addEventListener('abort', () => {
            clearTimeout(t);
            reject(new DOMException('Aborted', 'AbortError'));
        });
    });
}

export async function mockSearch(query, signal) {
    await wait(300, signal); // simulated network latency

    const q = query.toLowerCase();

    const invoiceHits = invoices
        .filter((inv) => inv.id.toLowerCase().includes(q) || inv.customer.toLowerCase().includes(q))
        .map((inv) => ({
            group: 'Invoices',
            label: `${inv.id} — ${inv.customer}`,
            meta: `₦${inv.amount}`,
            href: `/invoicing/${inv.id}/`,
        }));

    const customerHits = customers
        .filter((c) => {
            const firstName = c.firstName.toLowerCase();
            const lastName = c.lastName.toLowerCase();
            const email = c.email.toLowerCase();
            const phone = c.phone.toLowerCase();

            return (
                firstName.includes(q) ||
                lastName.includes(q) ||
                email.includes(q) ||
                phone.includes(q)
            );
        })
        .map((c) => ({
            group: 'Customers',
            label: `${c.firstName} ${c.lastName}`,
            meta: `Spent: $${c.spend.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} | Orders: ${c.totalOrders}`,
            href: `/customers/`,
        }));

    const productHits = products
        .filter((p) => {
            const name = p.name.toLowerCase();
            const productType = p.product_type.toLowerCase();
            return name.includes(q) || productType.includes(q);
        })
        .map((p) => {
            const totalRevenue = p.salesCount * p.price;
            return {
                group: 'Products',
                label: p.name,
                meta: `Revenue: ₦${totalRevenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} | Sales: ${p.salesCount}`,
                href: p.url,
            };
        });

    return [...invoiceHits, ...customerHits, ...productHits];
}

// When the real endpoint exists, the swap is exactly one file:
// create remote-search.js with the same
// export async function remoteSearch(query, signal) signature
// then change one import line and one call site in search-dialog.js (mockSearch → remoteSearch). 
// Nothing in the template or the rest of the component changes.
export async function remoteSearch(query, signal) {
    const res = await fetch(`/api/search/?q=${encodeURIComponent(query)}`, { signal });
    const data = await res.json();
    return data.results; // shape it server-side to match { group, label, meta, href }
}
