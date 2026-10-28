import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import "lenis/dist/lenis.css";

gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();

// Everything lives inside this query, so visitors who ask for reduced
// motion get native scrolling and fully visible content.
mm.add("(prefers-reduced-motion: no-preference)", () => {

    /* ---------- Smooth scroll (Lenis driven by GSAP's ticker) ---------- */
    const lenis = new Lenis({
        anchors: { offset: -96 },   // nav links stop below the floating header
    });
    lenis.on("scroll", ScrollTrigger.update);

    const tick = (time) => lenis.raf(time * 1000);
    gsap.ticker.add(tick);
    gsap.ticker.lagSmoothing(0);

    /* ---------- Hero: entrance on load ---------- */
    gsap.from("[data-hero]", {
        opacity: 0,
        y: 28,
        duration: 0.9,
        ease: "power3.out",
        stagger: 0.12,
        delay: 0.1,
    });

    /* ---------- Hero: exit as you scroll past ---------- */
    gsap.to("[data-hero-content]", {
        opacity: 0,
        yPercent: -10,
        ease: "none",
        scrollTrigger: {
            trigger: "[data-hero-content]",
            start: "top top",
            end: "bottom 25%",
            scrub: true,
        },
    });

    /* ---------- Sections: reveal on enter, fade back out when scrolling up ---------- */
    gsap.set("[data-reveal]", { opacity: 0, y: 32 });

    ScrollTrigger.batch("[data-reveal]", {
        start: "top 88%",
        onEnter: (els) =>
            gsap.to(els, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                ease: "power3.out",
                stagger: 0.1,
                overwrite: true,
            }),
        onLeaveBack: (els) =>
            gsap.to(els, {
                opacity: 0,
                y: 32,
                duration: 0.4,
                ease: "power2.in",
                overwrite: true,
            }),
    });

    // Images and fonts shift layout after load; recalculate trigger positions.
    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener("load", refresh);

    // Cleanup if the user flips the reduced-motion setting mid-visit.
    return () => {
        window.removeEventListener("load", refresh);
        gsap.ticker.remove(tick);
        lenis.destroy();
    };
});
