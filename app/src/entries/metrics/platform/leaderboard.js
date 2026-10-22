// src/entries/metrics/platform/leaderboard.js
import { inAppToast } from "../../../lib/in-app-toast";

export function leaderboardComponent() {
    return {
        searchQuery: '',
        currentPage: 1,
        timeframe: 'this_month',
        perPage: 5,
        allData: [],

        init() {
            const urlParams = new URLSearchParams(window.location.search);
            const tfParam = urlParams.get('timeframe');
            if (tfParam && ['this_week', 'this_month', 'all_time'].includes(tfParam)) {
                this.timeframe = tfParam;
            }

            const scriptTag = document.getElementById('leaderboard-data');
            this.loadJSONData(scriptTag);
        },

        loadJSONData(scriptTag) {

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

        async setTimeframe(tf) {
            if (this.loading || this.timeframe === tf) return;

            this.timeframe = tf;
            this.loading = true;

            try {
                // Fetch updated dataset from the backend asynchronously
                const response = await fetch(`?timeframe=${tf}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });

                if (response.ok) {
                    const htmlText = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(htmlText, 'text/html');
                    const newScriptTag = doc.getElementById('leaderboard-data');

                    this.loadJSONData(newScriptTag);

                    // Update browser URL without refreshing the page
                    const newUrl = new URL(window.location.href);
                    newUrl.searchParams.set('timeframe', tf);
                    window.history.pushState({}, '', newUrl);

                    this.currentPage = 1;
                } else {
                    inAppToast(
                        'Data Unavailable',
                        "We couldn't load data for the selected time window. Please try a different range or try again.",
                        'error'
                    );
                }
            } catch (err) {
                inAppToast(
                    'Connection Lost',
                    "We couldn't reach the server.Check your connection and try again in a moment.",
                    'error'
                );
            } finally {
                this.loading = false;
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
