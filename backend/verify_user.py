"""Quick script to verify user credentials"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check admin user
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"Admin user found: {admin.username}")
        print(f"Role: {admin.role}")
        print(f"Password hash exists: {bool(admin.password_hash)}")
        
        # Try to verify password
        test_password = "Admin@123"
        is_valid = admin.check_password(test_password)
        print(f"Password '{test_password}' is valid: {is_valid}")
        
        # If not valid, reset password
        if not is_valid:
            print(f"\nResetting admin password to '{test_password}'...")
            admin.set_password(test_password)
            db.session.commit()
            print("Password reset successfully!")
            
            # Verify again
            is_valid = admin.check_password(test_password)
            print(f"Password verification after reset: {is_valid}")
    else:
        print("Admin user not found!")
        print("Creating admin user...")
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('Admin@123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
