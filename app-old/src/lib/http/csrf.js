/**
 * Retrieves the CSRF token, checking common Django rendering locations
 * in order of proximity: body dataset -> meta tag in head -> cookie.
 * Returns null if none is found.
 */
export function getCsrfToken() {
    // 1. Check body dataset, e.g. <body data-csrf-token="{{ csrf_token }}">
    const bodyToken = document.body?.dataset?.csrfToken;
    if (bodyToken) return bodyToken;

    // 2. Check meta tag in head, e.g. <meta name="csrf-token" content="{{ csrf_token }}">
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag?.content) return metaTag.content;

    // 3. Fall back to the csrftoken cookie Django sets by default
    const cookieToken = getCookie('csrftoken');
    if (cookieToken) return cookieToken;

    return null;
}

function getCookie(name) {
    const match = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));
    return match ? decodeURIComponent(match.split('=')[1]) : null;
}