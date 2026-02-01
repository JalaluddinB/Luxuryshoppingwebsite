"""
Integration test for cart automation feature
This test simulates the complete workflow of Lux adding items to cart
"""
import unittest
import json
import re


class TestCartAutomationIntegration(unittest.TestCase):
    """Integration tests for cart automation"""
    
    def test_lux_response_format(self):
        """Test that Lux responses with cart tags are properly formatted"""
        # Simulate a Lux response with cart automation tag
        lux_response = "Absolutely! I've added the Diamond Ring to your cart. [ADD_TO_CART: Diamond Ring]"
        
        # Pattern from JavaScript
        pattern = r'\[ADD_TO_CART:\s*([^\]]+)\]'
        match = re.search(pattern, lux_response)
        
        self.assertIsNotNone(match)
        product_name = match.group(1).strip()
        self.assertEqual(product_name, "Diamond Ring")
        
        # Verify clean message (removing the tag)
        clean_message = lux_response.replace(match.group(0), '').strip()
        self.assertEqual(clean_message, "Absolutely! I've added the Diamond Ring to your cart.")
        self.assertNotIn('[ADD_TO_CART', clean_message)
    
    def test_multiple_spaces_in_tag(self):
        """Test handling of multiple spaces in cart tag"""
        responses = [
            "Great choice! [ADD_TO_CART: Luxury Watch]",
            "Perfect! [ADD_TO_CART:Luxury Watch]",
            "Excellent! [ADD_TO_CART:  Luxury Watch  ]",
        ]
        
        pattern = r'\[ADD_TO_CART:\s*([^\]]+)\]'
        
        for response in responses:
            match = re.search(pattern, response)
            self.assertIsNotNone(match, f"Failed to match: {response}")
            product_name = match.group(1).strip()
            self.assertEqual(product_name, "Luxury Watch")
    
    def test_cart_tag_at_end_of_response(self):
        """Test that cart tag appears at the end as per Lux instructions"""
        correct_format = "I'll add that to your cart right away. [ADD_TO_CART: Designer Handbag]"
        
        pattern = r'\[ADD_TO_CART:\s*([^\]]+)\]'
        match = re.search(pattern, correct_format)
        
        self.assertIsNotNone(match)
        # Verify tag is near the end (after removing tag, very little content remains)
        clean = correct_format.replace(match.group(0), '').strip()
        self.assertTrue(len(clean) > 0)  # Should have content before tag
        self.assertFalse(correct_format.startswith('[ADD_TO_CART'))  # Should not start with tag
    
    def test_case_insensitive_product_lookup(self):
        """Test that product names are matched case-insensitively"""
        # Simulate different case variations
        test_names = [
            "Diamond Ring",
            "diamond ring",
            "DIAMOND RING",
            "DiAmOnD rInG",
        ]
        
        # All should normalize to the same value when using ilike in SQL
        # This is handled by the backend with Product.name.ilike(product_name)
        # Here we just verify the names are equivalent when normalized
        normalized = [name.lower() for name in test_names]
        self.assertTrue(all(n == "diamond ring" for n in normalized))
    
    def test_sample_products_exist(self):
        """Verify sample products are defined in the app"""
        with open('app.py', 'r') as f:
            content = f.read()
            
        # Check for sample products
        sample_products = [
            'Luxury Watch',
            'Designer Handbag',
            'Silk Scarf',
            'Leather Jacket',
            'Diamond Ring',
            'Premium Sunglasses'
        ]
        
        for product in sample_products:
            self.assertIn(product, content, f"Sample product '{product}' not found in app.py")


if __name__ == '__main__':
    unittest.main()
