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

## ✅ All Tests Passed?

If all checks pass, your E-Commerce Store is working perfectly! 🎉

**Next Steps**:
1. Explore the API at http://localhost:8000/api/docs
2. Review the code structure
3. Start implementing Phase 4: Shopping Cart
4. Add more products/categories as needed

## 📝 Notes

Add any observations or issues you find:

---

**Testing Date**: _______________
**Tester**: _______________
**Browser**: _______________
**OS**: _______________
