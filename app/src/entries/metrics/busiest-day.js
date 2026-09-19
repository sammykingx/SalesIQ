// app/src/entries/metrics/busiest-days.js

import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';

const PEAK = '#10b981'; // Primary highlight color
const BASE = '#e5e7eb'; // Default bar color
const MUTED = 'rgba(163, 163, 163, 0.15)'; // Fallback empty-state bar color

const formatNaira = (val) => `₦${Number(val || 0).toLocaleString('en-NG')}`;

export function busiestDaysChart(endpoint) {
    return {
        loading: true,
        isEmpty: false,
        peakLabel: null,
        peakPct: null,
        barChartInstance: null,

        async init() {
            await this.load();
        },

        async load() {
            this.loading = true;
            try {
                
                const response = await fetch(endpoint);
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
                console.error("Failed to load busiest days:", error);
            } finally {
                this.loading = false;
            }
        },

        render({ labels = [], revenue = [], has_data = false, peak_index = null, peak_label = null, peak_pct = null } = {}) {
            this.isEmpty = !has_data;
            this.peakLabel = peak_label;
            this.peakPct = peak_pct;

            const chartLabels = labels.length ? labels : ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
            const chartData = this.isEmpty ? chartLabels.map(() => 30) : revenue;

            const colors = this.isEmpty
                ? chartLabels.map(() => MUTED)
                : chartLabels.map((_, i) => (i === peak_index ? PEAK : BASE));

            const canvas = this.$refs.canvas;
            if (!canvas) return;

            // Update existing instance if tied to current canvas node
            if (this.barChartInstance && this.barChartInstance.ctx.canvas === canvas) {
                this.barChartInstance.data.labels = chartLabels;
                this.barChartInstance.data.datasets[0].data = chartData;
                this.barChartInstance.data.datasets[0].backgroundColor = colors;
                this.barChartInstance.options.plugins.tooltip.enabled = !this.isEmpty;
                this.barChartInstance.options.scales.y.ticks.display = !this.isEmpty;
                this.barChartInstance.update();
                return;
            }

            // Clean up stale chart instance if canvas element changed
            if (this.barChartInstance) {
                this.barChartInstance.destroy();
            }

            this.barChartInstance = new Chart(canvas.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: chartLabels,
                    datasets: [{
                        data: chartData,
                        backgroundColor: colors,
                        borderRadius: 6,
                        maxBarThickness: 40
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            enabled: !this.isEmpty,
                            callbacks: {
                                label: (context) => `Revenue: ${formatNaira(context.parsed.y)}`
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
