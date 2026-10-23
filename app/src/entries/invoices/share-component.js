export function invoiceShareComponent() {
    return {
        open: false,
        copied: false,
        hasNativeShare: false,
        shareUrl: '',
        invoiceID: '',
        businessName: '',

        init() {
            this.hasNativeShare = typeof navigator.share === 'function';

            this.shareUrl = this.$el.dataset.shareUrl || window.location.href;
            this.invoiceID = this.$el.dataset.invoiceId || '';
            this.businessName = this.$el.dataset.businessName || '';
        },

        triggerShare() {
            if (this.hasNativeShare) {
                navigator.share({
                    title: `Invoice #${this.invoiceID} — ${this.businessName}`,
                    text: `View invoice details from ${this.businessName}.`,
                    url: this.shareUrl,
                }).catch(() => { });
            } else {
                this.open = !this.open;
            }
        },

        copyLink() {
            navigator.clipboard.writeText(this.shareUrl);
            this.copied = true;
            setTimeout(() => this.copied = false, 2000);
        },

        shareToWhatsApp() {
            const bName = this.businessName || 'SalesIQ Merchant';
            const text = encodeURIComponent(`View invoice for ${bName}: ${this.shareUrl}`);
            window.open(`https://wa.me/?text=${text}`, '_blank');
        },

        shareToEmail() {
            const id = this.invoiceID || 'N/A';
            const bName = this.businessName || 'Merchant';
            const subject = encodeURIComponent(`Invoice #${id} from ${bName}`);
            const body = encodeURIComponent(`Hello,\n\nPlease find your invoice here: ${this.shareUrl}`);
            window.open(`mailto:?subject=${subject}&body=${body}`);
        },

        printA4() {
            this.open = false;
            setTimeout(() => {
                window.print();
            }, 100);
        },

        printThermal(receiptUrl) {
            this.open = false;
            document.getElementById('thermal-print-frame')?.remove();

            const frame = document.createElement('iframe');
            frame.id = 'thermal-print-frame';
            frame.setAttribute('aria-hidden', 'true');
            
            // Not display:none, some browsers print a blank page from hidden iframes
            frame.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0;';

            frame.onload = () => {
                const win = frame.contentWindow;
                win.addEventListener('afterprint', () => frame.remove(), { once: true });
                win.focus();
                win.print();
            };

            frame.src = receiptUrl;
            document.body.appendChild(frame);
        },
    };
}
