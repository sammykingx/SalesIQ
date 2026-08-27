import collapse from '@alpinejs/collapse';

export function initSidebarModule(Alpine) {
    Alpine.plugin(collapse);

    // Shared store so the header toggle button can also collapse the sidebar
    Alpine.store('sidebar', {
        collapsed: false,
        toggle() {
            this.collapsed = !this.collapsed;
        },
    });

    Alpine.data('sidebarNav', () => ({
        q: '',
        groups: { dashboards: true, crm: false },
        filterOpen: {},
        defaultGroups: { dashboards: true, crm: false },

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
                const groupEl = el.closest('.ax-nav__group');
                const groupName = groupEl?.querySelector('[aria-level="1"]')?.getAttribute('data-ax-group')?.replace('grp.', '');
                if (match && groupName) groupHasMatch[groupName] = true;
            });

            this.filterOpen = { dashboards: !!groupHasMatch.dashboards, crm: !!groupHasMatch.crm };
        },

        clearFilter() {
            this.q = '';
            this.filterOpen = {};
            this.$refs.tree.querySelectorAll('[data-nav-label]').forEach((el) => el.classList.remove('hidden'));
            this.$refs.filter.value = '';
            this.$refs.filter.focus();
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
