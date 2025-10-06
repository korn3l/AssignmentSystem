import sys
import os

try:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
except NameError:
    project_root = os.path.abspath('.')
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from GUI.dashboard import main

if __name__ == "__main__":
    print("--------------------------------------------------")
    print(f"Project Root: {project_root}")
    print("This has been added to the Python path.")
    print("Starting application from the correct entry point...")
    print("--------------------------------------------------")
    main()