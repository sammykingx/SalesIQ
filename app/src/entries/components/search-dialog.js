import focus from '@alpinejs/focus';
import { navManifest } from '../../entries/data/manifest.js';
import { mockSearch } from '../../entries/data/mock-serach.js'; // swap for remote-search.js later

export function initSearchDialogModule(Alpine) {
    Alpine.plugin(focus);

    Alpine.data('commandPalette', () => ({
        open: false,
        query: '',
        activeIndex: 0,
        loading: false,
        staticItems: navManifest,
        remoteItems: [],
        controller: null,

        get staticFiltered() {
            const q = this.query.trim().toLowerCase();
            if (!q) return this.staticItems;
            return this.staticItems.filter(
                (i) => i.label.toLowerCase().includes(q) || i.group.toLowerCase().includes(q)
            );
        },

        get filtered() {
            return [...this.remoteItems, ...this.staticFiltered];
        },

        openPalette() {
            this.open = true;
            this.query = '';
            this.remoteItems = [];
            this.activeIndex = 0;
        },

        close() {
            this.open = false;
            this.controller?.abort();
            this.loading = false;
        },

        async search() {
            const q = this.query.trim();
            this.controller?.abort();

            if (!q) {
                this.remoteItems = [];
                this.loading = false;
                return;
            }

            this.controller = new AbortController();
            this.loading = true;

            try {
                this.remoteItems = await mockSearch(q, this.controller.signal);
            } catch (err) {
                if (err.name !== 'AbortError') console.error(err);
            } finally {
                if (!this.controller.signal.aborted) this.loading = false;
            }
        },

        moveDown() {
            this.activeIndex = Math.min(this.activeIndex + 1, this.filtered.length - 1);
            this.scrollActiveIntoView();
        },

        moveUp() {
            this.activeIndex = Math.max(this.activeIndex - 1, 0);
            this.scrollActiveIntoView();
        },

        scrollActiveIntoView() {
            this.$nextTick(() => {
                this.$refs.results.querySelector('[data-active="true"]')?.scrollIntoView({ block: 'nearest' });
            });
        },

        select(item) {
            item = item || this.filtered[this.activeIndex];
            if (!item) return;
            this.close();
            if (item.action === 'toggleTheme') {
                const isDark = document.documentElement.classList.toggle('dark');
                localStorage.setItem('vireo-theme', isDark ? 'dark' : 'light');
            } else if (item.href) {
                window.location.href = item.href;
            }
        },
    }));
}
