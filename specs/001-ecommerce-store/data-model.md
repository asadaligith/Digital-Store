# Data Model: E-Commerce Store Platform

**Feature**: E-Commerce Store Platform
**Branch**: `001-ecommerce-store`
**Date**: 2025-12-29
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the MongoDB database schema for all collections in the E-Commerce Store. Each collection is designed following MongoDB best practices with appropriate embedding vs referencing strategies, indexing, and validation rules.

---

## Design Principles

### Embedding vs Referencing Strategy

**Embed When**:
- 1:1 relationships (user profile data)
- 1:few relationships (cart items in cart, order items in order)
- Data always accessed together (order items with order)
- Data doesn't change independently (order snapshot)

**Reference When**:
- 1:many relationships (user → orders, product → reviews)
- Many:many relationships (products ← → categories)
- Data accessed separately (user separate from orders)
- Large/growing arrays (product reviews, order history)

### Denormalization Strategy

**Denormalize** product name and price in `order_items` to preserve historical accuracy (prices change over time, but orders should reflect price at time of purchase).

**Don't Denormalize** product details that change frequently (stock, rating) - use references instead.

---

## Collections

### 1. users

**Purpose**: Store customer account information

**Schema**:

```json
{
  "_id": ObjectId,
  "email": String (unique, indexed),
  "password_hash": String,
  "full_name": String,
  "phone": String (optional),
  "is_email_verified": Boolean (default: false),
  "verification_token": String (optional, expires),
  "reset_token": String (optional, expires),
  "reset_token_expiry": DateTime (optional),
  "failed_login_attempts": Integer (default: 0),
  "lockout_until": DateTime (optional),
  "created_at": DateTime,
  "updated_at": DateTime,
  "last_login_at": DateTime (optional)
}
```

**Indexes**:
```python
db.users.create_index("email", unique=True)
db.users.create_index("verification_token")
db.users.create_index("reset_token")
```

**Validation Rules** (Pydantic):
```python
email: EmailStr (valid email format, unique)
password: Min 8 characters, at least 1 uppercase, 1 lowercase, 1 number
full_name: Min 2 characters, max 100 characters
phone: Optional, E.164 format (e.g., +1234567890)
```

