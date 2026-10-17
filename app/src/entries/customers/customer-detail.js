// app/src/entries/customers/customer-detail.js
import { demoCustomers } from './demo-data.js';

export function customerDetailComponent() {
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
                    // Fallback to demo data (e.g., first demo customer with rich mock stats)
                    const sample = demoCustomers[0];
                    this.customer = {
                        id: sample.id,
                        firstName: sample.firstName,
                        lastName: sample.lastName,
                        email: sample.email,
                        phone: sample.phone,
                        status: sample.status,
                        dateCreated: sample.dateCreated,
                        avatar: sample.avatar,
                        spend: sample.spend,
                        totalOrders: sample.totalOrders,
                        repeatPercentage: 78.5, // Mock metric
                        recentSales: [
                            { id: 'INV-2026-142', date: '2026-04-12', itemsSummary: 'Premium Leather Bag, Dust Cover', total: 1850.00, status: 'Paid' },
                            { id: 'INV-2026-118', date: '2026-03-28', itemsSummary: 'Wireless Earbuds Pro', total: 920.00, status: 'Paid' },
                            { id: 'INV-2026-089', date: '2026-03-05', itemsSummary: 'Minimalist Card Holder', total: 350.00, status: 'Paid' },
                            { id: 'INV-2026-045', date: '2026-02-14', itemsSummary: 'Designer Silk Scarf', total: 680.00, status: 'Paid' },
                            { id: 'INV-2026-012', date: '2026-01-20', itemsSummary: 'Classic Chronograph Watch', total: 450.00, status: 'Paid' }
                        ]
                    };
                }
            } catch (err) {
                console.error('Failed to parse customer data:', err);
            }
            this.resetEditForm();
        },

        normalizeCustomer(data) {
            return {
                id: data.id || null,
                firstName: data.first_name || data.firstName || '',
                lastName: data.last_name || data.lastName || '',
                email: data.email || '',
                phone: data.phone || '',
                status: data.status || 'Active',
                dateCreated: data.date_created || data.dateCreated || new Date().toISOString(),
                avatar: data.avatar || null,
                spend: Number(data.spend || data.total_spend || 0),
                totalOrders: Number(data.total_orders || data.totalOrders || 0),
                repeatPercentage: Number(data.repeat_percentage || data.repeatPercentage || 0),
                recentSales: data.recent_sales || data.recentSales || []
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
                phone: this.editForm.phone.trim()
            };

            try {
                // Simulate backend API call or replace with actual endpoint
                await new Promise(resolve => setTimeout(resolve, 600));

                // Update local state on success
                this.customer.firstName = payload.first_name;
                this.customer.lastName = payload.last_name;
                this.customer.email = payload.email;
                this.customer.phone = payload.phone;

                this.successMessage = 'Customer information updated successfully.';
                this.isEditing = false;

                // Dispatch custom event if parent listeners require it
                window.dispatchEvent(new CustomEvent('customer-updated', { detail: this.customer }));
            } catch (err) {
                this.errorMessage = err.message || 'Failed to update customer information.';
            } finally {
                this.loading = false;
            }
        },

        formatCurrency(amount) {
            return '₦' + Number(amount || 0).toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        },

        formatDate(dateString) {
            if (!dateString) return 'N/A';
            return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
    };
}
