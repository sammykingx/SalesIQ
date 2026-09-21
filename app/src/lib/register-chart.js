// src/lib/register-chart.js

import {
    Chart, LineController, LineElement, PointElement,
    LinearScale, CategoryScale, Filler, Tooltip,
    BarController, BarElement, PieController, ArcElement,
} from 'chart.js';

Chart.register(
    LineController, LineElement, PointElement, LinearScale,
    CategoryScale, Filler, Tooltip, BarController, BarElement,
    PieController, ArcElement,
);

Chart.defaults.color = '#a3a3a3';
Chart.defaults.font.weight = '400';
Chart.defaults.font.size = 11;

export { Chart };
