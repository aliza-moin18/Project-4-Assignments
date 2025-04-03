import os

def rename_files():
    folder_path = input("Enter the folder path: ").strip()

    if not os.path.exists(folder_path):
        print(" Error: Folder does not exist!")
        return

    prefix = input("Enter a prefix for the new filenames (e.g., 'Project_'): ").strip()
    extension = input("Enter the file extension to rename (e.g., .txt, .jpg, .pdf, etc.): ").strip().lower()

    files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() == extension]


    if not files:
        print(f"⚠️ No files found with the extension '{extension}'.")
        return

    for count, filename in enumerate(files, start=1):
        file_ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}{count}{file_ext}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"✅ Renamed: {filename} → {new_name}")

    print("✅ Bulk renaming complete!")

rename_files()
