import "../styles/theme.css";
import "../styles/keyframes.css";

import Alpine from "alpinejs";

import { createIcons, icons } from "lucide";

window.Alpine = Alpine;
Alpine.start();
createIcons({ icons });
console.log("Hello from app.js!");
