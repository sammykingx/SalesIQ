// app/src/entries/products/all-products.js

export function allProductsComponent() {
    return {
        sortBy: 'dateCreated', // Options: 'sales', 'dateCreated', 'price', 'name'
        sortOrder: 'desc',     // Options: 'asc', 'desc'
        searchQuery: '',
        currentPage: 1,
        perPage: 16,
        rawProducts: [],

        init() {
            // Read JSON script tag injected by Django template context
            const scriptTag = document.getElementById('products-data');
            if (scriptTag && scriptTag.textContent.trim()) {
                try {
                    const parsed = JSON.parse(scriptTag.textContent);
                    this.rawProducts = Array.isArray(parsed) ? parsed : [];
                } catch (e) {
                    console.error('Failed to parse backend products_json script:', e);
                    this.rawProducts = [];
                }
            } else {
                this.rawProducts = [];
            }
        },

        // Normalize property names from Django dataclass/dict payloads
        normalizeProduct(p) {
            return {
                id: p.id || Math.random(),
                name: p.name || p.title || 'Untitled Product',
                productType: p.product_type || p.productType || 'physical', // 'physical' or 'virtual'
                price: Number(p.price || 0),
                salesCount: Number(p.sales_count || p.salesCount || p.total_sales || p.sales || 0),
                status: p.status || (p.is_active !== false ? 'Active' : 'Draft'),
                dateCreated: p.date_created || p.created_at || p.added_at || p.dateAdded || new Date().toISOString(),
                // description: p.description || '',
                url: '#', // p.url || p.detail_url || '#',
                imageUrl: p.image_url || p.imageUrl || p.image || null
            };
        },

        get processedProducts() {
            return this.rawProducts.map(p => this.normalizeProduct(p));
        },

        get filteredProducts() {
            const query = this.searchQuery.toLowerCase().trim();
            return this.processedProducts.filter(product => {
                if (!query) return true;
                return (
                    product.name.toLowerCase().includes(query) ||
                    product.productType.toLowerCase().includes(query) ||
                    product.status.toLowerCase().includes(query)
                );
            });
        },

        get sortedProducts() {
            return [...this.filteredProducts].sort((a, b) => {
                const modifier = this.sortOrder === 'asc' ? 1 : -1;

                switch (this.sortBy) {
                    case 'name':
                        return a.name.localeCompare(b.name) * modifier;
                    case 'price':
                        return (a.price - b.price) * modifier;
                    case 'sales':
                        return (a.salesCount - b.salesCount) * modifier;
                    case 'dateCreated':
                    default:
                        return (new Date(a.dateCreated) - new Date(b.dateCreated)) * modifier;
                }
            });
        },

        // Pagination Computations
        get totalPages() {
            return Math.ceil(this.sortedProducts.length / this.perPage) || 1;
        },

        get paginatedProducts() {
            const start = (this.currentPage - 1) * this.perPage;
            const end = start + Number(this.perPage);
            return this.sortedProducts.slice(start, end);
        },

        get paginationStartIndex() {
            if (this.sortedProducts.length === 0) return 0;
            return (this.currentPage - 1) * this.perPage + 1;
        },

        get paginationEndIndex() {
            const end = this.currentPage * this.perPage;
            return end > this.sortedProducts.length ? this.sortedProducts.length : end;
        },

        // Page Navigation Actions
        setPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },

        toggleSortOrder() {
            this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
        },

        formatCurrency(val) {
            return new Intl.NumberFormat('en-NG', {
                style: 'currency',
                currency: 'NGN',
                minimumFractionDigits: 2
            }).format(val || 0);
        },

        formatDate(dateStr) {
            if (!dateStr) return 'N/A';
            try {
                return new Date(dateStr).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
            } catch (e) {
                return 'N/A';
            }
        }
    };
}
