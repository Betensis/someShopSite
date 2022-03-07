import {addProductToCart} from "../api/cart.js";
import {getCSRF} from "../lib/csrf.js";

const addToCartBtn = document.querySelector('.js-add-product-to-cart');

addToCartBtn.addEventListener(
    'click',
    addToCart
);

function addToCart() {
    const productSizeForm = document.querySelectorAll('.form-check');
    const productCode = parseInt(document.querySelector('.js-product-code').textContent);
    let productSize;
    productSizeForm.forEach(
        productSizeData => {
            const productSizeInput = productSizeData.querySelector('.js-product-size-input[type="radio"]');
            if (productSizeInput.checked) {
                productSize = productSizeData.querySelector('.js-product-size-value').textContent.trim();
            }
        }
    )
    if (typeof productSize === 'undefined') {
        showErrors([
            'Не выбран размер'
        ])
        return;
    }
    const csrf = getCSRF(document.querySelector('.product-size-container'));
    addProductToCart(productCode, productSize, csrf).then(
        response => {
            if (response.ok)
            {
                window.location.reload();
            }
            if (response.statusText === 'Unauthorized')
            {
                window.location.href = '/account/login/?next=' + window.location.pathname;
            }
        }
    )
}

/**
 *
 * @param {string[]} errors
 */
function showErrors(errors) {
    let priviesErrorContainer = document.querySelector('.errorContainer');
    if (priviesErrorContainer !== null) {
       priviesErrorContainer.parentNode.removeChild(priviesErrorContainer);
    }

    let errorContainer = document.createElement('div');
    errorContainer.classList.add('errorContainer');

    for (let error of errors) {
        const errorElement = document.createElement('p');
        errorElement.classList.add('invalid-feedback');
        errorElement.textContent = error;
        errorContainer.appendChild(errorElement);
    }

    document.querySelector('.product-main-info__data').appendChild(
        errorContainer
    );
}