import os
import pandas as pd

# 1. Define file paths
csv_filename = "melanoma_challenge_datacollections (test set).csv"
output_filename = "melanoma_challenge_updated.csv"
folder_path = "."

print("--- Starting Process ---")
print(f"Looking for CSV file: {csv_filename}")

# Check if the CSV is actually in this folder
if not os.path.exists(csv_filename):
    print(f"\nERROR: Could not find '{csv_filename}'.")
    print(f"Your terminal is currently looking in this folder: {os.getcwd()}")
    print("Please make sure the CSV file is inside this exact folder.")
    exit()

# 2. Load the CSV
print("Loading CSV...")
df = pd.read_csv(csv_filename, dtype={'MC_LESION_ID': str})

# Force create the 'description' column
df['description'] = ""
print(f"Created 'description' column successfully.")

# 3. Loop through files
md_files_found = 0
matches_found = 0

print(f"\nScanning for .md files in: {os.getcwd()}")
for filename in os.listdir(folder_path):
    if filename.endswith("_Redacted_ocr.md"):
        md_files_found += 1
        # Extract the ID: "7767-26-10_Redacted_ocr.md" -> "7767-26-10"
        file_id = filename.replace("_Redacted_ocr.md", "")

        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        # Check if this ID actually exists in the CSV
        if file_id in df['MC_LESION_ID'].values:
            df.loc[df['MC_LESION_ID'] == file_id, 'description'] = content
            matches_found += 1
            print(f"  -> Matched & copied text for ID: {file_id}")
        else:
            print(f"  -> WARNING: Found file for {file_id}, but this ID is missing from the CSV.")

print("\n--- Summary ---")
print(f"Markdown (.md) files found: {md_files_found}")
print(f"Successful matches updated in CSV: {matches_found}")

# 4. Save to a NEW file so it doesn't overwrite your original
print(f"\nSaving to {output_filename}...")
df.to_csv(output_filename, index=False)
print(f"Done! Please look in your project folder and open the file named exactly: {output_filename}")