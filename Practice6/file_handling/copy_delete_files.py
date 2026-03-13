import os
import shutil

shutil.copy("sample.txt", "backup_sample.txt")

if os.path.exists("backup_sample.txt"):
    os.remove("backup_sample.txt")