let cart_list = [];

try {
  cart_list = JSON.parse(localStorage.getItem('cart_list')) || [];
} catch (e) {
  cart_list = [];
}

function addToCart(btn) {
  let card = btn.closest('.card'); // safer
  let title = card.querySelector('.title')?.innerText.trim() || 'Unknown';
  let priceText = card.querySelector('.price')?.innerText.trim() || '$0';
  let image = card.querySelector('.product-image')?.src || '';

  let price = parseFloat(priceText.replace('$', '')) || 0;

  let existingItem = cart_list.find(item => item.title === title);

  if (existingItem) {
    existingItem.quantity++;
  } else {
    cart_list.push({
      title,
      quantity: 1,
      price,
      image
    });
  }

  localStorage.setItem('cart_list', JSON.stringify(cart_list));

  Swal.fire({
    icon: 'success',
    title: 'Added to cart!',
    timer: 1200,
    showConfirmButton: false
  });

  updateCart();
}

function updateCart() {
  try {
    cart_list = JSON.parse(localStorage.getItem('cart_list')) || [];
  } catch (e) {
    cart_list = [];
  }

  const cart_count = document.querySelector('.cartNumber');

  // Show total quantity, not just item count
  let totalQty = cart_list.reduce((sum, item) => sum + item.quantity, 0);
  if (cart_count) {
    cart_count.innerText = totalQty;
  }
}