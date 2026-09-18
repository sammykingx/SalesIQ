// app/src/entries/metrice/index.js

import { revenueTrendChart } from "./revenue-chart";

export function initMetricsModule(Alpine) {
    Alpine.data("revenueTrendChart", revenueTrendChart);

}
