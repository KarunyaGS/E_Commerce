#!/usr/bin/env python3
"""
Simple script to view encrypted passwords
Just run: python3 show_passwords.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from django.contrib.auth.models import User

def main():
    print("🔐 ENCRYPTED PASSWORD VIEWER 🔐")
    print("=" * 50)
    
    users = User.objects.all().order_by('-id')
    
    if not users:
        print("No users found!")
        return
    
    for i, user in enumerate(users, 1):
        print(f"\n{i}. USER: {user.username}")
        if user.email:
            print(f"   EMAIL: {user.email}")
        if user.first_name or user.last_name:
            print(f"   NAME: {user.first_name} {user.last_name}".strip())
        
        print(f"   ENCRYPTED PASSWORD:")
        print(f"   {user.password}")
        
        # Show encryption type
        if 'bcrypt' in user.password:
            print(f"   🔐 ENCRYPTION: bcrypt (Most Secure)")
        elif 'pbkdf2' in user.password:
            print(f"   🔐 ENCRYPTION: pbkdf2")
        
        print(f"   📅 CREATED: {user.date_joined}")
        print("-" * 50)

if __name__ == "__main__":
    main()
