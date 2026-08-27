// Stand-in for a Django search endpoint. Shape matches what the real one should
// return: an array of { group, label, meta, href }. Swap this module out for
// remote-search.js (fetch-based) when the backend endpoint exists — nothing
// in search-dialog.js needs to change beyond the import.

const invoices = [
    { id: 'INV-1042', customer: 'Acme Ltd', amount: '482.00' },
    { id: 'INV-1043', customer: 'Northwind Traders', amount: '129.50' },
    { id: 'INV-1091', customer: 'Acme Ltd', amount: '1,204.00' },
    { id: 'INV-2049', customer: 'Bright Retail Co', amount: '1,280.00' },
];

const customers = [
    { id: 'CUST-104', name: 'Jane Doe', email: 'jane@acme.com' },
    { id: 'CUST-118', name: 'Kwame Mensah', email: 'kwame@northwind.co' },
    { id: 'CUST-201', name: 'Priya Nair', email: 'priya@brightretail.com' },
];

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
            meta: `$${inv.amount}`,
            href: `/invoicing/${inv.id}/`,
        }));

    const customerHits = customers
        .filter((c) => c.id.toLowerCase().includes(q) || c.name.toLowerCase().includes(q) || c.email.toLowerCase().includes(q))
        .map((c) => ({
            group: 'Customers',
            label: c.name,
            meta: c.email,
            href: `/customers/${c.id}/`,
        }));

    return [...invoiceHits, ...customerHits];
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
