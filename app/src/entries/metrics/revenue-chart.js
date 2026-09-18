// app/src/entries/metrics/revenue-chart.js

import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';

export function revenueTrendChart(endpoint) {
    // Store the chart instance in a closure variable here so Alpine 
    // never touches it with its reactivity proxy system!
    let chartInstance = null;

    return {
        period: '7d',
        loading: true,

        async init() {
            await this.load();
            this.$watch('period', () => this.load());
        },

        async load() {
            this.loading = true;
            try {
                const response = await fetch(`${endpoint}?period=${this.period}`);
                if (!response.ok) {
                    inAppToast(
                        "Oops, glitch in the matrix!",
                        "We hit a tiny snag fetching your data. Try refreshing the page!"
                    );
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                this.$nextTick(() => this.render(data));
            } catch (error) {
                console.error("Failed to load data:", error);
            } finally {
                this.loading = false;
            }
        },

        render({ labels, revenue }) {
            // Reference the closure variable instead of `this.chart`
            if (chartInstance) {
                chartInstance.data.labels = labels;
                chartInstance.data.datasets[0].data = revenue;
                chartInstance.update();
                return;
            }

            chartInstance = new Chart(this.$refs.canvas.getContext('2d'), {
                type: 'line',
                data: {
                    labels,
                    datasets: [{
                        data: revenue,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16,185,129,0.08)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 0,
                        borderWidth: 2,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { intersect: false, mode: 'index' }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { display: false } },
                        x: { grid: { display: false } }
                    },
                },
            });
        },
    };
}
