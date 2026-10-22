import tempfile, unittest
from pathlib import Path
from backup import create, verify, ROOT

class BackupTests(unittest.TestCase):
    def test_create_and_verify(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/"ep051.tgz"; metadata=create(target)
            self.assertTrue(verify(target, metadata["sha256"]))
            self.assertFalse(verify(target, "0"*64))
    def test_refuses_destination_inside_source(self):
        with self.assertRaises(ValueError): create(ROOT/"unsafe.tgz")

if __name__ == "__main__": unittest.main()
