import os

#Export all submodules
__all__ = []
for file in os.listdir("comparators"):
    if file.endswith(".py") and "__init__" not in file:
        __all__.append(file.split('.')[0])
