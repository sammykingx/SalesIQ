const DEFAULTS = {
    selector: '#app-preloader',
    minDisplayMs: 900,
    maxWaitMs: 3000,
};

export function initPreloader(options = {}) {
    const config = { ...DEFAULTS, ...options };
    const el = document.querySelector(config.selector);
    if (!el) return null;

    const start = Date.now();
    let hidden = false;

    function hide() {
        if (hidden) return;
        hidden = true;

        const elapsed = Date.now() - start;
        const wait = Math.max(config.minDisplayMs - elapsed, 0);

        setTimeout(() => {
            el.classList.add('is-hidden');
            el.addEventListener('transitionend', () => el.remove(), { once: true });
        }, wait);
    }

    window.addEventListener('load', hide);
    setTimeout(hide, config.maxWaitMs);

    return { hide };
}
