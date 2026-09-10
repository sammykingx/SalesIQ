// app/src/entries/products/index.js
import { addProductForm } from './add-products.js';
import { allProductsComponent } from './all-products.js';
import { modifyProductComponent } from './update.js';

export function initProductsModule(Alpine) {
    Alpine.data('addProductForm', addProductForm);
    Alpine.data('allProductsComponent', allProductsComponent);
    Alpine.data('modifyProductComponent', modifyProductComponent);
}