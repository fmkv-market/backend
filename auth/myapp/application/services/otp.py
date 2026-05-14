import secrets
import string

class OtpService:
    @classmethod
    def generate_otp(cls) -> str:
        digits = string.digits
        secure_pin = ''.join(secrets.choice(digits) for _ in range(6))
        return secure_pin