**Relationships**:
- One user has many carts (reference: cart.user_id → user._id)
- One user has many orders (reference: order.user_id → user._id)
- One user has many addresses (reference: address.user_id → user._id)
- One user has many reviews (reference: review.user_id → user._id)

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "email": "john.doe@example.com",
  "password_hash": "$2b$12$KIXvC3DKfGzKbKDVVqMWeu...",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "is_email_verified": true,
  "failed_login_attempts": 0,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-15T12:30:00Z"),
  "last_login_at": ISODate("2025-01-15T12:30:00Z")
}
```

---

### 2. products

**Purpose**: Store product catalog information

**Schema**:

```json
{
  "_id": ObjectId,
  "name": String,
  "slug": String (unique, indexed, URL-friendly),
  "description": String,
  "specifications": Object (flexible key-value pairs),
  "price": Decimal128 (current price),
  "category_id": ObjectId (reference to categories collection),
  "brand": String (optional),
  "sku": String (unique, indexed, stock keeping unit),
  "stock_quantity": Integer (>= 0),
  "is_available": Boolean (derived: stock_quantity > 0),
  "images": Array of Objects [
    {
      "url": String (Cloudinary URL),
      "public_id": String (Cloudinary public_id),
      "alt_text": String,
      "is_primary": Boolean
    }
  ],
  "average_rating": Float (0.0 to 5.0, calculated from reviews),
  "review_count": Integer (denormalized count),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**Indexes**:
```python
db.products.create_index("slug", unique=True)
db.products.create_index("sku", unique=True)
db.products.create_index("category_id")
db.products.create_index([("name", "text"), ("description", "text")])  # Text search
db.products.create_index("price")
db.products.create_index("average_rating")
db.products.create_index("is_available")
```

**Validation Rules** (Pydantic):
```python
name: Min 3 characters, max 200 characters
slug: Lowercase, alphanumeric + hyphens, unique
price: Positive number, max 2 decimal places
stock_quantity: Non-negative integer
images: At least 1 image, max 10 images
average_rating: 0.0 to 5.0
```

**Relationships**:
- One product belongs to one category (reference: product.category_id → category._id)
- One product has many reviews (reference: review.product_id → product._id)
- One product can be in many carts (reference: cart_item.product_id → product._id)
- One product can be in many orders (reference: order_item.product_id → product._id, denormalized)

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "name": "Wireless Bluetooth Headphones",
  "slug": "wireless-bluetooth-headphones",
  "description": "Premium noise-cancelling headphones with 30-hour battery life",
  "specifications": {
    "battery_life": "30 hours",
    "connectivity": "Bluetooth 5.0",
    "noise_cancellation": "Active",
    "weight": "250g"
  },
  "price": NumberDecimal("149.99"),
  "category_id": ObjectId("507f1f77bcf86cd799439020"),
  "brand": "AudioTech",
  "sku": "AT-BT-HP-001",
  "stock_quantity": 50,
  "is_available": true,
  "images": [
    {
      "url": "https://res.cloudinary.com/demo/image/upload/v1234567890/products/at-bt-hp-001-main.jpg",
      "public_id": "products/at-bt-hp-001-main",
      "alt_text": "Wireless Bluetooth Headphones - Front View",
      "is_primary": true
    },
    {
      "url": "https://res.cloudinary.com/demo/image/upload/v1234567890/products/at-bt-hp-001-side.jpg",
      "public_id": "products/at-bt-hp-001-side",
      "alt_text": "Wireless Bluetooth Headphones - Side View",
      "is_primary": false
    }
  ],
  "average_rating": 4.5,
  "review_count": 128,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-10T14:20:00Z")
}
```

---

### 3. categories

**Purpose**: Hierarchical product categorization

**Schema**:

```json
{
  "_id": ObjectId,
  "name": String,
  "slug": String (unique, indexed, URL-friendly),
  "parent_id": ObjectId (optional, reference to parent category),
  "description": String (optional),
  "image_url": String (optional, Cloudinary URL),
  "display_order": Integer (for sorting),
  "is_active": Boolean (default: true),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**Indexes**:
```python
db.categories.create_index("slug", unique=True)
db.categories.create_index("parent_id")
db.categories.create_index("display_order")
```

**Validation Rules** (Pydantic):
```python
name: Min 2 characters, max 100 characters
slug: Lowercase, alphanumeric + hyphens, unique
display_order: Non-negative integer
```

**Relationships**:
- One category can have one parent category (reference: category.parent_id → category._id)
- One category can have many child categories (hierarchical)
- One category has many products (reference: product.category_id → category._id)

**Example Documents**:
```json
// Root category
{
  "_id": ObjectId("507f1f77bcf86cd799439020"),
  "name": "Electronics",
  "slug": "electronics",
  "parent_id": null,
  "description": "Electronic devices and accessories",
  "image_url": "https://res.cloudinary.com/demo/image/upload/categories/electronics.jpg",
  "display_order": 1,
  "is_active": true,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}

// Child category
{
  "_id": ObjectId("507f1f77bcf86cd799439021"),
  "name": "Headphones",
  "slug": "headphones",
  "parent_id": ObjectId("507f1f77bcf86cd799439020"),
  "description": "Wired and wireless headphones",
  "image_url": "https://res.cloudinary.com/demo/image/upload/categories/headphones.jpg",
  "display_order": 1,
  "is_active": true,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}
```

---

### 4. carts

**Purpose**: Store active shopping carts (user and guest carts)

**Schema**:

```json
{
  "_id": ObjectId,
  "user_id": ObjectId (optional, reference to users, null for guest carts),
  "session_id": String (optional, for guest carts, unique),
  "items": Array of Objects [  // EMBEDDED cart items
    {
      "product_id": ObjectId (reference to products),
      "quantity": Integer (>= 1),
      "price_at_addition": Decimal128 (snapshot of product price),
      "added_at": DateTime
    }
  ],
  "created_at": DateTime,
  "updated_at": DateTime,
  "expires_at": DateTime (7 days for guest carts, null for user carts)
}
```

**Indexes**:
```python
db.carts.create_index("user_id", unique=True, sparse=True)  # One cart per user
db.carts.create_index("session_id", unique=True, sparse=True)  # One cart per session
db.carts.create_index("expires_at")  # For cleanup job
db.carts.create_index("items.product_id")
```

**Validation Rules** (Pydantic):
```python
Either user_id OR session_id must be present (not both, not neither)
items: Array length >= 0, max 100 items
quantity: Integer >= 1, max 99 per item
price_at_addition: Positive number
```

**Relationships**:
- One cart belongs to zero or one user (reference: cart.user_id → user._id, optional for guest carts)
- Cart items reference products (cart.items[].product_id → product._id)

**Design Decision**: Embed cart items in cart (not separate collection) because:
- Cart items are always accessed with the cart (no independent queries)
- Small array size (max 100 items)
- Atomic updates (add/remove item in single operation)

**Example Documents**:
```json
// Authenticated user cart
{
  "_id": ObjectId("507f1f77bcf86cd799439030"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "session_id": null,
  "items": [
    {
      "product_id": ObjectId("507f1f77bcf86cd799439012"),
      "quantity": 2,
      "price_at_addition": NumberDecimal("149.99"),
      "added_at": ISODate("2025-01-15T10:30:00Z")
    },
    {
      "product_id": ObjectId("507f1f77bcf86cd799439013"),
      "quantity": 1,
      "price_at_addition": NumberDecimal("79.99"),
      "added_at": ISODate("2025-01-15T11:45:00Z")
    }
  ],
  "created_at": ISODate("2025-01-15T10:30:00Z"),
  "updated_at": ISODate("2025-01-15T11:45:00Z"),
  "expires_at": null
}

// Guest cart
{
  "_id": ObjectId("507f1f77bcf86cd799439031"),
  "user_id": null,
  "session_id": "guest-abc123-xyz789",
  "items": [
    {
      "product_id": ObjectId("507f1f77bcf86cd799439012"),
      "quantity": 1,
      "price_at_addition": NumberDecimal("149.99"),
      "added_at": ISODate("2025-01-15T12:00:00Z")
    }
  ],
  "created_at": ISODate("2025-01-15T12:00:00Z"),
  "updated_at": ISODate("2025-01-15T12:00:00Z"),
  "expires_at": ISODate("2025-01-22T12:00:00Z")  // 7 days from creation
}
```

---

### 5. orders

**Purpose**: Store completed purchase orders

**Schema**:

```json
{
  "_id": ObjectId,
  "order_number": String (unique, indexed, human-readable: ORD-20250115-ABC123),
  "user_id": ObjectId (optional, reference to users, null for guest orders),
  "guest_email": String (optional, for guest orders),
  "status": String (enum: "pending", "processing", "shipped", "delivered", "cancelled"),
  "items": Array of Objects [  // EMBEDDED order items (historical snapshot)
    {
      "product_id": ObjectId (reference to products, for tracking),
      "product_name": String (DENORMALIZED snapshot),
      "product_sku": String (DENORMALIZED snapshot),
      "quantity": Integer,
      "price_at_purchase": Decimal128 (DENORMALIZED snapshot),
      "subtotal": Decimal128 (quantity * price_at_purchase)
    }
  ],
  "shipping_address": Object {  // EMBEDDED address
    "full_name": String,
    "address_line1": String,
    "address_line2": String (optional),
    "city": String,
    "state": String,
    "postal_code": String,
    "country": String,
    "phone": String
  },
  "shipping_method": String (enum: "standard", "express", "overnight"),
  "shipping_cost": Decimal128,
  "subtotal": Decimal128 (sum of item subtotals),
  "tax_amount": Decimal128,
  "total_amount": Decimal128 (subtotal + shipping_cost + tax_amount),
  "payment_id": ObjectId (reference to payments collection),
  "estimated_delivery_date": Date,
  "tracking_number": String (optional, for shipped orders),
  "notes": String (optional, customer notes),
  "created_at": DateTime (order date),
  "updated_at": DateTime,
  "shipped_at": DateTime (optional),
  "delivered_at": DateTime (optional),
  "cancelled_at": DateTime (optional)
}
```

**Indexes**:
```python
db.orders.create_index("order_number", unique=True)
db.orders.create_index("user_id")
db.orders.create_index("guest_email")
db.orders.create_index("status")
db.orders.create_index("created_at")  # For sorting by date
db.orders.create_index([("user_id", 1), ("created_at", -1)])  # Compound index for user order history
```

**Validation Rules** (Pydantic):
```python
order_number: Format ORD-YYYYMMDD-XXXXXX (e.g., ORD-20250115-ABC123)
Either user_id OR guest_email must be present
status: One of ["pending", "processing", "shipped", "delivered", "cancelled"]
shipping_method: One of ["standard", "express", "overnight"]
items: Array length >= 1 (cannot create empty order)
subtotal, tax_amount, total_amount: Positive numbers
total_amount: Must equal subtotal + shipping_cost + tax_amount
```

**Relationships**:
- One order belongs to zero or one user (reference: order.user_id → user._id, optional for guest orders)
- Order items reference products (order.items[].product_id → product._id, for reference only)
- One order has one payment (reference: order.payment_id → payment._id)

**Design Decision**: Embed order items and shipping address because:
- Orders are immutable (historical snapshot, never updated)
- Denormalize product name/price to preserve historical accuracy
- Shipping address snapshot specific to this order (user might change saved addresses later)

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439040"),
  "order_number": "ORD-20250115-ABC123",
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "guest_email": null,
  "status": "processing",
  "items": [
    {
      "product_id": ObjectId("507f1f77bcf86cd799439012"),
      "product_name": "Wireless Bluetooth Headphones",
      "product_sku": "AT-BT-HP-001",
      "quantity": 2,
      "price_at_purchase": NumberDecimal("149.99"),
      "subtotal": NumberDecimal("299.98")
    },
    {
      "product_id": ObjectId("507f1f77bcf86cd799439013"),
      "product_name": "USB-C Charging Cable",
      "product_sku": "AT-CBL-USBC-001",
      "quantity": 1,
      "price_at_purchase": NumberDecimal("19.99"),
      "subtotal": NumberDecimal("19.99")
    }
  ],
  "shipping_address": {
    "full_name": "John Doe",
    "address_line1": "123 Main Street",
    "address_line2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "United States",
    "phone": "+1234567890"
  },
  "shipping_method": "standard",
  "shipping_cost": NumberDecimal("9.99"),
  "subtotal": NumberDecimal("319.97"),
  "tax_amount": NumberDecimal("28.80"),
  "total_amount": NumberDecimal("358.76"),
  "payment_id": ObjectId("507f1f77bcf86cd799439050"),
  "estimated_delivery_date": ISODate("2025-01-20"),
  "tracking_number": null,
  "notes": "Please leave at the front desk",
  "created_at": ISODate("2025-01-15T14:30:00Z"),
  "updated_at": ISODate("2025-01-15T14:30:00Z"),
  "shipped_at": null,
  "delivered_at": null,
  "cancelled_at": null
}
```

---

### 6. payments

**Purpose**: Store payment transaction records

**Schema**:

```json
{
  "_id": ObjectId,
  "order_id": ObjectId (reference to orders collection),
  "payment_method": String (enum: "credit_card", "debit_card", "paypal", "apple_pay", "google_pay"),
  "payment_provider": String (e.g., "stripe", "paypal"),
  "transaction_id": String (unique, indexed, from payment gateway),
  "status": String (enum: "pending", "completed", "failed", "refunded"),
  "amount": Decimal128,
  "currency": String (default: "USD", ISO 4217 code),
  "card_last4": String (optional, last 4 digits of card, NEVER store full card number),
  "card_brand": String (optional, e.g., "visa", "mastercard", "amex"),
  "failure_reason": String (optional, for failed payments),
  "refund_amount": Decimal128 (optional, for partial/full refunds),
  "refund_reason": String (optional),
  "metadata": Object (optional, additional data from payment gateway),
  "created_at": DateTime (payment initiation),
  "completed_at": DateTime (optional, payment completion),
  "failed_at": DateTime (optional),
  "refunded_at": DateTime (optional)
}
```

**Indexes**:
```python
db.payments.create_index("order_id")
db.payments.create_index("transaction_id", unique=True, sparse=True)
db.payments.create_index("status")
db.payments.create_index("created_at")
```

**Validation Rules** (Pydantic):
```python
payment_method: One of ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay"]
payment_provider: One of ["stripe", "paypal"]
status: One of ["pending", "completed", "failed", "refunded"]
amount: Positive number
currency: ISO 4217 code (3 uppercase letters)
card_last4: Exactly 4 digits (optional)
NEVER store full card number, CVV, or expiry date (PCI-DSS compliance)
```

**Relationships**:
- One payment belongs to one order (reference: payment.order_id → order._id)

**Security Note**: NEVER store sensitive payment information (full card number, CVV, expiry). Use Stripe Elements to handle card input and tokenization.

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439050"),
  "order_id": ObjectId("507f1f77bcf86cd799439040"),
  "payment_method": "credit_card",
  "payment_provider": "stripe",
  "transaction_id": "pi_3AbCdEfGhIjKlMnO",
  "status": "completed",
  "amount": NumberDecimal("358.76"),
  "currency": "USD",
  "card_last4": "4242",
  "card_brand": "visa",
  "failure_reason": null,
  "refund_amount": null,
  "refund_reason": null,
  "metadata": {
    "stripe_customer_id": "cus_AbCdEfGhIjKl",
    "stripe_payment_intent_id": "pi_3AbCdEfGhIjKlMnO"
  },
  "created_at": ISODate("2025-01-15T14:30:00Z"),
  "completed_at": ISODate("2025-01-15T14:30:15Z"),
  "failed_at": null,
  "refunded_at": null
}
```

