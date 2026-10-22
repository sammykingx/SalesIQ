// src/entries/metrics/platform/leaderboard.js
import { inAppToast } from "../../../lib/in-app-toast";

export function leaderboardComponent() {
    return {
        searchQuery: '',
        currentPage: 1,
        perPage: 5,
        allData: [],

        init() {
            const scriptTag = document.getElementById('leaderboard-data');
            if (scriptTag && scriptTag.textContent.trim()) {
                try {
                    const parsed = JSON.parse(scriptTag.textContent);
                    this.allData = Array.isArray(parsed) ? parsed : [];
                } catch (e) {
                    inAppToast(
                        'Data Load Error',
                        'We encountered an issue loading the leaderboard data. Please try refreshing the page.',
                        'error'
                    );
                    this.allData = [];
                }
            } else {
                this.allData = [];
            }
        },

        get podiumData() {
            return {
                first: this.allData[0] || null,
                second: this.allData[1] || null,
                third: this.allData[2] || null
            };
        },

        // Live client-side search filtering
        get filteredData() {
            if (!this.searchQuery.trim()) return this.allData;
            const query = this.searchQuery.toLowerCase().trim();
            return this.allData.filter(item =>
                item.name.toLowerCase().includes(query) ||
                item.owner.toLowerCase().includes(query) ||
                item.code.toLowerCase().includes(query)
            );
        },

        get totalPages() {
            return Math.ceil(this.filteredData.length / this.perPage) || 1;
        },

        get paginatedData() {
            const start = (this.currentPage - 1) * this.perPage;
            return this.filteredData.slice(start, start + this.perPage);
        },

        resetSearch() {
            this.searchQuery = '';
            this.currentPage = 1;
        }
    };
}
