// src/lib/register-chart.js

import {
    Chart, LineController, LineElement, PointElement,
    LinearScale, CategoryScale, Filler, Tooltip
} from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip);
export { Chart };
