import { getCsrfToken } from './csrf.js';
import { validateApiRequest } from './validators.js';

/**
 * Thin wrapper around fetch for mutating requests (POST/PATCH/PUT/DELETE).
 * Validates args, attaches CSRF token + JSON headers, and returns the raw
 * Response object — callers are responsible for handling status codes
 * (2xx, 403, 500, etc.) and parsing the body.
 *
 * @param {string} endpoint
 * @param {string} httpVerb - one of POST, PATCH, PUT, DELETE
 * @param {object} [data]
 * @returns {Promise<Response>}
 */
export async function apiRequest(endpoint, httpVerb, data) {
    const validated = validateApiRequest({ endpoint, httpVerb, data });

    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        console.warn('apiRequest: no CSRF token found — request will likely be rejected.');
    }

    const options = {
        method: validated.httpVerb,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken ?? '',
            'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin',
    };

    if (validated.httpVerb !== 'DELETE' || Object.keys(validated.data).length > 0) {
        options.body = JSON.stringify(validated.data);
    }

    return fetch(validated.endpoint, options);
}