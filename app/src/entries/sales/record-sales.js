// import { demoCustomers } from "../customers/demo-data.js";
// import { demoProductsData } from "../products/demo-data.js";
import { inAppToast } from "../../lib/in-app-toast.js";
import { apiRequest } from "../../lib/http/api.js";

/**
 * Parses JSON script tags rendered by Django templates, falling back to demo data if absent.
 */
function loadInitialData(scriptId, fallbackData) {
    const scriptElement = document.getElementById(scriptId);
    if (scriptElement && scriptElement.textContent.trim()) {
        try {
            const parsed = JSON.parse(scriptElement.textContent);
            if (Array.isArray(parsed) && parsed.length > 0) {
                return parsed;
            }
        } catch (e) {
            console.error(`Failed to parse JSON script tag #${scriptId}:`, e);
            inAppToast(
                'Missing a Few Pieces',
                'SalesIQ is sharp, but it can’t read an empty page. Let’s get this data filled in.',
                'warning'
            )
        }
    }
    return fallbackData;
}

export function recordSaleComponent(endpoint) {
    return {
        // Data registries loaded from Django JSON script tags or fallback demo modules
        customersJson: [],
        productsJson: [],

        // Customer Form State
        customerSearch: '',
        showCustomerDropdown: false,
        isCustomerLocked: false, // <-- Tracks lock status
        selectedCustomer: {
            id: null,
            first_name: '',
            last_name: '',
            email: '',
            phone_number: ''
        },

        // Sales Line Items State
        items: [],

        // Taxes & Discounts State
        discountPercentage: 0,
        taxName: 'VAT',
        taxPercentage: '',

        // UI Loading & Submission State
        isSubmitting: false,
        submitSuccess: false,

        init() {
            // this.customersJson = loadInitialData('customers_data', demoCustomers);
            // this.productsJson = loadInitialData('products_data', demoProductsData);

            this.customersJson = loadInitialData('customers_data', []);
            this.productsJson = loadInitialData('products_data', []);

            // Initialize with one default blank line item
            this.addItem();
        },

        // Helper: Number Formatter (Naira format with thousands separators)
        formatCurrency(val) {
            let num = parseFloat(val) || 0;
            return num.toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        },

        // Customer Lookup Logic
        get filteredCustomers() {
            if (!this.customerSearch.trim()) return [];
            const q = this.customerSearch.toLowerCase();
            return this.customersJson.filter(c => {
                const firstName = (c.first_name || c.firstName || '').toLowerCase();
                const lastName = (c.last_name || c.lastName || '').toLowerCase();
                const email = (c.email || '').toLowerCase();
                const phone = c.phone_number || c.phone || '';
                return firstName.includes(q) || lastName.includes(q) || email.includes(q) || phone.includes(q);
            });
        },

        selectCustomer(cust) {
            const firstName = cust.first_name || cust.firstName || '';
            const lastName = cust.last_name || cust.lastName || '';

            this.selectedCustomer = {
                id: cust.id || null,
                first_name: firstName,
                last_name: lastName,
                email: cust.email || '',
                phone_number: cust.phone_number || cust.phone || ''
            };
            this.customerSearch = `${firstName} ${lastName}`.trim();
            this.showCustomerDropdown = false;
            this.isCustomerLocked = true; // Lock fields upon selecting existing customer
        },

        unlockCustomer() {
            this.isCustomerLocked = false;
            this.selectedCustomer = {
                id: null,
                first_name: '',
                last_name: '',
                email: '',
                phone_number: ''
            };
            this.customerSearch = '';
        },

        resetCustomerIfEdited() {
            if (this.selectedCustomer.id) {
                this.selectedCustomer.id = null; // Mark as new customer if modified manually
            }
        },

        // Line Item Operations
        addItem() {
            this.items.push({
                id: null,
                product_name: '',
                price: 0,
                formatted_price: '0',
                product_type: 'physical',
                quantity: 1,
                is_new: true,
                showDropdown: false,
                searchQuery: ''
            });
        },

        removeItem(index) {
            if (this.items.length > 1) {
                this.items.splice(index, 1);
            }
        },

        getFilteredProducts(query) {
            if (!query.trim()) return [];
            const q = query.toLowerCase();
            return this.productsJson.filter(p => {
                const name = (p.product_name || p.name || '').toLowerCase();
                return name.includes(q);
            });
        },

        selectProduct(index, prod) {
            let item = this.items[index];
            const prodName = prod.product_name || prod.name || '';
            const prodPrice = prod.price || prod.spend || 0;
            const prodType = prod.product_type || 'physical';

            item.id = prod.id;
            item.product_name = prodName;
            item.searchQuery = prodName;
            item.price = prodPrice;
            item.formatted_price = prodPrice.toLocaleString('en-NG');
            item.product_type = prodType;
            item.is_new = false;
            item.showDropdown = false;

            if (prodType === 'service') {
                item.quantity = 1;
            }
        },

        handleProductInput(index) {
            let item = this.items[index];
            item.product_name = item.searchQuery;
            item.id = null;
            item.is_new = true;
            item.showDropdown = true;
        },

        formatPriceInput(index, value) {
            let cleanDigits = value.replace(/\D/g, '');
            let numericVal = parseInt(cleanDigits, 10) || 0;
            this.items[index].price = numericVal;
            this.items[index].formatted_price = numericVal ? numericVal.toLocaleString('en-NG') : '0';
        },

        // Financial Calculation Getters
        get subTotal() {
            return this.items.reduce((sum, item) => {
                let qty = item.product_type === 'service' ? 1 : (parseInt(item.quantity, 10) || 1);
                return sum + (parseFloat(item.price) * qty);
            }, 0);
        },

        get discountAmount() {
            let pct = parseFloat(this.discountPercentage) || 0;
            return (this.subTotal * pct) / 100;
        },

        get taxAmount() {
            let pct = parseFloat(this.taxPercentage) || 0;
            return (this.subTotal * pct) / 100;
        },

        get grandTotal() {
            return this.subTotal + this.taxAmount - this.discountAmount;
        },

        resetForm() {
            this.selectedCustomer = {
                id: null,
                first_name: '',
                last_name: '',
                email: '',
                phone_number: ''
            };

            this.items = [];

            this.discountPercentage = 0;
            this.taxName = 'VAT';
            this.taxPercentage = '';
        },

        async submitSaleForm() {
            this.isSubmitting = true;

            const payload = {
                customer: {
                    id: this.selectedCustomer.id,
                    first_name: this.selectedCustomer.first_name,
                    last_name: this.selectedCustomer.last_name,
                    email: this.selectedCustomer.email,
                    phone_number: this.selectedCustomer.phone_number
                },
                products: this.items.map(item => ({
                    id: item.id,
                    name: item.product_name,
                    price: parseFloat(item.price),
                    product_type: item.product_type,
                    quantity: item.product_type === 'service' ? 1 : parseInt(item.quantity, 10)
                })),
                sub_total: this.subTotal,
                discount_percentage: parseFloat(this.discountPercentage) || 0,
                discount_amount: this.discountAmount,
                tax_name: this.taxName,
                tax_percentage: parseFloat(this.taxPercentage) || 0,
                tax_amount: this.taxAmount,
                total_amount: this.grandTotal
            };

            try {
                const response = await apiRequest(endpoint, "POST", payload);
                const data = await response.json().catch(() => { })

                if (!response.ok) {
                    if (response.status === 422) {
                        const errorDetails = Array.isArray(data?.error)
                            ? data.error.map(err => {
                                const formattedField = err.field
                                    ? err.field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                                    : 'Field';
                                return `${formattedField}: ${err.message}`;
                            }).join(' | ')
                            : (data?.error || '');

                        inAppToast(
                            'Sale Identity Rejected 🚫',
                            data?.message || "Fix the typos and let's give it another shot.",
                            'warning',
                            4500
                        );
                    } else {
                        inAppToast('Ecosystem Glitch ⚠️', data?.message || 'An unexpected error occurred.', 'error');
                    }
                    return;
                }

                inAppToast(
                    data?.title || "Sales Recorded",
                    data?.message || "The sale has been successfully recorded in your books and ready for insights.",
                    data?.status || "success"
                );
                this.submitSuccess = true;
                this.resetForm();
                if (data?.redirect && data?.redirect_url) {
                    setTimeout(() => {
                        window.location.assign(data.redirect_url);
                    }, 2500);
                }

            } catch (err) {
                inAppToast('Connection Void 🌪️', err.message || 'Failed to reach the server. Check your network connection.', 'error');
            } finally {
                this.isSubmitting = false;
            }

        }
    };
}
