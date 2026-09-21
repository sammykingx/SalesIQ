// app/src/entries/metrics/index.js

import { revenueTrendChart } from "./revenue-chart";
import { busiestDaysChart } from "./busiest-day";
import { platformGmvChart } from "./platform-gmv-chart";
import { platformAdoptionChart } from "./adoption-chart";

export function initMetricsModule(Alpine) {
    Alpine.data("revenueTrendChart", revenueTrendChart);
    Alpine.data("busiestDaysChart", busiestDaysChart);
    Alpine.data("platformGmvChart", platformGmvChart);
    Alpine.data("platformAdoptionChart", platformAdoptionChart);
}
