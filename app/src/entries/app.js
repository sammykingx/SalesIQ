import "../styles/theme.css";
import "../styles/keyframes.css";

import Alpine from "alpinejs";

import { createIcons, icons } from "lucide";

import { initAuthModule } from "./auth/index.js";
import { initComponentsModule } from "./components/index.js";

/* register alpine components before start */
initAuthModule(Alpine);
initComponentsModule(Alpine);



window.Alpine = Alpine;
Alpine.start();

createIcons({ icons });
