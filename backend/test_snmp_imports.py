#!/usr/bin/env python3
import sys
print("Python version:", sys.version)
print("Testing pysnmp imports...")

try:
    import pysnmp
    print("pysnmp version:", pysnmp.__version__)
except ImportError as e:
    print("Failed to import pysnmp:", e)
    sys.exit(1)

# Try different import approaches
print("\nTrying hlapi import...")
try:
    from pysnmp.hlapi import *
    print("hlapi import successful")
    print("Available functions:", [x for x in dir() if 'Cmd' in x or 'Engine' in x])
except ImportError as e:
    print("hlapi import failed:", e)

print("\nTrying sync import...")
try:
    from pysnmp.hlapi.sync import *
    print("sync import successful")
    print("Available functions:", [x for x in dir() if 'Cmd' in x or 'Engine' in x])
except ImportError as e:
    print("sync import failed:", e)

print("\nTrying entity import...")
try:
    from pysnmp.entity import *
    print("entity import successful")
    print("Available:", [x for x in dir() if not x.startswith('_')])
except ImportError as e:
    print("entity import failed:", e)

print("\nTrying carrier import...")
try:
    from pysnmp.carrier import *
    print("carrier import successful")
    print("Available:", [x for x in dir() if not x.startswith('_')])
except ImportError as e:
    print("carrier import failed:", e)