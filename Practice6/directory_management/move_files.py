import os
import shutil

os.makedirs("test_dir", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "test_dir/sample.txt")
    print("File moved successfully")
else:
    print("sample.txt not found")