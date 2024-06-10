# Render Checker 1.0 ***************************************************************
# description = This is a render checker for Nuke that filters render by department
#               for the same shot.
#
# date        = 2024-06-09
# author      = rileyliao@icloud.com
#***********************************************************************************


import os
import nuke

# Define the directory to search for render files
DIR_PATH = "F:/Your_Directory_PATH/show/render/"

# GET SHOTNAME and SEQUENCE from current nuke file name.
def get_shot_info():
    open_file_name = os.path.basename(nuke.root().name())
    print("Current Nuke script file name:", open_file_name)

    split_name = open_file_name.split('_')
    SEQUENCE = split_name[0]
    SHOTNAME = split_name[1]
    print("Sequence and Shotname of the current Nuke script:", SEQUENCE, SHOTNAME)
    return SHOTNAME, SEQUENCE

SHOTNAME, SEQUENCE = get_shot_info()

# GET all read nodes path from current scene
def get_read_nodes_info():
    read_nodes_info = []
    for node in nuke.allNodes('Read'):
        file_path = node['file'].value()
        if DIR_PATH in file_path:
            file_name = os.path.basename(file_path)  # Extract the file name
            read_nodes_info.append((node, file_path, file_name))
    return read_nodes_info

read_nodes_info = get_read_nodes_info()

# GET department info and version from render file names
def get_render_dept_and_version(file_name):
    split_names = file_name.split('_')
    if len(split_names) > 3:  # Ensure there are enough parts to extract the department and version
        dept = split_names[2]
        version = split_names[3].split('.')[0]  # Get the version
        return dept, version
    else:
        print("File name format is not correct:", file_name)
        return None, None

# Function to show the department selection popup
def show_department_popup():
    panel = nuke.Panel("Select Department")
    departments = ["lighting", "fx", "tracking"]
    panel.addEnumerationPulldown("Department", " ".join(departments))
    result = panel.show()
    if result:
        return panel.value("Department")
    return None

# Function to detect new version
def detect_new_version(dept, SEQUENCE, SHOTNAME, current_version):
    render_path = os.path.join(DIR_PATH, dept, SEQUENCE, SHOTNAME)
    versions = []

    if os.path.exists(render_path):
        for item in os.listdir(render_path):
            if os.path.isdir(os.path.join(render_path, item)) and item.startswith('v'):
                versions.append(item)

        versions.sort()
        latest_version = versions[-1] if versions else None

        if latest_version > current_version:
            nuke.message("New version: " + latest_version + " is available: " + SEQUENCE + "_" + SHOTNAME + "_" + dept + "_" + latest_version)
            for node, file_path, file_name in read_nodes_info:
                if dept in file_name:
                    node_version = file_name.split('_')[3].split('.')[0]
                    if node_version == current_version:
                        node['tile_color'].setValue(0xff0000ff)  # RED for read nodes
            return latest_version, True
        else:
            nuke.message("Already at the latest version!")
            return current_version, False
    else:
        nuke.message("Render path does not exist:", render_path)
        return current_version, False

# Update to the latest render version
def update_latest_render():
    selected_dept = show_department_popup()
    if selected_dept:
        current_dept = selected_dept
        current_version = None
        for node, file_path, file_name in read_nodes_info:
            dept, version = get_render_dept_and_version(file_name)
            if dept == current_dept:
                current_version = version
                break
        if current_dept and current_version:
            latest_version, update_available = detect_new_version(selected_dept, SEQUENCE, SHOTNAME, current_version)
            if update_available:
                if nuke.ask("Do you want to update to " + SEQUENCE + "_" + SHOTNAME + "_" + selected_dept + "_" + latest_version + "?"):
                    for node, file_path, file_name in read_nodes_info:
                        if selected_dept in file_name:
                            node_version = file_name.split('_')[3].split('.')[0]
                            if node_version == current_version:
                                new_file_path = file_path.replace(current_version, latest_version)
                                node['file'].setValue(new_file_path)
                                node['tile_color'].setValue(0xff000ff)  # GREEN for updated read nodes
                    nuke.message("Update successful to the version: " + latest_version)
                else:
                    nuke.message("Update cancelled by the user!")
            else:
                print("Already at the latest version.")
                

#---- This is the END of the code ----


