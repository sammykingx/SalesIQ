import { apiRequest } from '../../lib/http/api.js';
import { inAppToast } from '../../lib/in-app-toast.js';

export function modifyProductComponent(endpointUrl = '') {
    return {
        endpoint: '',
        isLoading: false,

        productData: {
            id: '',
            name: '',
            price: '',
            product_type: '',
            description: ''
        },
        form: {
            product_id: '',
            name: '',
            price: '',
            product_type: '',
            description: ''
        },

        init() {
            const formEl = document.getElementById('product-form');
            if (formEl && formEl.getAttribute('action')) {
                this.endpoint = formEl.getAttribute('action');
            }

            const scriptTag = document.getElementById('product-data');
            if (scriptTag && scriptTag.textContent.trim()) {
                try {
                    const parsed = JSON.parse(scriptTag.textContent);
                    this.productData = {
                        id: String(parsed.id || ''),
                        name: parsed.name || '',
                        price: parsed.price ? String(parsed.price) : '',
                        product_type: parsed.product_type || 'physical',
                        description: parsed.description || ''
                    };

                    this.form = {
                        product_id: parsed.id || '',
                        name: parsed.name || '',
                        price: parsed.price ? String(parsed.price) : '',
                        product_type: parsed.product_type || 'physical',
                        description: parsed.description || ''
                    };

                } catch (e) {
                    inAppToast(
                        'Initialization Error',
                        'Failed to parse product data, kindly refresh page',
                        'warning'
                    );
                }
            }
        },

        formatWithCommas(val) {
            if (!val && val !== 0) return '';
            const parts = String(val).split('.');
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            return parts.join('.');
        },

        resetForm() {
            this.form = { ...this.productData };
        },

        validatePrice(e) {
            let value = e.target.value;
            value = value.replace(/[^0-9.]/g, '');

            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            if (parts[1] && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].substring(0, 2);
            }

            this.form.price = value;
        },

        async saveProduct() {
            if (this.isLoading) return;

            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';

            const targetUrl = this.endpoint || endpointUrl || window.location.pathname;

            const payload = {
                product_id: this.productData.id,
                name: this.form.name,
                price: Number(this.form.price) || 0,
                product_type: this.form.product_type,
                description: this.form.description
            };

            try {
                const response = await apiRequest(targetUrl, 'PUT', payload);
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
                            'Product Update Rejected 🚫',
                            data?.message || "Fix the typos and let's give it another shot.",
                            'warning',
                            4500
                        );
                    } else {
                        inAppToast(
                            data?.title || 'Ecosystem Glitch ⚠️',
                            data?.message || 'An unexpected error occurred.',
                            data?.status || 'error'
                        );
                    }
                    return;
                }
                inAppToast('Product Updated✨', data?.message || `Your product ${this.form.name} was successfully updated.`, 'success');
                this.productData = {
                    ...this.productData,
                    ...payload,
                    price: String(payload.price)
                };

                if (data.redirect && data.redirect_url) {
                    setTimeout(() => {
                        window.location.href = data.redirect_url
                    }, 1500);
                }

            } catch (error) {
                inAppToast('Connection Void 🌪️', err.message || 'Failed to reach the server. Check your network connection.', 'error');
            } finally {
                this.isLoading = false;
            }
        }
    };
}
