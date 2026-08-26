import "../styles/theme.css";
import "../styles/keyframes.css";

import Alpine from "alpinejs";

import { createIcons, icons } from "lucide";

import { initAuthModule } from "./auth/index.js";

/* register auth alpine componetns before start */
initAuthModule(Alpine);



window.Alpine = Alpine;
Alpine.start();

createIcons({ icons });
