import { inAppToast } from "../../lib/in-app-toast";
import { getCsrfToken } from '../../lib/http/csrf.js';

let cachedDataPromise = null;

function getEndpoint() {
    const el = document.getElementById('globalBusinessSearch');
    const endpoint = el?.dataset?.endpoint;
    if (!endpoint) {
        inAppToast(
            'Initialization Error',
            'Business Search engine configuration is incomplete: missing required attribute.',
            'error'
        );
        throw new Error('globalBusinessSearch: missing data-endpoint attribute');
    }
    return endpoint;
}

function fetchBusinessData(signal) {
    if (!cachedDataPromise) {
        cachedDataPromise = fetch(getEndpoint(), {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            signal,
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`Business data request failed: ${res.status}`);
                }
                return res.json();
            })
            .catch((err) => {
                // let the next search retry instead of caching a failure
                cachedDataPromise = null;
                throw err;
            });
    }
    return cachedDataPromise;
}

function money(amount) {
    return Number(amount || 0).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

export async function remoteSearch(query, signal) {
    const data = await fetchBusinessData(signal);
    if (signal?.aborted) throw new DOMException('Aborted', 'AbortError');

    const q = query.toLowerCase();

    const invoiceHits = (data.invoice_json || [])
        .filter((inv) => {
            const id = (inv.display_id || '').toLowerCase();
            const name = `${inv.customer?.first_name || ''} ${inv.customer?.last_name || ''}`.toLowerCase();
            const email = (inv.customer?.email || '').toLowerCase();
            return id.includes(q) || name.includes(q) || email.includes(q);
        })
        .map((inv) => ({
            group: 'Invoices',
            label: `${inv.display_id} — ${inv.customer?.first_name} ${inv.customer?.last_name}`,
            meta: `₦${money(inv.total)}`,
            href: inv.url,
        }));

    const customerHits = (data.customers_json || [])
        .filter((c) => {
            const first = (c.first_name || '').toLowerCase();
            const last = (c.last_name || '').toLowerCase();
            const email = (c.email || '').toLowerCase();
            const phone = (c.phone || '').toLowerCase();
            return first.includes(q) || last.includes(q) || email.includes(q) || phone.includes(q);
        })
        .map((c) => ({
            group: 'Customers',
            label: c.display_name || `${c.first_name} ${c.last_name}`,
            meta: `Spent: ₦${money(c.total_spend)} | Orders: ${c.total_orders}`,
            href: `/customers/`,
        }));

    const productHits = (data.products_json || [])
        .filter((p) => {
            const name = (p.name || '').toLowerCase();
            const type = (p.product_type || '').toLowerCase();
            return name.includes(q) || type.includes(q);
        })
        .map((p) => {
            const revenue = Number(p.price || 0) * Number(p.total_sales || 0);
            return {
                group: 'Products',
                label: p.name,
                meta: `Revenue: ₦${money(revenue)} | Sales: ${p.total_sales}`,
                href: p.url,
            };
        });

    return [...invoiceHits, ...customerHits, ...productHits];
}
