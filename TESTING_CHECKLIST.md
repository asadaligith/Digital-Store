# Testing Checklist

Use this checklist to verify your E-Commerce Store is working correctly.

## ✅ Pre-Testing Setup

- [ ] MongoDB is running (docker ps shows mongodb container)
- [ ] Backend virtual environment is activated
- [ ] Backend dependencies installed (pip list shows fastapi, motor, etc.)
- [ ] Frontend dependencies installed (node_modules/ exists)
- [ ] Database seeded (shows 5 categories, 20 products)
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:5173

## 🌐 Browser Testing

### 1. Backend API Documentation

**URL**: http://localhost:8000/api/docs

**Checks**:
- [ ] Swagger UI loads successfully
- [ ] Shows "E-Commerce Store" title
- [ ] See Products and Categories sections
- [ ] Endpoints are expandable and show request/response schemas

**Try**:
- [ ] Click "GET /api/products" → "Try it out" → "Execute"
- [ ] Should return 200 OK with list of products
- [ ] Click "GET /api/categories" → "Try it out" → "Execute"
- [ ] Should return 200 OK with list of categories

### 2. Health Check

**URL**: http://localhost:8000/health

**Expected Response**:
```json
{
  "status": "healthy",
  "app": "E-Commerce Store",
  "version": "1.0.0",
  "environment": "development"
}
```

**Checks**:
- [ ] Returns 200 OK
- [ ] Shows correct app name and version
- [ ] Status is "healthy"

### 3. Frontend - Home Page

**URL**: http://localhost:5173/

**Checks**:
- [ ] Page loads without errors
- [ ] See "Welcome to E-Commerce Store" heading
- [ ] See "Shop Now" button
- [ ] Header shows logo and navigation
- [ ] Footer displays with newsletter signup
- [ ] Page is responsive (try resizing window)

**Try**:
- [ ] Click "Shop Now" button → Should navigate to /products

### 4. Frontend - Products Page

**URL**: http://localhost:5173/products

**Checks**:
- [ ] Page loads without errors
- [ ] Shows "Products" heading
- [ ] Shows product count (should be ~20 products)
- [ ] Product grid displays (1-4 columns based on screen width)
- [ ] Each product card shows:
  - [ ] Product image
  - [ ] Product name
  - [ ] Price
  - [ ] Rating stars
  - [ ] "Add to Cart" button
- [ ] Filters sidebar visible on left
- [ ] Sort dropdown shows on top right

**Animations**:
- [ ] Products fade/slide in when page loads (stagger effect)
- [ ] Product cards lift up on hover
- [ ] Smooth transitions

**Try Filtering**:
- [ ] Click a category checkbox (e.g., "Electronics")
  - [ ] Products update to show only that category
  - [ ] URL updates with ?category=electronics
  - [ ] Product count updates

- [ ] Set price range (e.g., Min: 50, Max: 200)
  - [ ] Click "Apply" button
  - [ ] Products filter to price range
  - [ ] URL updates with ?min_price=50&max_price=200

- [ ] Select minimum rating (e.g., 4 stars)
  - [ ] Products filter to 4+ rating
  - [ ] URL updates

- [ ] Check "In Stock Only"
  - [ ] Only in-stock products show
  - [ ] Out of stock products hidden

- [ ] Click "Clear All" button
  - [ ] All filters reset
  - [ ] Shows all products again

**Try Sorting**:
- [ ] Select "Price: Low to High"
  - [ ] Products re-order by price ascending
  - [ ] Lowest price first

- [ ] Select "Price: High to Low"
  - [ ] Products re-order by price descending
  - [ ] Highest price first

- [ ] Select "Highest Rated"
  - [ ] Products sorted by rating

**Try Pagination**:
- [ ] If more than 20 products, pagination shows at bottom
- [ ] Click "Next" or page number
- [ ] Products update
- [ ] URL updates with ?page=2
- [ ] Page scrolls to top

**Try Search** (in header):
- [ ] Type a product name (e.g., "headphones") in search bar
- [ ] Press Enter
- [ ] Navigate to products page with search results
- [ ] URL shows ?search=headphones

### 5. Frontend - Product Detail Page

**URL**: Click any product card OR navigate to http://localhost:5173/products/wireless-bluetooth-headphones

**Checks**:
- [ ] Page loads without errors
- [ ] Breadcrumb shows: Home / Products / Product Name
- [ ] Large product image displays
- [ ] Product name shows as page heading
- [ ] Rating stars and review count visible
- [ ] Price displayed (with discount if applicable)
- [ ] SKU number shows
- [ ] Stock status shows (In Stock / Low Stock / Out of Stock)
- [ ] Full product description displays
- [ ] Quantity selector shows (+ and - buttons)
- [ ] "Add to Cart" button shows

**Try**:
- [ ] Click thumbnail images (if multiple)
  - [ ] Main image updates

- [ ] Click + button on quantity
  - [ ] Quantity increases

- [ ] Click - button on quantity
  - [ ] Quantity decreases (stops at 1)

