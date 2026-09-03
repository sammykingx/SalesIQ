import "../styles/theme.css";
import "../styles/keyframes.css";

import Alpine from "alpinejs";

import { createIcons, BarChart2, ChevronRight, FileText, LayoutDashboard, Lock, Link, ShoppingCart, Store, User, Users } from "lucide";

import { initAuthModule } from "./auth/index.js";
import { initComponentsModule } from "./components/index.js";
import { initOnboarding } from "./onboarding/index.js.js";

/* register alpine components before start */
initAuthModule(Alpine);
initComponentsModule(Alpine);
initOnboarding(Alpine);


createIcons({
    icons: { BarChart2, ChevronRight, FileText, LayoutDashboard, Lock, Link, ShoppingCart, Store, User, Users },
    attrs: { 'stroke-width': 1.75 },
});

window.Alpine = Alpine;
Alpine.start();
