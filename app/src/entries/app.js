// app/src/entries/app.js
// vite entry point

import "../styles/theme.css";
import "../styles/keyframes.css";

import Alpine from "alpinejs";

import {
    createIcons, BarChart2, ChevronRight, FileText, LayoutDashboard, Lock,
    Link, ShoppingCart, Store, User, Users, Settings, LogOut, Globe, Languages,
    Check, LockOpen, ShieldCheck, Eye, EyeOff, CheckCircle2, XCircle, Timer, Save,
    AlertTriangle, AlertCircle, Info, X, KeyRound, ShieldAlert, Share2, MessageSquare,
    Phone, Trash2, TriangleAlert, PackagePlus, Box, Download, Briefcase, Bold, Italic,
    List, ListOrdered, Plus, UserCheck, UserPlus, ExternalLink,
} from "lucide";

import { initAuthModule } from "./auth/index.js";
import { initComponentsModule } from "./components/index.js";
import { initOnboarding } from "./onboarding/index.js";
import { inAppToast } from "../lib/in-app-toast.js";

import { initAccountsModule } from "./accounts";
import { initCustomerModule } from "./customers";
import { initProductsModule } from "./products";
import { initSalesModule } from "./sales";
import { initMetricsModule } from "./metrics/index.js";


initAuthModule(Alpine);
initComponentsModule(Alpine);
initOnboarding(Alpine);
initAccountsModule(Alpine);
initCustomerModule(Alpine);
initProductsModule(Alpine);
initSalesModule(Alpine);
initMetricsModule(Alpine);


createIcons({
    icons: {
        BarChart2, ChevronRight, FileText, LayoutDashboard, Lock,
        Link, ShoppingCart, Store, User, Users, Settings, LogOut,
        Globe, Languages, Check, LockOpen, ShieldCheck, Eye, EyeOff,
        CheckCircle2, XCircle, AlertTriangle, AlertCircle, Info, X,
        KeyRound, ShieldAlert, Timer, Share2, MessageSquare, Save,
        Phone, Trash2, TriangleAlert, PackagePlus, Box, Download,
        Briefcase, Bold, Italic, List, ListOrdered, Plus, UserCheck,
        UserPlus, ExternalLink
    },
    attrs: { 'stroke-width': 1.75 },
});

window.Alpine = Alpine;
window.inAppToast = inAppToast;

Alpine.start();

