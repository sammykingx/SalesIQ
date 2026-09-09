// app/src/entries/customers/all-customers.js
import { demoCustomers } from './demo-data.js';

export function allCustomersComponent(useDemo = true) {
    return {
        sortBy: 'spend',
        sortOrder: 'desc',
        searchQuery: '',
        currentPage: 1,
        perPage: 15,
        rawCustomers: [],

        bgColors: [
            'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300',
            'bg-indigo-100 text-indigo-800 dark:bg-indigo-950/70 dark:text-indigo-300',
            'bg-purple-100 text-purple-800 dark:bg-purple-950/70 dark:text-purple-300',
            'bg-sky-100 text-sky-800 dark:bg-sky-950/70 dark:text-sky-300',
            'bg-amber-100 text-amber-800 dark:bg-amber-950/70 dark:text-amber-300',
            'bg-rose-100 text-rose-800 dark:bg-rose-950/70 dark:text-rose-300'
        ],

        init() {
            if (useDemo) {
                this.rawCustomers = demoCustomers;
                return;
            }

            const scriptTag = document.getElementById('customers-data');
            if (scriptTag && scriptTag.textContent.trim()) {
                try {
                    let parsed = JSON.parse(scriptTag.textContent);

                    if (typeof parsed === 'string') {
                        parsed = JSON.parse(parsed);
                    }

                    // Handle nested object response wrapper (e.g. { customers: [...] } or { data: [...] })
                    if (!Array.isArray(parsed) && typeof parsed === 'object' && parsed !== null) {
                        parsed = parsed.customers || parsed.data || parsed.results || [];
                    }

                    this.rawCustomers = Array.isArray(parsed) ? parsed : [];

                } catch (e) {
                    this.rawCustomers = [];
                }
            } else {
                this.rawCustomers = [];
            }
        },

        normalizeCustomer(c) {
            if (!c) return {};
            const customerObj = c.customer || {};

            const firstName = c.firstName ?? c.first_name ?? customerObj.firstName ?? customerObj.first_name ?? '';
            const lastName = c.lastName ?? c.last_name ?? customerObj.lastName ?? customerObj.last_name ?? '';

            const fallbackName = `${firstName} ${lastName}`.trim() || 'Customer';
            const displayName = (c.displayName || c.display_name) ? (c.displayName || c.display_name) : fallbackName;
        
            return {
                id: c.id ?? customerObj.id ?? Math.random(),
                displayName: displayName,
                firstName: firstName,
                lastName: lastName,
                email: c.email ?? customerObj.email ?? '',
                phone: c.phone ?? c.phone_number ?? customerObj.phone ?? customerObj.phone_number ?? '',
                spend: Number(c.spend ?? c.total_spend ?? 0),
                totalOrders: Number(c.totalOrders ?? c.total_orders ?? 0),
                status: c.status ?? 'Active',
                dateCreated: c.dateCreated ?? c.created_at ?? c.added_at ?? c.date_created ?? '',
                avatar: c.avatar ?? c.avatar_url ?? null
            };
        },

        get processedCustomers() {
            return this.rawCustomers.map(c => this.normalizeCustomer(c));
        },

        get filteredCustomers() {
            const query = this.searchQuery.toLowerCase().trim();
            return this.processedCustomers.filter(c => {
                if (!query) return true;
                return (
                    (c.firstName && c.firstName.toLowerCase().includes(query)) ||
                    (c.lastName && c.lastName.toLowerCase().includes(query)) ||
                    (c.displayName && c.displayName.toLowerCase().includes(query)) ||
                    (c.email && c.email.toLowerCase().includes(query)) ||
                    (c.phone && c.phone.toLowerCase().includes(query))
                );
            });
        },

        get sortedCustomers() {
            return [...this.filteredCustomers].sort((a, b) => {
                const modifier = this.sortOrder === 'asc' ? 1 : -1;

                switch (this.sortBy) {
                    case 'firstName':
                        return a.firstName.localeCompare(b.firstName) * modifier;
                    case 'lastName':
                        return a.lastName.localeCompare(b.lastName) * modifier;
                    case 'dateCreated':
                        return (new Date(a.dateCreated) - new Date(b.dateCreated)) * modifier;
                    case 'totalOrders':
                        return (a.totalOrders - b.totalOrders) * modifier;
                    case 'spend':
                    default:
                        return (a.spend - b.spend) * modifier;
                }
            });
        },

        get totalPages() {
            return Math.ceil(this.sortedCustomers.length / this.perPage) || 1;
        },

        get paginatedCustomers() {
            const start = (this.currentPage - 1) * this.perPage;
            const end = start + Number(this.perPage);
            return this.sortedCustomers.slice(start, end);
        },

        get paginationStartIndex() {
            if (this.sortedCustomers.length === 0) return 0;
            return (this.currentPage - 1) * this.perPage + 1;
        },

        get paginationEndIndex() {
            const end = this.currentPage * this.perPage;
            return end > this.sortedCustomers.length ? this.sortedCustomers.length : end;
        },

        setPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },

        getInitials(firstName, lastName) {
            const f = firstName ? firstName.charAt(0).toUpperCase() : '';
            const l = lastName ? lastName.charAt(0).toUpperCase() : '';
            return `${f}${l}` || 'CU';
        },

        getAvatarBgClass(id) {
            const numId = typeof id === 'number' ? id : String(id).length;
            const index = Math.abs(numId || 0) % this.bgColors.length;
            return this.bgColors[index];
        }
    };
}