---

### 7. addresses

**Purpose**: Store saved shipping/billing addresses for registered users

**Schema**:

```json
{
  "_id": ObjectId,
  "user_id": ObjectId (reference to users collection),
  "type": String (enum: "shipping", "billing", "both"),
  "full_name": String,
  "address_line1": String,
  "address_line2": String (optional),
  "city": String,
  "state": String,
  "postal_code": String,
  "country": String,
  "phone": String,
  "is_default": Boolean (default: false),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**Indexes**:
```python
db.addresses.create_index("user_id")
db.addresses.create_index([("user_id", 1), ("is_default", 1)])  # Find user's default address
```

**Validation Rules** (Pydantic):
```python
type: One of ["shipping", "billing", "both"]
full_name: Min 2 characters, max 100 characters
address_line1: Min 5 characters, max 200 characters
city: Min 2 characters, max 100 characters
state: 2-letter state code (US) or province name
postal_code: Format varies by country (e.g., 5 digits for US ZIP)
country: ISO 3166-1 country name or code
phone: E.164 format
Only one default address per user per type
```

**Relationships**:
- Many addresses belong to one user (reference: address.user_id → user._id)

**Business Logic**: When a user sets a new default address, unset is_default on all other addresses of the same type for that user.

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439060"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "type": "shipping",
  "full_name": "John Doe",
  "address_line1": "123 Main Street",
  "address_line2": "Apt 4B",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "country": "United States",
  "phone": "+1234567890",
  "is_default": true,
  "created_at": ISODate("2025-01-10T09:00:00Z"),
  "updated_at": ISODate("2025-01-10T09:00:00Z")
}
```

