#!/usr/bin/env python3
"""
Script to view encrypted user passwords
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from django.contrib.auth.models import User

def view_encrypted_passwords():
    print("🔐 ENCRYPTED PASSWORD VIEWER 🔐")
    print("=" * 60)
    
    users = User.objects.all().order_by('-id')[:10]
    
    for i, user in enumerate(users, 1):
        print(f"\n{i}. 👤 USER: {user.username}")
        print(f"   📧 Email: {user.email or 'Not provided'}")
        print(f"   👤 Name: {user.first_name} {user.last_name}".strip())
        print(f"   🔒 Encrypted Password:")
        print(f"      {user.password}")
        
        # Analyze password hash
        if user.password.startswith('bcrypt_sha256'):
            parts = user.password.split('$')
            print(f"   🔐 Algorithm: bcrypt_sha256 (Most Secure)")
            print(f"   🧂 Salt: {parts[2][:15]}...")
            print(f"   📏 Hash Length: {len(user.password)} chars")
        elif user.password.startswith('pbkdf2_sha256'):
            parts = user.password.split('$')
            print(f"   🔐 Algorithm: pbkdf2_sha256")
            print(f"   🔄 Iterations: {parts[1]}")
            print(f"   🧂 Salt: {parts[2][:15]}...")
            print(f"   📏 Hash Length: {len(user.password)} chars")
        
        print(f"   📅 Created: {user.date_joined}")
        print("-" * 60)

if __name__ == "__main__":
    view_encrypted_passwords()
