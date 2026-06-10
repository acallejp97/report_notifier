import os
import sys
from pathlib import Path
import pytest
import tempfile

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))


@pytest.fixture
def temp_working_dir():
    """Create a temporary directory and change to it for the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        # Create the saves directory for SaveService
        os.makedirs("saves", exist_ok=True)
        yield tmpdir
        os.chdir(original_dir)