- [ ] Click "Add to Cart"
  - [ ] Button shows loading state
  - [ ] Console logs "Add to cart: ..." (cart not implemented yet)

- [ ] Click breadcrumb "Products"
  - [ ] Navigate back to products page

### 6. Mobile Responsiveness

**Resize browser to mobile width (< 768px)**:

**Home Page**:
- [ ] Layout stacks vertically
- [ ] Header shows hamburger menu icon
- [ ] Click hamburger → mobile menu opens
- [ ] Navigation links visible in mobile menu

**Products Page**:
- [ ] Product grid shows 1 column
- [ ] Filters collapse into accordion
- [ ] Click "Filters" → filter panel expands
- [ ] Sort dropdown visible
- [ ] Pagination buttons adjust for mobile

**Product Detail**:
- [ ] Image gallery stacks vertically
- [ ] Product info below image
- [ ] All buttons remain touch-friendly (≥44px)

### 7. Accessibility Testing

**Keyboard Navigation**:
- [ ] Press Tab to navigate
- [ ] All interactive elements are focusable
- [ ] Focus visible (blue ring appears)
- [ ] Can activate buttons with Enter/Space
- [ ] Can navigate pagination with keyboard

**Screen Reader** (if available):
- [ ] Product cards announce product name
- [ ] Buttons have descriptive labels
- [ ] Form inputs have labels
- [ ] Images have alt text

## 🐛 Common Issues & Solutions

### Issue: "Cannot connect to MongoDB"
**Solution**:
```bash
docker-compose up -d
docker ps  # Verify it's running
```

### Issue: "Module not found" errors in backend
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: Frontend shows blank page
**Solution**:
- Check browser console for errors
- Ensure backend is running
- Check VITE_API_BASE_URL in frontend/.env

### Issue: "CORS" errors in browser console
**Solution**:
- Verify backend CORS_ORIGINS includes http://localhost:5173
- Restart backend server

### Issue: Products don't load
**Solution**:
1. Check backend is running: http://localhost:8000/health
2. Test API directly: http://localhost:8000/api/products
3. Check browser Network tab for failed requests
4. Verify MongoDB has data: `python -m src.scripts.seed_data`

## 📊 Performance Checks

- [ ] Products page loads in < 2 seconds
- [ ] Filtering/sorting updates in < 500ms
- [ ] Page transitions are smooth (60fps)
- [ ] Images lazy load as you scroll
- [ ] No console errors in browser dev tools
- [ ] No console warnings about missing keys/props

## 🛒 Phase 4: Shopping Cart Testing

### 8. Backend - Cart API Endpoints

**URL**: http://localhost:8000/api/docs

**Checks**:
- [ ] Cart section appears in Swagger UI
- [ ] See 7 cart endpoints (GET cart, POST items, PATCH items, DELETE items, etc.)
- [ ] All endpoints expandable with request/response schemas

**Try**:
- [ ] Click "GET /api/cart" → "Try it out" → "Execute"
  - [ ] Returns 200 OK with empty cart
  - [ ] Shows session_id cookie in response headers
  - [ ] item_count is 0, subtotal is 0.0

- [ ] Click "POST /api/cart/items" → "Try it out"
  - [ ] Enter product_id from products list
  - [ ] Set quantity to 2
  - [ ] Execute → Returns 201 Created
  - [ ] Cart now has 1 item with quantity 2
  - [ ] Subtotal calculated correctly

- [ ] Click "GET /api/cart/summary" → "Try it out" → "Execute"
  - [ ] Returns item_count and subtotal
  - [ ] Matches full cart data

- [ ] Click "PATCH /api/cart/items/{product_id}" → Update quantity to 5
  - [ ] Returns 200 OK with updated cart
  - [ ] Quantity changed to 5
  - [ ] Subtotal recalculated

- [ ] Click "DELETE /api/cart/items/{product_id}" → Remove item
  - [ ] Returns 200 OK
  - [ ] Item removed from cart
  - [ ] Cart now empty

### 9. Frontend - Cart Badge (Header)

**Location**: Header navigation (top right)

**Checks**:
- [ ] Cart icon visible in header
- [ ] Badge shows "0" initially (or empty)
- [ ] Badge is clickable
- [ ] Clicking navigates to /cart page

**Try**:
- [ ] Add item to cart from Products page
  - [ ] Badge updates immediately
  - [ ] Shows correct item count
  - [ ] Badge color is primary-600
  - [ ] Count displays "99+" if > 99 items

### 10. Frontend - Add to Cart (Products Page)

**URL**: http://localhost:5173/products

**Checks**:
- [ ] "Add to Cart" button on each product card
- [ ] Button shows loading state when clicked
- [ ] Button disabled for out-of-stock items

**Try**:
- [ ] Click "Add to Cart" on any product
  - [ ] Button shows loading spinner briefly
  - [ ] Cart badge in header updates (+1)
  - [ ] No page reload
  - [ ] Can add same product multiple times (quantity increases)

