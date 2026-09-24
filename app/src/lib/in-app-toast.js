import { createIcons, CheckCircle2, AlertTriangle, AlertCircle, Info, X } from 'lucide';

export function inAppToast(title, message = '', type = 'success', duration = 4000) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'pointer-events-none fixed top-4 inset-x-4 z-50 flex flex-col gap-3 sm:top-5 sm:right-5 sm:left-auto sm:w-full sm:max-w-sm';
        document.body.appendChild(container);
    }

    const styles = {
        success: {
            border: 'border-emerald-200/80 dark:border-emerald-900/40',
            iconBg: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400',
            barBg: 'bg-emerald-500',
            iconName: 'check-circle-2'
        },
        error: {
            border: 'border-rose-200/80 dark:border-rose-900/40',
            iconBg: 'bg-rose-100 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400',
            barBg: 'bg-rose-500',
            iconName: 'alert-triangle'
        },
        warning: {
            border: 'border-amber-200/80 dark:border-amber-900/40',
            iconBg: 'bg-amber-100 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400',
            barBg: 'bg-amber-500',
            iconName: 'alert-circle'
        },
        info: {
            border: 'border-indigo-200/80 dark:border-indigo-900/40',
            iconBg: 'bg-indigo-100 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400',
            barBg: 'bg-indigo-500',
            iconName: 'info'
        }
    };

    const currentStyle = styles[type] || styles.success;

    const toast = document.createElement('div');
    toast.className = `pointer-events-auto relative overflow-hidden rounded-2xl border bg-white/95 p-4 shadow-xl backdrop-blur-md dark:bg-neutral-900/95 dark:border-neutral-800 ${currentStyle.border} transition-all duration-300 opacity-0 translate-y-[-12px] sm:translate-y-0 sm:translate-x-8 scale-95`;

    toast.innerHTML = `
        <div class="flex items-start gap-3">
            <div class="shrink-0 pt-0.5">
                <div class="flex h-7 w-7 items-center justify-center rounded-xl ${currentStyle.iconBg}">
                    <i data-lucide="${currentStyle.iconName}" class="h-4 w-4"></i>
                </div>
            </div>
            <div class="flex-1 pr-2">
                <h4 class="text-xs font-medium text-neutral-900 dark:text-white">${title}</h4>
                ${message ? `<p class="mt-0.5 text-[11px] text-neutral-500 dark:text-neutral-400">${message}</p>` : ''}
            </div>
            <button type="button" class="toast-close shrink-0 rounded-lg p-1 text-neutral-400 hover:bg-neutral-100 hover:text-neutral-600 dark:hover:bg-neutral-800 dark:hover:text-neutral-200">
                <i data-lucide="x" class="h-3.5 w-3.5"></i>
            </button>
        </div>
        <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-neutral-100 dark:bg-neutral-800">
            <div class="toast-progress h-full transition-all ease-linear ${currentStyle.barBg}" style="width: 100%; transition-duration: ${duration}ms;"></div>
        </div>
    `;

    container.appendChild(toast);

    // Render icons specifically for this newly injected toast element
    createIcons({
        icons: {
            CheckCircle2,
            AlertTriangle,
            AlertCircle,
            Info,
            X
        },
        root: toast,
        attrs: { 'stroke-width': 1.75 }
    });

    // Trigger enter animation
    requestAnimationFrame(() => {
        toast.classList.remove('opacity-0', 'translate-y-[-12px]', 'sm:translate-x-8', 'scale-95');
        toast.classList.add('opacity-100', 'translate-y-0', 'sm:translate-x-0', 'scale-100');
        toast.querySelector('.toast-progress').style.width = '0%';
    });

    const remove = () => {
        toast.classList.add('opacity-0', 'scale-95');
        setTimeout(() => toast.remove(), 200);
    };

    let dismissTimer = setTimeout(remove, duration);

    toast.addEventListener('mouseenter', () => {
        clearTimeout(dismissTimer);
        const bar = toast.querySelector('.toast-progress');
        bar.style.transitionDuration = '0ms';
        bar.style.width = window.getComputedStyle(bar).width;
    });

    toast.addEventListener('mouseleave', () => {
        const bar = toast.querySelector('.toast-progress');
        const currentWidth = parseFloat(bar.style.width);
        const remainingTime = (currentWidth / 100) * duration;
        bar.style.transitionDuration = `${remainingTime}ms`;
        bar.style.width = '0%';
        dismissTimer = setTimeout(remove, remainingTime);
    });

    toast.querySelector('.toast-close').addEventListener('click', () => {
        clearTimeout(dismissTimer);
        remove();
    });
}
