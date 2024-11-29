import secrets

# Generate a secure random API key
api_key = secrets.token_hex(32)  # 64-character hexadecimal key
print(f"Your API key: {api_key}")