---

### 8. reviews

**Purpose**: Store product reviews and ratings

**Schema**:

```json
{
  "_id": ObjectId,
  "product_id": ObjectId (reference to products collection),
  "user_id": ObjectId (reference to users collection),
  "rating": Integer (1 to 5),
  "title": String (optional),
  "review_text": String,
  "helpful_count": Integer (default: 0, number of users who marked as helpful),
  "verified_purchase": Boolean (default: false, true if user purchased this product),
  "is_approved": Boolean (default: false, for moderation),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**Indexes**:
```python
db.reviews.create_index("product_id")
db.reviews.create_index("user_id")
db.reviews.create_index([("product_id", 1), ("is_approved", 1)])  # Approved reviews for product
db.reviews.create_index([("product_id", 1), ("created_at", -1)])  # Recent reviews for product
db.reviews.create_index([("user_id", 1), ("product_id", 1)], unique=True)  # One review per user per product
```

**Validation Rules** (Pydantic):
```python
rating: Integer 1 to 5
review_text: Min 10 characters, max 2000 characters
title: Optional, max 200 characters
User can only review products they purchased (verified_purchase check)
One review per user per product
```

**Relationships**:
- Many reviews belong to one product (reference: review.product_id → product._id)
- Many reviews belong to one user (reference: review.user_id → user._id)

**Business Logic**:
- When review is created/updated, recalculate product.average_rating and product.review_count
- Only approved reviews are displayed to customers
- Verified purchases have higher weight in rating calculation

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439070"),
  "product_id": ObjectId("507f1f77bcf86cd799439012"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "rating": 5,
  "title": "Excellent sound quality!",
  "review_text": "These headphones exceeded my expectations. The noise cancellation is fantastic, and the battery lasts for days. Highly recommend for anyone looking for quality wireless headphones.",
  "helpful_count": 12,
  "verified_purchase": true,
  "is_approved": true,
  "created_at": ISODate("2025-01-12T16:00:00Z"),
  "updated_at": ISODate("2025-01-12T16:00:00Z")
}
```

