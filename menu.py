# -----------------------------------------------------------
#  menu.py
#  Version: 1.0.1
#  Last Updated: May 25, 2024
# -----------------------------------------------------------


# ----- DEFINE CUSTOM FOLDER STRUCTURE ----------------------
"""
import nuke
import sys
import os
"""

import nuke


# **************************************************************************************************
# MENU
# **************************************************************************************************

    
def add_menu_toolbar():
    custom_menu = nuke.menu('Nuke').addMenu('Comp_BFF')
    print("This new menu has been created!")

    custom_gizmo = nuke.menu('Nodes').addMenu('Comp_BFF', icon='F:/icons/r_icon_Small.png')
    
    return custom_menu, custom_gizmo

custom_menu, custom_gizmo = add_menu_toolbar()


# ADD toolbars
custom_menu.addCommand('Render Check', 'import render_checker_v1;render_checker_v1.update_latest_render()')

custom_gizmo.addCommand('Render Check', 'import render_checker_v1;render_checker_v1.update_latest_render()')
