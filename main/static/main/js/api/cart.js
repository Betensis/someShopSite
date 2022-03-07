/**
 *
 * @param {int} product_id
 * @param {string} size
 * @param {{name: string, value:string}} csrf
 * @return {Promise<Response>}
 */
export function addProductToCart(product_id, size, csrf) {
    let formData = new FormData();
    formData.append('id', product_id.toString());
    formData.append('size', size);
    formData.append(csrf.name, csrf.value);
    return fetch(
        '/api/v1/cart/add-products',
        {
            method: 'post',
            body: formData
        }
    );
}