---

### 9. refresh_tokens (for JWT authentication)

**Purpose**: Store refresh tokens for stateless JWT authentication

**Schema**:

```json
{
  "_id": ObjectId,
  "user_id": ObjectId (reference to users collection),
  "token": String (unique, indexed, hashed UUID),
  "expires_at": DateTime,
  "created_at": DateTime,
  "is_revoked": Boolean (default: false, for logout/security)
}
```

**Indexes**:
```python
db.refresh_tokens.create_index("token", unique=True)
db.refresh_tokens.create_index("user_id")
db.refresh_tokens.create_index("expires_at")  # For cleanup job (TTL index)
db.refresh_tokens.create_index([("user_id", 1), ("is_revoked", 1)])
```

**Validation Rules** (Pydantic):
```python
token: Hashed UUID (256-bit)
expires_at: Must be in future (7 days from creation)
```

**Relationships**:
- Many refresh tokens belong to one user (reference: refresh_token.user_id → user._id)

**Business Logic**:
- Refresh tokens are single-use (rotated on each refresh)
- Expired tokens are automatically deleted (TTL index)
- Revoked tokens cannot be used (logout, security breach)

**Example Document**:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439080"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",  // Hashed UUID
  "expires_at": ISODate("2025-01-22T14:30:00Z"),  // 7 days from creation
  "created_at": ISODate("2025-01-15T14:30:00Z"),
  "is_revoked": false
}
```

---

## Indexes Summary

**Critical Indexes** (must be created before production):

```python
# users
db.users.create_index("email", unique=True)

