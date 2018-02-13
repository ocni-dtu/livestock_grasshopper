__author__ = "Christian Kongsgaard"
__license__ = "MIT"
__version__ = "0.1.0"

# -------------------------------------------------------------------------------------------------------------------- #
# Imports

# Module imports


# Livestock imports


# Grasshopper imports
import scriptcontext as sc


# -------------------------------------------------------------------------------------------------------------------- #
# Functions and Classes

def get_python_exe():
    """
    Collects the python.exe path from a sticky.

    :return: The python path.
    :rtype: str
    """

    py = str(sc.sticky["PythonExe"])

    return py