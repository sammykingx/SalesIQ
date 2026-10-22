// app/src/entries/metrics/index.js

import { revenueTrendChart } from "./business/revenue-chart";
import { busiestDaysChart } from "./business/busiest-day";
import { platformGmvChart } from "./platform/platform-gmv-chart";
import { platformAdoptionChart } from "./platform/adoption-chart";
import { leaderboardComponent } from "./platform/leaderboard";

export function initMetricsModule(Alpine) {
    Alpine.data("revenueTrendChart", revenueTrendChart);
    Alpine.data("busiestDaysChart", busiestDaysChart);
    Alpine.data("platformGmvChart", platformGmvChart);
    Alpine.data("platformAdoptionChart", platformAdoptionChart);
    Alpine.data('leaderboardComponent', leaderboardComponent);
}
