// app/src/entries/metrics/index.js

import { revenueTrendChart } from "./revenue-chart";
import { busiestDaysChart } from "./busiest-day";

export function initMetricsModule(Alpine) {
    Alpine.data("revenueTrendChart", revenueTrendChart);
    Alpine.data("busiestDaysChart", busiestDaysChart);
}
