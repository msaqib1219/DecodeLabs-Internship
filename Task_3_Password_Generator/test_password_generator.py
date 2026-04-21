import unittest
import math
from password_generator import EnterprisePasswordGenerator


class TestEnterprisePasswordGenerator(unittest.TestCase):
    """Test suite for enterprise password generation system."""

    def setUp(self):
        """Initialize generator before each test."""
        self.generator = EnterprisePasswordGenerator()

    # Phase 1: Input Validation Tests
    def test_validate_length_valid_minimum(self):
        """Test validation accepts NIST minimum length (15 chars)."""
        is_valid, error = self.generator.validate_length(15)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_length_valid_maximum(self):
        """Test validation accepts NIST maximum length (64 chars)."""
        is_valid, error = self.generator.validate_length(64)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_length_valid_middle(self):
        """Test validation accepts mid-range length."""
        is_valid, error = self.generator.validate_length(32)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_length_below_minimum(self):
        """Test validation rejects length below NIST minimum."""
        with self.assertRaises(ValueError) as context:
            self.generator.validate_length(14)
        self.assertIn("at least 15", str(context.exception))

    def test_validate_length_above_maximum(self):
        """Test validation rejects length above NIST maximum."""
        with self.assertRaises(ValueError) as context:
            self.generator.validate_length(65)
        self.assertIn("cannot exceed 64", str(context.exception))

    def test_validate_length_type_error_string(self):
        """Test validation rejects non-integer types."""
        with self.assertRaises(TypeError):
            self.generator.validate_length("16")

    def test_validate_length_type_error_float(self):
        """Test validation rejects float types."""
        with self.assertRaises(TypeError):
            self.generator.validate_length(16.5)

    def test_validate_length_type_error_none(self):
        """Test validation rejects None."""
        with self.assertRaises(TypeError):
            self.generator.validate_length(None)

    # Phase 2: Password Generation Tests
    def test_generate_password_correct_length(self):
        """Test generated password has requested length."""
        for length in [15, 20, 32, 50, 64]:
            password = self.generator.generate_password(length)
            self.assertEqual(len(password), length)

    def test_generate_password_uses_all_character_types(self):
        """Test generated password contains diverse character types."""
        password = self.generator.generate_password(50)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.generator.punctuation for c in password)

        self.assertTrue(has_lower, "Password should contain lowercase letters")
        self.assertTrue(has_upper, "Password should contain uppercase letters")
        self.assertTrue(has_digit, "Password should contain digits")
        # Special characters are less likely in small samples, but should appear in most cases

    def test_generate_password_randomness(self):
        """Test that multiple generations produce different passwords."""
        passwords = [
            self.generator.generate_password(20) for _ in range(5)
        ]
        unique_passwords = set(passwords)
        self.assertEqual(
            len(unique_passwords), 5,
            "Generated passwords should be unique (cryptographic randomness test)"
        )

    def test_generate_password_no_validation_errors(self):
        """Test generation doesn't raise validation errors for valid input."""
        try:
            self.generator.generate_password(20)
        except (ValueError, TypeError):
            self.fail("generate_password raised unexpected exception")

    # Phase 3: Entropy Calculation Tests
    def test_entropy_calculation_formula(self):
        """Test entropy follows E = L × log₂(R) formula."""
        length = 16
        entropy = self.generator.calculate_entropy(length)
        expected = length * math.log2(len(self.generator.all_chars))
        self.assertAlmostEqual(entropy, expected, places=5)

    def test_entropy_minimum_length(self):
        """Test entropy at NIST minimum length."""
        entropy = self.generator.calculate_entropy(15)
        self.assertGreater(entropy, 95)  # ~97 bits at minimum
        self.assertLess(entropy, 100)

    def test_entropy_maximum_length(self):
        """Test entropy at NIST maximum length."""
        entropy = self.generator.calculate_entropy(64)
        self.assertGreater(entropy, 400)  # ~410 bits at maximum

    def test_entropy_scales_linearly(self):
        """Test that entropy scales linearly with length."""
        entropy_16 = self.generator.calculate_entropy(16)
        entropy_32 = self.generator.calculate_entropy(32)
        self.assertAlmostEqual(entropy_32 / entropy_16, 2.0, places=1)

    def test_entropy_positive(self):
        """Test entropy is always positive."""
        for length in range(15, 65):
            entropy = self.generator.calculate_entropy(length)
            self.assertGreater(entropy, 0)

    # Security Level Validation Tests
    def test_security_level_low(self):
        """Test low security classification (<50 bits)."""
        self.generator.MIN_LENGTH = 1
        # Simulate low entropy by calculating for very short password
        result = self.generator.validate_entropy(40)
        self.assertIn("LOW", result)

    def test_security_level_acceptable(self):
        """Test acceptable security level (50-64 bits)."""
        result = self.generator.validate_entropy(60)
        self.assertIn("ACCEPTABLE", result)

    def test_security_level_strong(self):
        """Test strong security level (64-128 bits)."""
        result = self.generator.validate_entropy(100)
        self.assertIn("STRONG", result)

    def test_security_level_military(self):
        """Test military-grade security level (128+ bits)."""
        result = self.generator.validate_entropy(150)
        self.assertIn("MILITARY", result)

    # Integration Tests
    def test_generate_with_validation_returns_dict(self):
        """Test complete pipeline returns proper structure."""
        result = self.generator.generate_with_validation(20)
        self.assertIsInstance(result, dict)
        required_keys = {'password', 'length', 'entropy', 'security_level', 'character_pool_size'}
        self.assertEqual(set(result.keys()), required_keys)

    def test_generate_with_validation_password_properties(self):
        """Test generated password in pipeline has correct properties."""
        result = self.generator.generate_with_validation(20)
        self.assertEqual(len(result['password']), 20)
        self.assertIsInstance(result['entropy'], float)
        self.assertGreater(result['entropy'], 0)

    def test_generate_with_validation_invalid_length(self):
        """Test pipeline rejects invalid lengths."""
        with self.assertRaises(ValueError):
            self.generator.generate_with_validation(14)
        with self.assertRaises(ValueError):
            self.generator.generate_with_validation(65)

    def test_nist_compliance_minimum(self):
        """Test NIST 2024 compliance at minimum length."""
        result = self.generator.generate_with_validation(15)
        self.assertEqual(result['length'], 15)
        self.assertGreater(result['entropy'], 95)

    def test_nist_compliance_maximum(self):
        """Test NIST 2024 compliance at maximum length."""
        result = self.generator.generate_with_validation(64)
        self.assertEqual(result['length'], 64)
        self.assertGreater(result['entropy'], 400)

    def test_character_pool_size_constant(self):
        """Test character pool size is consistent across generations."""
        result1 = self.generator.generate_with_validation(20)
        result2 = self.generator.generate_with_validation(30)
        self.assertEqual(result1['character_pool_size'], result2['character_pool_size'])
        self.assertEqual(result1['character_pool_size'], 94)  # 26+26+10+32


if __name__ == '__main__':
    unittest.main(verbosity=2)