# products
db.products.create_index("slug", unique=True)
db.products.create_index("sku", unique=True)
db.products.create_index("category_id")
db.products.create_index([("name", "text"), ("description", "text")])
db.products.create_index("price")

# categories
db.categories.create_index("slug", unique=True)

# carts
db.carts.create_index("user_id", unique=True, sparse=True)
db.carts.create_index("session_id", unique=True, sparse=True)
db.carts.create_index("expires_at")  # TTL index

# orders
db.orders.create_index("order_number", unique=True)
db.orders.create_index("user_id")
db.orders.create_index([("user_id", 1), ("created_at", -1)])

# payments
db.payments.create_index("order_id")
db.payments.create_index("transaction_id", unique=True, sparse=True)

# addresses
db.addresses.create_index("user_id")

# reviews
db.reviews.create_index("product_id")
db.reviews.create_index([("user_id", 1), ("product_id", 1)], unique=True)

# refresh_tokens
db.refresh_tokens.create_index("token", unique=True)
db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0)  # TTL index
```

---

## Data Migration & Seeding

### Seed Data (for development/testing):

1. **Categories**: Create 10-20 categories (Electronics, Clothing, Home, etc.)
2. **Products**: Create 100-200 sample products with images, descriptions, prices
3. **Users**: Create 5-10 test users with verified emails
4. **Reviews**: Create 50-100 reviews for popular products
5. **Orders**: Create 10-20 sample orders in various states

### Production Migration Strategy:

1. **Version Schema**: Use `schema_version` field in each document for future migrations
2. **Backward Compatibility**: New fields are optional, never remove fields
3. **Migration Scripts**: Store in `backend/migrations/` directory
4. **Testing**: Test migrations on staging before production
5. **Rollback Plan**: Keep old schema for 30 days, document rollback procedure

---

## Performance Optimization

### Query Optimization:
- Use projection to fetch only required fields: `db.products.find({}, {"name": 1, "price": 1})`
- Use `limit()` and `skip()` for pagination (offset pagination for small datasets)
- Use cursor-based pagination for large datasets (orders, reviews)
- Use aggregation pipelines for complex queries (product filtering, revenue reports)

### Denormalization Trade-offs:
- **Pros**: Faster reads, fewer joins, simplified queries
- **Cons**: Data duplication, potential inconsistency, more storage
- **When to denormalize**: Data rarely changes (product name in orders), always accessed together (order items)

### Caching Strategy:
- Cache frequently accessed data (product catalog, categories) in Redis
- Invalidate cache on updates (product price change, stock update)
- Use TTL for cache expiry (5-10 minutes for product data)

---

## Next Steps

1. ✅ Data model complete
2. 🎯 Create API contracts (OpenAPI specs)
3. 🎯 Create quickstart.md (setup guide)
4. 🎯 Generate tasks with `/sp.tasks`

---

**Data Model Status**: ✅ COMPLETE
