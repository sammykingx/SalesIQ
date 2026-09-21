// app/src/entries/metrics/platform-gmv-chart.js
import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';

function demoWave(pointCount) {
    return Array.from({ length: pointCount }, (_, i) =>
        40 + 25 * Math.sin(i / 1.5) + 10 * Math.sin(i / 0.7)
    );
}

export function platformGmvChart(endpoint) {
    return {
        period: '7d',
        loading: true,
        isEmpty: false,
        gmvChartInstance: null,

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
                        "We hit a tiny snag fetching platform data. Try refreshing the page!"
                    );
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                this.$nextTick(() => this.render(data));
            } catch (error) {
                console.error("Failed to load platform GMV:", error);
                this.$nextTick(() => this.render({}));
            } finally {
                this.loading = false;
            }
        },

        render({ labels = [], gmv = [], has_data = false } = {}) {
            this.isEmpty = !has_data;

            const chartLabels = labels.length ? labels : Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`);
            const chartData = this.isEmpty ? demoWave(chartLabels.length) : gmv;

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

            if (this.gmvChartInstance) {
                this.gmvChartInstance.data.labels = chartLabels;
                this.gmvChartInstance.data.datasets[0] = dataset;
                this.gmvChartInstance.options.plugins.tooltip.enabled = !this.isEmpty;
                this.gmvChartInstance.options.scales.y.ticks.display = !this.isEmpty;
                this.gmvChartInstance.update();
                return;
            }

            this.gmvChartInstance = new Chart(this.$refs.canvas.getContext('2d'), {
                type: 'line',
                data: { labels: chartLabels, datasets: [dataset] },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { intersect: false, mode: 'index', enabled: !this.isEmpty },
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
