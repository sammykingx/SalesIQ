// app/src/entries/metrics/revenue-chart.js
import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';

function demoWave(pointCount) {
    return Array.from({ length: pointCount }, (_, i) =>
        40 + 25 * Math.sin(i / 1.5) + 10 * Math.sin(i / 0.7)
    );
}

const formatNaira = (value) =>
    `₦${Number(value || 0).toLocaleString('en-NG')}`;

export function revenueTrendChart(endpoint) {
    return {
        period: '7d',
        loading: true,
        isEmpty: false,
        trendChartInstance: null,

        async init() {
            this.$watch('period', (newVal, oldVal) => {
                if (newVal !== oldVal) {
                    this.load();
                }
            });
            await this.load();
        },

        async load() {
            this.loading = true;
            try {
                const url = new URL(endpoint, window.location.origin);
                url.searchParams.set('period', this.period);

                const response = await fetch(url.toString());
                if (!response.ok) {
                    inAppToast(
                        "Oops, glitch in the matrix!",
                        "We hit a tiny snag fetching your data. Try refreshing the page!"
                    );
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                this.$nextTick(() => this.render(data ?? {}));
            } catch (error) {
                this.$nextTick(() => this.render({}));
                console.error("Failed to load data:", error);
            } finally {
                this.loading = false;
            }
        },

        render({ labels = [], revenue = [], has_data = false } = {}) {
            this.isEmpty = !has_data;

            const chartLabels = labels.length ? labels : Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`);
            const chartData = this.isEmpty ? demoWave(chartLabels.length) : revenue;

            const dataset = this.isEmpty
                ? {
                    data: chartData,
                    borderColor: '#a3a3a3',
                    backgroundColor: 'rgba(163,163,163,0.06)',
                    fill: true,
                    tension: 0.45,
                    pointRadius: 0,
                    borderWidth: 2,
                    borderDash: [6, 4],
                }
                : {
                    data: chartData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16,185,129,0.08)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 0,
                    borderWidth: 2,
                };

            const canvas = this.$refs.canvas;
            if (!canvas) return;

            // Update existing instance if it belongs to the current canvas node
            if (this.trendChartInstance && this.trendChartInstance.ctx.canvas === canvas) {
                this.trendChartInstance.data.labels = chartLabels;
                this.trendChartInstance.data.datasets[0] = dataset;
                this.trendChartInstance.options.plugins.tooltip.enabled = !this.isEmpty;
                this.trendChartInstance.options.scales.y.ticks.display = !this.isEmpty;
                this.trendChartInstance.update();
                return;
            }

            // Destroy stale chart instance before binding a new one
            if (this.trendChartInstance) {
                this.trendChartInstance.destroy();
            }

            this.trendChartInstance = new Chart(canvas.getContext('2d'), {
                type: 'line',
                data: { labels: chartLabels, datasets: [dataset] },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            intersect: false,
                            mode: 'index',
                            enabled: !this.isEmpty,
                            callbacks: {
                                label: (context) => {
                                    const value = context.parsed.y ?? 0;
                                    const label = context.dataset.label || 'Revenue';
                                    return `${label}: ${formatNaira(value)}`;
                                }
                            }
                        },
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { display: false }, ticks: { display: !this.isEmpty } },
                        x: { grid: { display: false } },
                    },
                },
            });
        },
    };
}
