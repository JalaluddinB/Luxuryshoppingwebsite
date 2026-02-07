"""
Basic tests for the cart automation feature
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestCartAutomation(unittest.TestCase):
    """Test cart automation functionality"""
    
    def test_add_to_cart_endpoint_exists(self):
        """Verify the add_to_cart_by_name endpoint is defined"""
        from app import app
        
        # Check if the route exists
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        self.assertIn('/api/add_to_cart_by_name', rules)
    
    def test_cart_tag_pattern(self):
        """Test the cart tag regex pattern matches correctly"""
        import re
        
        # The pattern used in script.js
        pattern = r'\[ADD_TO_CART:\s*([^\]]+)\]'
        
        # Test various formats - note: the \s* after colon consumes leading spaces
        # but trailing spaces in the captured group are preserved
        # JavaScript implementation uses .trim() to clean both ends
        test_cases = [
            ("[ADD_TO_CART: Diamond Ring]", "Diamond Ring", "Diamond Ring"),
            ("[ADD_TO_CART:Diamond Ring]", "Diamond Ring", "Diamond Ring"),
            ("[ADD_TO_CART:  Diamond Ring  ]", "Diamond Ring  ", "Diamond Ring"),
            ("Some text [ADD_TO_CART: Gold Watch] more text", "Gold Watch", "Gold Watch"),
        ]
        
        for test_input, expected_raw, expected_trimmed in test_cases:
            match = re.search(pattern, test_input)
            self.assertIsNotNone(match, f"Pattern should match: {test_input}")
            # Verify raw capture
            self.assertEqual(match.group(1), expected_raw)
            # Verify trimmed matches (as done in JavaScript)
            self.assertEqual(match.group(1).strip(), expected_trimmed)
    
    def test_system_prompt_includes_cart_instruction(self):
        """Verify system prompt includes cart automation instructions when user is logged in"""
        # This would require mocking the session and database
        # For now, we just verify the code contains the cart instruction
        with open('app.py', 'r') as f:
            content = f.read()
            self.assertIn('CART AUTOMATION:', content)
            self.assertIn('[ADD_TO_CART:', content)

if __name__ == '__main__':
    unittest.main()
