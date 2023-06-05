$(document).ready(function() {
  $('#weatherFilterCheck').change(function() {
    if(this.checked) {
      // Get only products suitable for current weather
      $.get('/weather_clothes/', function(data) {
        updateProductList(data);
      });
    } else {
      // Get all products
      $.get('/all-clothes/', function(data) {
        updateProductList(data);
      });
    }
  });
});

function updateProductList(data) {
  // Clear the current list of products
  $('.row').empty();

  // Add the suitable products to the list
  for (let product of data) {
    $('.row').append(`
      <div class="col-md-4">
        <figure class="card card-product-grid">
          <div class="img-wrap">
            <a href="${product.get_url}"><img src="${product.images.url}"></a>
          </div>
          <figcaption class="info-wrap">
            <div class="fix-height">
              <a href="${product.get_url}" class="title">${product.product_name}</a>
              <div class="price-wrap mt-2">
                <span class="price">$ ${product.price}</span>
              </div>
            </div>
            <a href="${product.get_url}" class="btn btn-block btn-primary">Подробнее</a>
          </figcaption>
        </figure>
      </div>
    `);
  }
}
