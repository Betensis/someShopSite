const csrfTokenSelector = 'input[name=csrfmiddlewaretoken]';

/**
 *
 * @param {Element} form
 * @return {{name: string, value:string}}
 */
export function getCSRF(form) {
    const csrfInput = form.querySelector(csrfTokenSelector);
    return {
        name: csrfInput.getAttribute('name'),
        value: csrfInput.getAttribute('value'),
    }
}