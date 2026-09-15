// app/src/entries/sales/list-sales.js
import { inAppToast } from "../../lib/in-app-toast.js";


function loadInitialData(scriptId, fallbackData = []) {
    const scriptElement = document.getElementById(scriptId);
    if (scriptElement && scriptElement.textContent.trim()) {
        try {
            const parsed = JSON.parse(scriptElement.textContent);
            if (Array.isArray(parsed)) {
                return parsed;
            }
        } catch (e) {
            inAppToast('Initialization Error', 'We tried to read the data, but it spoke in hieroglyphics instead.', 'error');
        }
    }
    return fallbackData;
}

export function listSalesComponent() {
    return {
        sales: [],
        searchQuery: '',
        statusFilter: 'all',
        sortBy: 'created_at',
        sortOrder: 'desc',
        currentPage: 1,
        pageSize: 7,

        init() {
            this.sales = loadInitialData('invoices_data', []);
        },

        get hasNoTransactions() {
            return this.sales.length === 0;
        },

        get filteredSales() {
            let result = [...this.sales];

            // 1. Search filter: display_id, customer name, customer email
            if (this.searchQuery.trim()) {
                const q = this.searchQuery.toLowerCase();
                result = result.filter(item => {
                    const displayId = (item.display_id || '').toLowerCase();
                    const firstName = (item.customer?.first_name || '').toLowerCase();
                    const lastName = (item.customer?.last_name || '').toLowerCase();
                    const fullName = `${firstName} ${lastName}`.trim();
                    const email = (item.customer?.email || '').toLowerCase();

                    return displayId.includes(q) || fullName.includes(q) || email.includes(q);
                });
            }

            // 2. Status filter
            if (this.statusFilter !== 'all') {
                result = result.filter(item =>
                    (item.status || '').toLowerCase() === this.statusFilter.toLowerCase()
                );
            }

            // 3. Sorting (Date created, sale total amount, client name)
            result.sort((a, b) => {
                let valA, valB;

                if (this.sortBy === 'created_at') {
                    valA = new Date(a.created_at || 0).getTime();
                    valB = new Date(b.created_at || 0).getTime();
                } else if (this.sortBy === 'amount') {
                    valA = parseFloat(a.total) || 0;
                    valB = parseFloat(b.total) || 0;
                } else if (this.sortBy === 'client') {
                    valA = `${a.customer?.first_name || ''} ${a.customer?.last_name || ''}`.toLowerCase();
                    valB = `${b.customer?.first_name || ''} ${b.customer?.last_name || ''}`.toLowerCase();
                }

                if (valA < valB) return this.sortOrder === 'asc' ? -1 : 1;
                if (valA > valB) return this.sortOrder === 'asc' ? 1 : -1;
                return 0;
            });

            return result;
        },

        get totalPages() {
            return Math.ceil(this.filteredSales.length / this.pageSize) || 1;
        },

        get paginatedSales() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.filteredSales.slice(start, start + this.pageSize);
        },

        toggleSort(field) {
            if (this.sortBy === field) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortBy = field;
                this.sortOrder = 'desc';
            }
            this.currentPage = 1;
        },

        formatDate(dateStr) {
            if (!dateStr) return '—';
            const d = new Date(dateStr);
            return isNaN(d.getTime()) ? dateStr : d.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        formatCurrency(amount) {
            const num = parseFloat(amount) || 0;
            return num.toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }
    };
}
