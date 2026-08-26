// src/lib/lottie/lottie.js
import lottie from "lottie-web";

/**
 * Initializes a Lottie animation on a container element.
 * @param {HTMLElement|string} target - element or selector
 * @param {string} path - URL to the animation JSON (from data-attribute)
 * @param {object} [options]
 * @param {boolean} [options.loop=true]
 * @param {boolean} [options.autoplay=true]
 * @param {"svg"|"canvas"|"html"} [options.renderer="svg"]
 */
export function initLottie(target, path, options = {}) {
    const container = typeof target === "string" ? document.querySelector(target) : target;
    if (!container || !path) return null;

    // Respect reduced-motion preference
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const anim = lottie.loadAnimation({
        container,
        path,
        renderer: options.renderer ?? "svg",
        loop: options.loop ?? true,
        autoplay: prefersReducedMotion ? false : (options.autoplay ?? true),
    });

    if (prefersReducedMotion) {
        anim.goToAndStop(anim.totalFrames - 1, true); // show final frame, static
    }

    return anim; // caller can .destroy() on teardown if needed
}

/**
 * Convenience: reads path from a data-attribute on the container itself,
 * so entry files don't need to know the URL either.
 */
export function initLottieFromDataAttr(target, attr = "data-lottie-src", options = {}) {
    const container = typeof target === "string" ? document.querySelector(target) : target;
    if (!container) return null;
    const path = container.getAttribute(attr);
    return initLottie(container, path, options);
}