- [ ] Try to add out-of-stock product
  - [ ] Button is disabled or shows "Out of Stock"
  - [ ] Cannot add to cart

### 11. Frontend - Add to Cart (Product Detail Page)

**URL**: http://localhost:5173/products/{any-product-slug}

**Checks**:
- [ ] Quantity selector with + and - buttons
- [ ] "Add to Cart" button visible
- [ ] Quantity defaults to 1
- [ ] Stock status shows correctly

**Try**:
- [ ] Click + button to increase quantity to 3
  - [ ] Quantity updates
  - [ ] Cannot exceed inventory quantity
  - [ ] - button disabled when quantity is 1

- [ ] Click "Add to Cart" with quantity 3
  - [ ] Button shows loading state
  - [ ] Cart badge updates by +3
  - [ ] Success (or could show toast notification)

- [ ] Try to set quantity > inventory
  - [ ] + button disabled when at max
  - [ ] Or shows error message

### 12. Frontend - Cart Page

**URL**: http://localhost:5173/cart

**Empty Cart Checks**:
- [ ] Shows empty cart icon/illustration
- [ ] Message: "Your cart is empty"
- [ ] "Continue Shopping" button visible
- [ ] Button navigates to /products

**With Items Checks**:
- [ ] Cart page shows all items
- [ ] Each item shows:
  - [ ] Product image (clickable to product detail)
  - [ ] Product name (clickable to product detail)
  - [ ] Price per unit
  - [ ] Quantity selector (+ and - buttons)
  - [ ] Remove button
  - [ ] Item total (price × quantity)
  - [ ] Stock status if low/out

- [ ] Cart summary sidebar shows:
  - [ ] Subtotal with item count
  - [ ] Shipping (FREE if > $50, else $5.99)
  - [ ] Estimated tax (8%)
  - [ ] Total
  - [ ] "Proceed to Checkout" button
  - [ ] "Continue Shopping" link
  - [ ] Security badge

**Try**:
- [ ] Click + to increase quantity
  - [ ] Quantity updates immediately
  - [ ] Item total recalculates
  - [ ] Subtotal recalculates
  - [ ] Total recalculates
  - [ ] Cart badge updates in header

- [ ] Click - to decrease quantity
  - [ ] Quantity decreases
  - [ ] All totals update
  - [ ] Cannot go below 1

- [ ] Click "Remove" button
  - [ ] Confirmation or immediate removal
  - [ ] Item disappears from cart
  - [ ] Totals update
  - [ ] Cart badge updates

- [ ] Click "Clear Cart" button
  - [ ] Shows confirmation modal
  - [ ] "Cancel" button closes modal
  - [ ] "Clear Cart" button empties cart
  - [ ] Redirects to empty cart state

- [ ] Click product image or name
  - [ ] Navigates to product detail page
  - [ ] Cart persists (still has items)

- [ ] Test free shipping threshold
  - [ ] Add items totaling < $50 → Shipping shows $5.99
  - [ ] Add more items > $50 → Shipping shows FREE
  - [ ] Message shows how much more needed for free shipping

### 13. Cart Persistence Testing

**Checks**:
- [ ] Add items to cart
- [ ] Refresh page (F5)
  - [ ] Cart items persist
  - [ ] Cart badge shows correct count
  - [ ] Navigate to /cart → items still there

- [ ] Close browser and reopen
  - [ ] Cart items persist (session cookie)
  - [ ] Badge shows correct count

- [ ] Wait 7 days (or manually delete cart in DB)
  - [ ] Cart should expire and be cleaned up

### 14. Cart Error Handling

**Try**:
- [ ] Add product with quantity > inventory
  - [ ] Shows error message
  - [ ] Does not add to cart

- [ ] Delete product from DB while in cart
  - [ ] Cart shows gracefully (missing product)
  - [ ] Or shows "Product unavailable"

- [ ] Update item to quantity 0
  - [ ] Item is removed from cart
  - [ ] Same as clicking "Remove"

### 15. Mobile Cart Testing

**Resize browser to mobile width (< 768px)**:

**Cart Page**:
- [ ] Cart summary moves below items (stacked layout)
- [ ] Quantity controls remain touch-friendly (≥44px)
- [ ] Item images resize appropriately
- [ ] "Remove" button accessible
- [ ] All buttons remain tappable

**Cart Badge**:
- [ ] Visible in mobile header
- [ ] Badge position correct
- [ ] Tappable (≥44px)

## ✅ All Tests Passed?

If all checks pass, your E-Commerce Store with Shopping Cart is working perfectly! 🎉

**Phase 4 Complete** ✅

**Next Steps**:
1. Explore the Cart API at http://localhost:8000/api/docs
2. Test cart functionality thoroughly
3. Start implementing Phase 5: Checkout
4. Add authentication (Phase 7) for cart merging

## 📝 Notes

Add any observations or issues you find:

---

**Testing Date**: _______________
**Tester**: _______________
**Browser**: _______________
**OS**: _______________
