#!/usr/bin/env python3
"""
Production readiness validation script

This script checks the backend application for production readiness
including configuration, security, and deployment considerations.
"""

import os
import json
from pathlib import Path

def check_file_structure():
    """Check if all required files and directories exist"""
    required_files = [
        'app/__init__.py',
        'app/config.py',
        'app/models.py',
        'app/utils.py',
        'app/routes/__init__.py',
        'app/routes/auth.py',
        'app/routes/devices.py',
        'app/routes/cameras.py',
        'app/routes/alerts.py',
        'app/services/poller.py',
        'app/services/alerting.py',
        'celery_worker.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'run.py',
        'README.md'
    ]
    
    required_dirs = [
        'app/routes',
        'app/services',
        'migrations'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    return missing_files, missing_dirs

def check_docker_configuration():
    """Check Docker configuration"""
    issues = []
    
    # Check Dockerfile
    if os.path.exists('Dockerfile'):
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
            
        if 'gunicorn' not in dockerfile_content:
            issues.append("Dockerfile should use gunicorn for production")
        
        if 'EXPOSE' not in dockerfile_content:
            issues.append("Dockerfile should expose the application port")
    else:
        issues.append("Dockerfile is missing")
    
    # Check docker-compose.yml
    if os.path.exists('docker-compose.yml'):
        with open('docker-compose.yml', 'r') as f:
            compose_content = f.read()
            
        if 'redis' not in compose_content:
            issues.append("docker-compose.yml should include Redis service")
        
        if 'celery_worker' not in compose_content:
            issues.append("docker-compose.yml should include Celery worker service")
    else:
        issues.append("docker-compose.yml is missing")
    
    return issues

def check_security_considerations():
    """Check security considerations"""
    issues = []
    
    # Check for hardcoded secrets (basic check)
    sensitive_files = ['app/config.py', 'run.py', 'celery_worker.py']
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Look for potential hardcoded secrets
            if 'password' in content.lower() and '=' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'password' in line.lower() and '=' in line and not line.strip().startswith('#'):
                        if not any(env_func in line for env_func in ['os.environ.get', 'getenv', 'config.']):
                            issues.append(f"{file_path}:{i} - Potential hardcoded password")
    
    return issues

def check_dependencies():
    """Check if all required dependencies are listed"""
    if not os.path.exists('requirements.txt'):
        return ["requirements.txt is missing"]
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    critical_packages = [
        'Flask',
        'Flask-JWT-Extended',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'celery',
        'redis',
        'gunicorn',
        'cryptography'
    ]
    
    missing_packages = []
    for package in critical_packages:
        if package not in requirements:
            missing_packages.append(package)
    
    return missing_packages

def check_logging_configuration():
    """Check if proper logging is configured"""
    issues = []
    
    # Check app/__init__.py for logging configuration
    if os.path.exists('app/__init__.py'):
        with open('app/__init__.py', 'r') as f:
            init_content = f.read()
        
        if 'logging' not in init_content:
            issues.append("No logging configuration found in app/__init__.py")
        
        if 'RotatingFileHandler' not in init_content:
            issues.append("No file logging handler configured")
    
    return issues

def main():
    """Main validation function"""
    print("=== Production Readiness Check ===\n")
    
    total_issues = 0
    
    # Check file structure
    print("1. File Structure Check")
    missing_files, missing_dirs = check_file_structure()
    if not missing_files and not missing_dirs:
        print("   ✅ All required files and directories present")
    else:
        if missing_files:
            print(f"   ❌ Missing files: {', '.join(missing_files)}")
            total_issues += len(missing_files)
        if missing_dirs:
            print(f"   ❌ Missing directories: {', '.join(missing_dirs)}")
            total_issues += len(missing_dirs)
    
    print()
    
    # Check Docker configuration
    print("2. Docker Configuration Check")
    docker_issues = check_docker_configuration()
    if not docker_issues:
        print("   ✅ Docker configuration looks good")
    else:
        for issue in docker_issues:
            print(f"   ❌ {issue}")
        total_issues += len(docker_issues)
    
    print()
    
    # Check security
    print("3. Security Check")
    security_issues = check_security_considerations()
    if not security_issues:
        print("   ✅ No obvious security issues found")
    else:
        for issue in security_issues:
            print(f"   ⚠️  {issue}")
        total_issues += len(security_issues)
    
    print()
    
    # Check dependencies
    print("4. Dependencies Check")
    missing_deps = check_dependencies()
    if not missing_deps:
        print("   ✅ All critical dependencies listed")
    else:
        print(f"   ❌ Missing dependencies: {', '.join(missing_deps)}")
        total_issues += len(missing_deps)
    
    print()
    
    # Check logging
    print("5. Logging Configuration Check")
    logging_issues = check_logging_configuration()
    if not logging_issues:
        print("   ✅ Logging configuration found")
    else:
        for issue in logging_issues:
            print(f"   ❌ {issue}")
        total_issues += len(logging_issues)
    
    print()
    
    # Summary
    print("=== Summary ===")
    if total_issues == 0:
        print("🎉 Application appears to be production ready!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set environment variables for production")
        print("3. Run with Docker: docker-compose up -d")
        print("4. Change default admin password")
        print("5. Configure SMTP and Slack webhooks")
        return 0
    else:
        print(f"⚠️  Found {total_issues} issues that should be addressed before production deployment")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
