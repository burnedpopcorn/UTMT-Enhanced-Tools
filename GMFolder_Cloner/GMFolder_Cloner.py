import os
# Regex
import re
# Windows File Manager stuff
import tkinter as tk
from tkinter import filedialog

# Select Folder Function
def select_folder_dialog(title="Select Folder"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=title)
    return folder_selected

# GMFolder_Cloner
#       by burnedpopcorn180

print("")
print("")
print("GMFolder_Cloner")
print("      by burnedpopcorn180")
print("")
print("Takes an already organized GMS2 project and clones its internal organization")
print("over to another, unorganized, GMS2 project")
print("")
print("WARNING - It is STRONGLY recommended to backup your Target Project")
print("")
print("")
print("")
print("Select Donor Project Folder")
print("     which must contain a project that is already organized")

# Select Folders
folder_1_path = select_folder_dialog("Select Donor Project Folder")  # Folder 1 selection
if not folder_1_path:
    print("Donor Project Selection Cancelled")
    print("Quitting...")
    exit()
    
print("")
print("")
print("Select Target Project Folder")
print("     which should contain a project that you want to be organized")

folder_2_path = select_folder_dialog("Select Target Project Folder")  # Folder 2 selection
if not folder_2_path:
    print("Target Project Selection Cancelled")
    print("Quitting...")
    exit()

print("")
print("")
print("Starting...")
print("Organizing YYP and resource_order...")
print("")
print("")

# Function to find the .yyp and .resource_order files
def find_yyp_and_resource_order(folder_path):
    yyp_file = None
    resource_order_file = None

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.yyp'):
                yyp_file = os.path.join(root, file)
                resource_order_file = os.path.join(root, file.replace('.yyp', '.resource_order'))

                # If both files are found, return them
                if yyp_file and resource_order_file:
                    return yyp_file, resource_order_file
    return None, None

# Function to read and extract the "Folders" section from the .yyp file
def extract_yyp_folders(yyp_file_path):
    with open(yyp_file_path, 'r') as f:
        yyp_data = f.read()

    # Use regex to capture the "Folders" array
    folders_pattern = r'("Folders":\s*\[.*?\])'
    match = re.search(folders_pattern, yyp_data, re.DOTALL)
    
    if match:
        return match.group(1)  # Return the entire "Folders" segment
    else:
        raise ValueError("=!= SYSTEM ERROR =!= 'Folders' Array MISSING in YYP file")

# Function to read and extract the "FolderOrderSettings" section from the .resource_order file
def extract_resource_order(resource_order_file_path):
    with open(resource_order_file_path, 'r') as f:
        resource_order_data = f.read()

    # Use regex to capture the "FolderOrderSettings" array
    folder_order_pattern = r'("FolderOrderSettings":\s*\[.*?\])'
    match = re.search(folder_order_pattern, resource_order_data, re.DOTALL)

    if match:
        return match.group(1)  # Return the entire "FolderOrderSettings" segment
    else:
        raise ValueError("!!! WARNING !!! 'FolderOrderSettings' Array MISSING in resource_order file")

# Function to read and extract the "parent" section from a .yy file
def extract_parent_section(yy_file_path):
    with open(yy_file_path, 'r') as f:
        yy_data = f.read()

    # Use regex to capture the "parent" section
    parent_pattern = r'("parent":\s*\{.*?\})'
    match = re.search(parent_pattern, yy_data, re.DOTALL)

    if match:
        return match.group(1)  # Return the entire "parent" section
    else:
        return None  # Return None if the "parent" section is not found

# Function to replace the "parent" section in a .yy file
def replace_parent_section(yy_file_path, parent_data):
    with open(yy_file_path, 'r') as f:
        yy_data = f.read()

    # Replace the "parent" section using regex
    updated_yy_data = re.sub(r'("parent":\s*\{.*?\})', parent_data, yy_data, flags=re.DOTALL)

    # Write the updated data back to the .yy file
    with open(yy_file_path, 'w') as f:
        f.write(updated_yy_data)

