// app/src/entries/metrics/platform-gmv-chart.js
import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';


const chartInstances = new WeakMap();

function demoWave(pointCount) {
    return Array.from({ length: pointCount }, (_, i) =>
        40 + 25 * Math.sin(i / 1.5) + 10 * Math.sin(i / 0.7)
    );
}

const formatNaira = (value) =>
    `₦${Number(value || 0).toLocaleString('en-NG')}`;

export function platformGmvChart(endpoint) {
    return {
        period: '7d',
        loading: true,
        isEmpty: false,

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
                        "We hit a tiny snag fetching platform data. Try refreshing the page!"
                    );
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();

                this.render(data ?? {});
                this.$nextTick(() => {
                    this.loading = false;
                });
            } catch (error) {
                console.error("Failed to load platform GMV:", error);
                this.render({});
                this.$nextTick(() => {
                    this.loading = false;
                });
            }
        },

        render({ labels = [], gmv = [], has_data = false } = {}) {
            this.isEmpty = !has_data;

            const chartLabels = labels.length ? labels : Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`);
            const chartData = this.isEmpty ? demoWave(chartLabels.length) : gmv;

            const dataset = this.isEmpty
                ? {
                    label: 'GMV',
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
                    label: 'GMV',
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

            // Retrieve existing instance keyed by component root ($el)
            const existingChart = chartInstances.get(this.$el);

            // Destroy stale instance on dataset length change (7d -> 30d -> 90d)
            if (existingChart) {
                existingChart.destroy();
                chartInstances.delete(this.$el);
            }

            // Create fresh Chart instance directly on visible canvas
            const chart = new Chart(canvas.getContext('2d'), {
                type: 'line',
                data: {
                    labels: chartLabels,
                    datasets: [dataset],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 250,
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            intersect: false,
                            mode: 'index',
                            enabled: !this.isEmpty,
                            callbacks: {
                                label: (context) => {
                                    const value = context.parsed.y ?? 0;
                                    const label = context.dataset.label || 'GMV';
                                    return `${label}: ${formatNaira(value)}`;
                                },
                            },
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { display: false },
                            ticks: { display: !this.isEmpty },
                        },
                        x: {
                            grid: { display: false },
                        },
                    },
                },
            });

            // Store pure unproxied instance in WeakMap
            chartInstances.set(this.$el, chart);
        },
    };
}
