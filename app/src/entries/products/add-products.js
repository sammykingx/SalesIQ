import { apiRequest } from '../../lib/http/api.js';
import { inAppToast } from '../../lib/in-app-toast.js';
import { closeAppModal } from '../components/modal.js';

export function addProductForm(endpointUrl = '') {
    return {
        productType: 'physical',
        formattedPrice: '',
        rawPrice: '',
        description: '',
        submitting: false,

        isBold: false,
        isItalic: false,

        allowOnlyNumbers(event) {
            const allowedKeys = ['Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 'ArrowLeft', 'ArrowRight', 'Home', 'End'];
            if (allowedKeys.includes(event.key) || (event.ctrlKey || event.metaKey)) {
                return;
            }

            // Block decimal if one already exists in the input
            if (event.key === '.' && event.target.value.includes('.')) {
                event.preventDefault();
                return;
            }

            // Block anything that isn't a digit or a decimal point
            if (!/^[0-9.]$/.test(event.key)) {
                event.preventDefault();
            }
        },

        // Paste filter: Strip non-numeric/non-decimal content from clipboard
        handlePaste(event) {
            event.preventDefault();
            const clipboardData = event.clipboardData || window.clipboardData;
            const pastedData = clipboardData.getData('text');

            // Extract numeric string with at most one decimal point
            let sanitized = pastedData.replace(/[^0-9.]/g, '');
            const parts = sanitized.split('.');
            if (parts.length > 2) {
                sanitized = parts[0] + '.' + parts.slice(1).join('');
            }

            // Programmatically insert and trigger re-formatting
            event.target.value = sanitized;
            this.formatNairaInput(event);
        },

        // Format execution
        execCmd(command, value = null) {
            document.execCommand(command, false, value);
            this.updateState();
        },

        // Sync button active states with caret / selection position
        updateState() {
            this.isBold = document.queryCommandState('bold');
            this.isItalic = document.queryCommandState('italic');
        },

        // Reset state and editor content
        resetForm() {
            this.productType = 'physical';
            this.formattedPrice = '';
            this.rawPrice = '';
            this.description = '';
            this.isBold = false;
            this.isItalic = false;
            this.submitting = false;

            if (this.$refs.editorContainer) {
                this.$refs.editorContainer.innerHTML = '';
            }
        },

        // Executed on @input for price
        formatNairaInput(event) {
            let input = event.target.value;

            // Strict sanitization fallback
            let sanitized = input.replace(/[^0-9.]/g, '');

            const parts = sanitized.split('.');
            if (parts.length > 2) {
                sanitized = parts[0] + '.' + parts.slice(1).join('');
            }

            if (parts[1] && parts[1].length > 2) {
                sanitized = parts[0] + '.' + parts[1].substring(0, 2);
            }

            this.rawPrice = sanitized;

            if (sanitized) {
                const [integerPart, decimalPart] = sanitized.split('.');
                const formattedInteger = parseInt(integerPart || '0', 10).toLocaleString('en-US');

                this.formattedPrice = decimalPart !== undefined
                    ? `${formattedInteger}.${decimalPart}`
                    : formattedInteger;
            } else {
                this.formattedPrice = '';
            }
        },

        // Handle Form Submission
        async handleSubmit(event) {
            const formElement = event.target;
            const targetUrl = endpointUrl || formElement.getAttribute('action');

            if (this.submitting || !targetUrl) return;

            const formData = new FormData(formElement);
            const payload = {
                name: formData.get('name')?.toString().trim(),
                product_type: this.productType,
                price: parseFloat(this.rawPrice || '0'),
                description: this.description
            };

            this.submitting = true;

            try {
                const response = await apiRequest(targetUrl, 'POST', payload);
                const data = await response.json().catch(() => null);

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
                            'Product Identity Rejected 🚫',
                            data?.message || "Fix the typos and let's give it another shot.",
                            'warning',
                            4500
                        );
                    } else {
                        inAppToast('Ecosystem Glitch ⚠️', data?.message || 'An unexpected error occurred.', 'error');
                    }
                    return;
                }

                inAppToast('Added to the fold ✨', data?.message || 'Product successfully created!', 'success');

                this.resetForm();
                if (formElement && typeof formElement.reset === 'function') {
                    formElement.reset();
                }
                setTimeout(() => {
                    window.location.reload();
                }, 1500);

                closeAppModal();
            } catch (err) {
                inAppToast('Connection Void 🌪️', err.message || 'Failed to reach the server. Check your network connection.', 'error');
            } finally {
                this.submitting = false;
            }
        }
    };
}
