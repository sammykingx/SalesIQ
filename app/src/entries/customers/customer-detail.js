// app/src/entries/customers/customer-detail.js
import { demoCustomers } from './demo-data.js';
import { inAppToast } from '../../lib/in-app-toast.js';

export function customerDetailComponent(endpointUrl = '') {
    return {
        // State
        isEditing: false,
        loading: false,
        successMessage: '',
        errorMessage: '',

        customer: {
            id: null,
            firstName: '',
            lastName: '',
            email: '',
            phone: '',
            status: 'Active',
            dateCreated: '',
            avatar: null,
            spend: 0,
            totalOrders: 0,
            repeatPercentage: 0,
            recentSales: []
        },

        // Editable form draft state
        editForm: {
            firstName: '',
            lastName: '',
            email: '',
            phone: ''
        },

        init() {
            this.loadCustomerData();
        },

        loadCustomerData() {
            try {
                const scriptTag = document.getElementById('customer-data');
                if (scriptTag && scriptTag.textContent.trim()) {
                    const backendData = JSON.parse(scriptTag.textContent);
                    this.customer = this.normalizeCustomer(backendData);
                } else {
                    const sample = demoCustomers[0];
                    // this.customer = {
                    //     id: sample.id,
                    //     firstName: sample.firstName,
                    //     lastName: sample.lastName,
                    //     email: sample.email,
                    //     phone: sample.phone,
                    //     status: sample.status,
                    //     dateCreated: sample.dateCreated,
                    //     avatar: sample.avatar,
                    //     spend: sample.spend,
                    //     totalOrders: sample.totalOrders,
                    //     repeatPercentage: 78.5, // Mock metric
                    //     recentSales: [
                    //         { displayId: 'SIQ-INV-4ZHG-64W6', slug: '5q6tnkcdc1mzt8selb4y6cbkjxm42ntfyp', dateDisplay: 'Oct 04', itemsSummary: 'Domain Name + 1 more', total: 25000.0, status: 'paid' },
                    //         { displayId: 'SIQ-INV-4ZHG-EHKO', slug: '8l8l07dw7blsxde3dj2de4m9hc68a2fu1h', dateDisplay: 'Sep 24', itemsSummary: 'Web Development + 4 more', total: 825125.0, status: 'paid' }
                    //     ]
                    // };
                }
            } catch (err) {
                // console.error('Failed to parse customer data:', err);
                inAppToast({
                    title: "Failed to Load Customer Profile",
                    message: "We couldn't process the customer's information correctly. Please refresh the page to try again.",
                    type: "error"
                });
            }
            this.resetEditForm();
        },

        normalizeCustomer(data) {
            const toTitleCase = (str) => {
                if (!str) return '';
                return str.trim().toLowerCase().replace(/\b\w/g, (char) => char.toUpperCase());
            };

            const parts = data.display_name.trim().split(/\s+/);
            const firstName = parts[0] || '';
            const lastName = parts.slice(1).join(' ') || '';

            const rawSales = data.recent_sales || data.recentSales || [];
            const normalizedSales = rawSales.map(sale => {
                let summary = sale.first_item || sale.itemsSummary || 'Item';
                const extra = sale.extra_count ?? sale.extraCount ?? 0;
                if (extra > 0) {
                    summary += ` + ${extra} more`;
                }
                return {
                    displayId: sale.display_id || sale.displayId || sale.id || 'INV-000',
                    slug: sale.slug || '',
                    dateDisplay: sale.date_display || sale.dateDisplay || 'N/A',
                    itemsSummary: summary,
                    total: Number(sale.total || sale.amount || 0),
                    status: sale.status || 'paid'
                };
            });

            const custData = data.customer || data;

            return {
                id: custData.id || null,
                firstName: toTitleCase(firstName || custData.first_name || ''),
                lastName: toTitleCase(lastName || custData.last_name || ''),
                email: custData.email || '',
                phone: custData.phone_number || custData.phone || '',
                status: data.status || 'Active',
                dateCreated: data.date_created || data.dateCreated || new Date().toISOString(),
                avatar: data.avatar || null,
                spend: Number(data.lifetime_spend || data.total_spend || data.spend || 0),
                totalOrders: Number(data.order_count || data.totalOrders || 0),
                repeatPercentage: Number(data.repeat_rate || data.repeatPercentage || 0),
                recentSales: normalizedSales
            };
        },

        resetEditForm() {
            this.editForm = {
                firstName: this.customer.firstName,
                lastName: this.customer.lastName,
                email: this.customer.email,
                phone: this.customer.phone
            };
        },

        // Computed Initials & Avatar Styling
        get fullName() {
            return `${this.customer.firstName} ${this.customer.lastName}`.trim() || 'Unnamed Customer';
        },

        get initials() {
            const f = this.customer.firstName ? this.customer.firstName[0] : '';
            const l = this.customer.lastName ? this.customer.lastName[0] : '';
            return (f + l).toUpperCase() || 'CS';
        },

        get avatarBgColor() {
            const colors = [
                'bg-indigo-100 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300',
                'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300',
                'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300',
                'bg-rose-100 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300',
                'bg-sky-100 text-sky-700 dark:bg-sky-950/60 dark:text-sky-300'
            ];
            const charCode = (this.customer.firstName || 'A').charCodeAt(0);
            return colors[charCode % colors.length];
        },

        // Actions
        toggleEdit() {
            if (this.isEditing) {
                this.resetEditForm();
            }
            this.isEditing = !this.isEditing;
            this.successMessage = '';
            this.errorMessage = '';
        },

        async saveCustomerInfo() {
            if (this.loading) return;

            this.loading = true;
            this.errorMessage = '';
            this.successMessage = '';

            const payload = {
                first_name: this.editForm.firstName.trim(),
                last_name: this.editForm.lastName.trim(),
                email: this.editForm.email.trim(),
                phone_number: this.editForm.phone.trim()
            };

            try {
                const response = await apiRequest(endpointUrl, 'POST', payload);
                const data = await response.json().catch(() => ({}));


                this.successMessage = 'Customer information updated successfully.';
                this.isEditing = false;

                if (!response.ok) {
                    if (response.status === 422) {
                        const errorDetails = Array.isArray(data.error)
                            ? data.error.map(err => {
                                const formattedField = err.field
                                    ? err.field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                                    : 'Field';
                                return `${formattedField}: ${err.message}`;
                            }).join(' | ')
                            : (data.error || '')

                        inAppToast(
                            'Update Rejected 🚫',
                            `${data.message}`,
                            'warning',
                            4500
                        );
                    } else {
                        inAppToast('Ecosystem Glitch ⚠️', data.message || 'An unexpected error occurred.', 'error');
                    }
                    return;
                }

                inAppToast({
                    title: "Client Updated Successfully",
                    message: "The customer's profile information has been updated.",
                    type: "success"
                });
            } catch (err) {
                this.errorMessage = err.message || 'Failed to update customer information.';
            } finally {
                this.loading = false;
            }
        },

        formatCurrency(amount) {
            return '₦' + Number(amount || 0).toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        },

        getInvoiceUrl(slug) {
            const container = document.querySelector('[data-invoice-base-url]');
            if (container) {
                const baseUrl = container.getAttribute('data-invoice-base-url');
                return baseUrl.replace('__slug__', slug);
            }

            return '#';
        },

        formatDate(dateString) {
            if (!dateString) return 'N/A';
            return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
    };
}
