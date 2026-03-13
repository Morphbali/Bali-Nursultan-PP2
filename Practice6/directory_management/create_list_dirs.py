import os

os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Files and folders in current directory:")
for item in os.listdir("."):
    print(item)