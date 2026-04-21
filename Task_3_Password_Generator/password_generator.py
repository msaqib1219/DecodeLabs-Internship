import secrets
import string
import math


class EnterprisePasswordGenerator:
    """
    Enterprise-grade random password generator following NIST 2024 guidelines.

    Implements the Input-Process-Output architectural pattern with:
    - Cryptographically secure randomness (secrets module)
    - Memory-efficient password building (.join() pattern)
    - Entropy validation for security assessment
    """

    # NIST 2024 SP 800-63-4 compliance constraints
    MIN_LENGTH = 15
    MAX_LENGTH = 64

    def __init__(self):
        """Initialize character pools using string module constants."""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.punctuation = string.punctuation
        self.all_chars = self.lowercase + self.uppercase + self.digits + self.punctuation

    def validate_length(self, length):
        """
        Phase 1: Validate environmental requirements.

        Args:
            length (int): Requested password length

        Returns:
            tuple: (is_valid: bool, error_message: str or None)

        Raises:
            TypeError: If length is not an integer
            ValueError: If length violates NIST guidelines
        """
        if not isinstance(length, int):
            raise TypeError(f"Password length must be an integer, got {type(length).__name__}")

        if length < self.MIN_LENGTH:
            raise ValueError(
                f"Password length must be at least {self.MIN_LENGTH} characters "
                f"(NIST 2024 requirement). Received: {length}"
            )

        if length > self.MAX_LENGTH:
            raise ValueError(
                f"Password length cannot exceed {self.MAX_LENGTH} characters "
                f"(NIST 2024 maximum). Received: {length}"
            )

        return True, None

    def generate_password(self, length):
        """
        Phase 2: Build backend transformation engine.

        Generates a cryptographically secure random password using:
        - secrets.choice() for cryptographic-grade randomness
        - .join() accumulator pattern for O(N) memory efficiency
        - Full character pool (letters + digits + punctuation)

        Args:
            length (int): Desired password length

        Returns:
            str: Cryptographically secure random password
        """
        self.validate_length(length)

        password_chars = [
            secrets.choice(self.all_chars) for _ in range(length)
        ]

        password = ''.join(password_chars)

        return password

    def calculate_entropy(self, length):
        """
        Phase 3: Mathematical validation of security.

        Calculates information entropy using Shannon's formula:
        E = L × log₂(R)

        Where:
        - L = password length
        - R = size of character pool (94 characters: 26 lower + 26 upper + 10 digits + 32 punctuation)

        Args:
            length (int): Password length

        Returns:
            float: Entropy in bits
        """
        char_pool_size = len(self.all_chars)
        entropy = length * math.log2(char_pool_size)
        return entropy

    def validate_entropy(self, entropy):
        """
        Validate that generated password meets security standards.

        Security levels:
        - 50-64 bits: Acceptable for low-risk accounts
        - 64-128 bits: Strong for most enterprise use
        - 128+ bits: Cryptographic strength

        Args:
            entropy (float): Calculated entropy in bits

        Returns:
            str: Human-readable security assessment
        """
        if entropy < 50:
            return "⚠️  LOW: Password lacks sufficient entropy"
        elif entropy < 64:
            return "✓ ACCEPTABLE: Suitable for low-security contexts"
        elif entropy < 128:
            return "✓✓ STRONG: Enterprise-grade security"
        else:
            return "✓✓✓ MILITARY: Cryptographic-strength password"

    def generate_with_validation(self, length):
        """
        Complete enterprise password generation pipeline.

        Executes all three phases:
        1. Input validation (NIST constraints)
        2. Cryptographic generation
        3. Entropy validation

        Args:
            length (int): Desired password length

        Returns:
            dict: Complete password metadata including:
                - password: Generated secure password
                - length: Password length
                - entropy: Calculated entropy (bits)
                - security_level: Human-readable assessment
                - character_pool_size: Number of possible characters
        """
        self.validate_length(length)
        password = self.generate_password(length)
        entropy = self.calculate_entropy(length)
        security_level = self.validate_entropy(entropy)

        return {
            'password': password,
            'length': length,
            'entropy': round(entropy, 2),
            'security_level': security_level,
            'character_pool_size': len(self.all_chars)
        }


def main():
    """Interactive CLI for enterprise password generation."""
    generator = EnterprisePasswordGenerator()

    print("\n" + "="*70)
    print("ENTERPRISE RANDOM PASSWORD GENERATOR")
    print("NIST 2024 Compliant | Cryptographically Secure")
    print("="*70)

    while True:
        try:
            user_input = input(
                f"\nEnter desired password length ({generator.MIN_LENGTH}-{generator.MAX_LENGTH} chars, "
                f"or 'quit' to exit): "
            ).strip()

            if user_input.lower() == 'quit':
                print("\n✓ Thank you for using Enterprise Password Generator")
                break

            length = int(user_input)
            result = generator.generate_with_validation(length)

            print("\n" + "-"*70)
            print(f"Generated Password: {result['password']}")
            print(f"Length: {result['length']} characters")
            print(f"Entropy: {result['entropy']} bits")
            print(f"Character Pool: {result['character_pool_size']} possible characters")
            print(f"Security Assessment: {result['security_level']}")
            print("-"*70)

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except TypeError as e:
            print(f"❌ Type error: {e}")
        except KeyboardInterrupt:
            print("\n\n✓ Generator terminated by user")
            break


if __name__ == "__main__":
    main()
