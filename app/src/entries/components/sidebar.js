// app/src/entries/components/sidebar.js
import collapse from '@alpinejs/collapse';

export function initSidebarModule(Alpine) {
    Alpine.plugin(collapse);

    Alpine.store('sidebar', {
        collapsed: false,
        mobileOpen: false,

        toggle() {
            if (window.matchMedia('(min-width: 1024px)').matches) {
                this.collapsed = !this.collapsed;
            } else {
                this.mobileOpen = !this.mobileOpen;
            }
        },

        closeMobile() {
            this.mobileOpen = false;
        },
    });

    Alpine.data('sidebarNav', () => ({
        q: '',
        groups: { dashboards: true, crm: false },
        filterOpen: {},

        toggle(name) {
            this.groups[name] = !this.groups[name];
        },

        matchesGroup(name) {
            if (!this.q) return true;
            return this.filterOpen[name] !== false;
        },

        filter(value) {
            this.q = value.trim().toLowerCase();
            const items = this.$refs.tree.querySelectorAll('[data-nav-label]');

            if (!this.q) return this.clearFilter();

            const groupHasMatch = {};
            items.forEach((el) => {
                const match = el.dataset.navLabel.toLowerCase().includes(this.q);
                el.classList.toggle('hidden', !match);
                const groupEl = el.closest('.nav_grp');
                const groupName = groupEl?.getAttribute('data-group-name');
                if (match && groupName) groupHasMatch[groupName] = true;
            });

            this.filterOpen = { dashboards: !!groupHasMatch.dashboards, crm: !!groupHasMatch.crm };
        },

        clearFilter() {
            this.q = '';
            this.filterOpen = {};
            this.$refs.tree.querySelectorAll('[data-nav-label]').forEach((el) => el.classList.remove('hidden'));
            if (this.$refs.filter) {
                this.$refs.filter.value = '';
                this.$refs.filter.focus();
            }
        },

        onTreeKey(e) {
            const items = Array.from(this.$refs.tree.querySelectorAll('[role="treeitem"]:not(.hidden)'));
            const current = document.activeElement;
            const i = items.indexOf(current);
            if (i === -1) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                items[(i + 1) % items.length]?.focus();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                items[(i - 1 + items.length) % items.length]?.focus();
            } else if (e.key === 'ArrowRight' && current.getAttribute('aria-expanded') === 'false') {
                current.click();
            } else if (e.key === 'ArrowLeft' && current.getAttribute('aria-expanded') === 'true') {
                current.click();
            }
        },
    }));
}
