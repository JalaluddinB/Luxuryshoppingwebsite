# Manual Testing Guide - Lux Cart Automation

## Feature Overview
Lux can now automatically add items to the cart when users request it. This guide will help you test this new functionality.

## Prerequisites
1. User must be logged in to use cart automation
2. Products must be in stock
3. Chat with Lux via the chat widget on any page

## Test Cases

### Test Case 1: Basic Cart Addition
**Steps:**
1. Log in to the website
2. Open the Lux chat widget (bottom right corner)
3. Ask Lux: "Tell me about your watches"
4. When Lux suggests a watch, say: "Add it to my cart"
5. Lux should confirm and automatically add the item

**Expected Result:**
- Lux responds with confirmation message
- System message appears: "✓ [Product Name] has been added to your cart"
- Cart count in navigation updates

### Test Case 2: Different Request Phrases
**Test these variations:**
- "I'll take it"
- "Add the [product name] to my cart"
- "Put it in my cart"
- "I want the diamond ring"
- "Can you add this to cart?"

**Expected Result:**
- Each phrase should trigger cart automation
- Appropriate confirmation messages appear

### Test Case 3: Specific Product Request
**Steps:**
1. Ask Lux: "Show me your diamond rings"
2. Wait for response
3. Say: "Add the Diamond Elegance Ring to my cart"

**Expected Result:**
- Product is added to cart even without prior context
- System message confirms the addition

### Test Case 4: Out of Stock Handling
**Steps:**
1. Find a product that's out of stock (stock = 0)
2. Ask Lux to add it to cart

**Expected Result:**
- System message: "Unable to add to cart: [Product Name] is out of stock"
- No item added to cart

### Test Case 5: Non-existent Product
**Steps:**
1. Ask Lux: "Add the Platinum Necklace to my cart"
   (assuming this product doesn't exist)

**Expected Result:**
- System message: "Unable to add to cart: Product not found"
- No item added to cart

### Test Case 6: Not Logged In
**Steps:**
1. Log out
2. Try asking Lux to add something to cart

**Expected Result:**
- Lux should NOT include the special [ADD_TO_CART:...] tag
- Lux may suggest logging in to use the cart feature
- No automatic cart addition occurs

### Test Case 7: Multiple Items in Conversation
**Steps:**
1. Ask Lux about multiple products
2. Request to add one specific item

**Expected Result:**
- Only the requested item is added
- Correct product is identified and added

### Test Case 8: Stock Limit Handling
**Steps:**
1. Add an item to cart manually until quantity = stock limit
2. Ask Lux to add the same item again

**Expected Result:**
- System message: "Unable to add to cart: Only [N] left in stock for [Product Name]"
- Quantity not increased beyond stock

## Visual Indicators to Check
- ✓ Cart count badge in navigation updates
- ✓ System messages appear in green with checkmark
- ✓ Error messages appear clearly
- ✓ Chat remains functional after cart operations

## Debugging Tips
If cart automation doesn't work:
1. Open browser console (F12)
2. Look for errors in the console
3. Check if the [ADD_TO_CART: ...] tag appears in Lux's response
4. Verify user is logged in (check session)
5. Confirm product exists in database

## API Testing (Optional)
Test the API endpoint directly:

```bash
# Add to cart by product name
curl -X POST http://localhost:5000/api/add_to_cart_by_name \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Diamond Ring"}' \
  --cookie "session=YOUR_SESSION_COOKIE"
```

Expected response:
```json
{
  "success": true,
  "message": "\"Diamond Ring\" has been added to your cart",
  "product_name": "Diamond Ring",
  "product_id": 1
}
```
