const ALLOWED_VERBS = ['POST', 'PATCH', 'PUT', 'DELETE'];
const VERBS_REQUIRING_PAYLOAD = ['POST', 'PATCH', 'PUT'];

/**
 * Validates args before an API request is made.
 * Throws on invalid input rather than failing silently —
 * callers should catch this separately from network/response errors.
 */
export function validateApiRequest({ endpoint, httpVerb, data }) {
    if (typeof endpoint !== 'string' || endpoint.trim() === '') {
        throw new Error('validateApiRequest: "endpoint" must be a non-empty string.');
    }

    const verb = httpVerb?.toUpperCase();
    if (!ALLOWED_VERBS.includes(verb)) {
        throw new Error(
            `validateApiRequest: "httpVerb" must be one of ${ALLOWED_VERBS.join(', ')}.`
        );
    }

    const isEmpty =
        data === undefined ||
        data === null ||
        (typeof data === 'object' && Object.keys(data).length === 0);

    if (VERBS_REQUIRING_PAYLOAD.includes(verb) && isEmpty) {
        throw new Error(`validateApiRequest: "data" cannot be empty for ${verb} requests.`);
    }

    return { endpoint: endpoint.trim(), httpVerb: verb, data: data ?? {} };
}