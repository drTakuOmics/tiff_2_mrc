from PIL import Image
import os

# Directory containing the problematic TIFF files
directory = r"C:\Users\Problematic_Files"

# Get the list of all TIFF files in the specified directory
file_names = [f for f in os.listdir(directory) if f.endswith(".tif")]

# List to store files with null byte warnings
null_byte_files = []

for file_name in file_names:
    try:
        file_path = os.path.join(directory, file_name)
        with Image.open(file_path) as img:
            metadata = img.tag_v2
            description = metadata.get(270)  # Tag 270 is ImageDescription
            
            # Check if the description is in bytes
            if isinstance(description, bytes):
                description = description.decode('utf-8', errors='ignore')  # Decode bytes to string
            
            print(f"{file_name} - Description: {description}")
            
            if description and '\x00' in description:
                null_byte_count = description.count('\x00')
                print(f"Warning: {null_byte_count} null byte(s) found in ImageDescription.")
                null_byte_files.append(file_name)  # Add to the list

                # Remove null bytes from the description
                clean_description = description.replace('\x00', '')
                # Update the image's metadata
                img.tag_v2[270] = clean_description.encode('utf-8')
                img.save(os.path.join(directory, f"cleaned_{file_name}"))  # Save as a new file
                print(f"Saved cleaned version as cleaned_{file_name}")
            else:
                print("No null bytes found.")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Summary of files with null bytes
if null_byte_files:
    print("\nSummary of files with null bytes:")
    for file in null_byte_files:
        print(file)
else:
    print("\nNo files had null bytes in their ImageDescriptions.")