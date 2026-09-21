// app/src/entries/metrics/adoption-chart.js
import { inAppToast } from '../../lib/in-app-toast.js';
import { Chart } from '../../lib/register-chart.js';

const ADOPTED = '#10b981';     // emerald-500
const NOT_ADOPTED = '#e5e5e5'; // neutral-200
const MUTED = '#d4d4d4';       // neutral-300, empty-state single slice

export function platformAdoptionChart(endpoint) {
    return {
        thresholds: [1, 5, 10, 15, 20],
        threshold: 1,
        loading: true,
        isEmpty: false,
        adopted: 0,
        notAdopted: 0,
        adoptionRate: 0,
        pieChartInstance: null,

        async init() {
            await this.load();
            this.$watch('threshold', () => this.load());
        },

        async load() {
            this.loading = true;
            try {
                const response = await fetch(`${endpoint}?threshold=${this.threshold}`);
                if (!response.ok) {
                    inAppToast(
                        "Oops, glitch in the matrix!",
                        "We hit a tiny snag fetching adoption data. Try refreshing the page!"
                    );
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                this.$nextTick(() => this.render(data));
            } catch (error) {
                console.error("Failed to load adoption data:", error);
                this.$nextTick(() => this.render({}));
            } finally {
                this.loading = false;
            }
        },

        render({ adopted = 0, not_adopted = 0, adoption_rate = 0, has_data = false } = {}) {
            this.isEmpty = !has_data;
            this.adopted = adopted;
            this.notAdopted = not_adopted;
            this.adoptionRate = adoption_rate;

            const chartData = this.isEmpty ? [1] : [adopted, not_adopted];
            const colors = this.isEmpty ? [MUTED] : [ADOPTED, NOT_ADOPTED];

            if (this.pieChartInstance) {
                this.pieChartInstance.data.datasets[0].data = chartData;
                this.pieChartInstance.data.datasets[0].backgroundColor = colors;
                this.pieChartInstance.options.plugins.tooltip.enabled = !this.isEmpty;
                this.pieChartInstance.update();
                return;
            }

            this.pieChartInstance = new Chart(this.$refs.canvas.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['Recorded a sale', 'No sales yet'],
                    datasets: [{ data: chartData, backgroundColor: colors, borderWidth: 0 }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: !this.isEmpty },
                    },
                },
            });
        },
    };
}