# Main Function Definition
def replace_in_target_project(folder_1_path, folder_2_path):
    
    #-------------------------------------------------------------------------------------------------------------------------------
    # .yyp and .resource_order stuff
    
    # Find the .yyp and .resource_order files in Folder 1 (donor project)
    yyp_file_1, resource_order_file_1 = find_yyp_and_resource_order(folder_1_path)
    if not yyp_file_1:
        print("FATAL ERROR: YYP file not found in Donor Project")
        print("Quitting...")
        return

    # Find the .yyp and .resource_order files in Folder 2 (target project)
    yyp_file_2, resource_order_file_2 = find_yyp_and_resource_order(folder_2_path)
    if not yyp_file_2:
        print("FATAL ERROR: YYP file not found in Target Project")
        print("Quitting...")
        return

    # Extract data from Folder 1 for the "Folders" segment
    try:
        folder_data_from_1 = extract_yyp_folders(yyp_file_1)
    except ValueError as e:
        print(f"=!= SYSTEM ERROR =!=")
        print(f"{e}")
        print("Continuing Anyways...")
        return

    # Replace the "Folders" segment in the target .yyp file
    with open(yyp_file_2, 'r') as f:
        yyp_data_2 = f.read()

    # Replace the folders section using regex
    updated_yyp_data_2 = re.sub(r'("Folders":\s*\[.*?\])', folder_data_from_1, yyp_data_2, flags=re.DOTALL)

    # Write the updated data back to the target .yyp file
    with open(yyp_file_2, 'w') as f:
        f.write(updated_yyp_data_2)

    print(f"+++ SUCCESS +++ Added GMFolders to '{yyp_file_2}'")
    
    #-------------------------------------------------------------------------------------------------------------------------------
    # Handle .resource_order (only if available in Folder 1)

    if resource_order_file_1 and os.path.exists(resource_order_file_1):
        try:
            resource_order_data_from_1 = extract_resource_order(resource_order_file_1)
        except ValueError as e:
            print(f"=!= SYSTEM ERROR =!=")
            print(f"{e}")
            print("Continuing Anyways...")
            resource_order_file_2 = None  # Skip the resource_order if it's missing in Folder 1
        else:
            if not resource_order_file_2 or not os.path.exists(resource_order_file_2):
                # If missing in Folder 2, copy it over from Folder 1
                print("resource_order file is missing in Target Folder")
                print(f"Copying '{resource_order_file_1}' to '{folder_2_path}'.")
                with open(resource_order_file_2, 'w') as f:
                    f.write(resource_order_data_from_1)
                print(f"+++ SUCCESS +++ Copied resource_order to Target Project")
    else:
        print("!!! WARNING !!! resource_order file MISSING in Donor Folder")
        print("Continuing Anyways...")

    #-------------------------------------------------------------------------------------------------------------------------------
    # Individual .yy assets

    # List of root subdirectories to check
    root_subdirs = ['animcurves', 'objects', 'rooms', 'scripts', 'sequences', 'shaders', 'sounds', 'sprites', 'tilesets']
    
    print("")
    print("YYP and resource_order organizing ... DONE")
    print("Organizing Individual Assets...")
    print("")

    # Iterate through each subdirectory in Folder 1
    for root_subdir in root_subdirs:
        # For the output text
        asset_type = root_subdir.upper()
        
        print("")
        print(f"--- Now Organizing Asset Type: {asset_type} ---")
        print("")
        
        # Remove final "s" from subdirectory names
        asset_type_single = asset_type[:-1]
        
        folder_1_subdir_path = os.path.join(folder_1_path, root_subdir)

        if os.path.isdir(folder_1_subdir_path):
            # Iterate through each subfolder in Folder 1's subdirectory
            for root, dirs, files in os.walk(folder_1_subdir_path):
                for dir_name in dirs:
                    # Check if the .yy file exists with the same name as the subfolder
                    yy_file_path_1 = os.path.join(root, dir_name, f"{dir_name}.yy")

                    if os.path.isfile(yy_file_path_1):
                        # Extract the "parent" section from Folder 1's .yy file
                        parent_data_from_1 = extract_parent_section(yy_file_path_1)

                        if parent_data_from_1:
                            # Check if the corresponding .yy file exists in Folder 2
                            yy_file_path_2 = os.path.join(folder_2_path, root[len(folder_1_path)+1:], dir_name, f"{dir_name}.yy")

                            if os.path.isfile(yy_file_path_2):
                                # Replace the "parent" section in the corresponding .yy file in Folder 2
                                replace_parent_section(yy_file_path_2, parent_data_from_1)
                                print(f"+++ SUCCESS +++ Organized {asset_type_single}: {dir_name}.yy")
                                
    print("")
    print("Individual Asset organization ... DONE")

# Initialize main process
replace_in_target_project(folder_1_path, folder_2_path)
