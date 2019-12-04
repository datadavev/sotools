# Simple package to setup working folder when running in a Binder environment
# from the code embedded in the documentation.
import os
try:
    os.chdir("docsource/source")
except:
    pass
