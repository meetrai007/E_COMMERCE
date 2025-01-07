import phonenumbers
import random

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Helper function to validate phone number
def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except phonenumbers.NumberParseException:
        return None