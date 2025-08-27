#!/usr/bin/env python3
"""
Script to update class_details.html with dynamic URLs for study materials
This script will replace static anchor tags with Django URL patterns
"""

import re

def update_study_material_links():
    # Read the file
    with open('templates/class_details.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Mapping of classes and their subjects based on the new requirements
    class_subjects = {
        5: ['Science', 'English', 'Arts'],
        6: ['Science', 'English', 'Arts'], 
        7: ['Science', 'English', 'Arts'],
        8: ['Mathematics', 'Physical Science', 'Life Science', 'Arts', 'English'],
        9: ['Mathematics', 'Physical Science', 'Life Science', 'Arts', 'English'],
        10: ['Mathematics', 'Physical Science', 'Life Science', 'Arts', 'English'],
        11: ['Mathematics', 'Physics', 'Biology', 'Nutrition', 'English', 'Bengali'],
        12: ['Mathematics', 'Physics', 'Biology', 'Nutrition', 'English', 'Bengali']
    }
    
    boards = ['WBBSE', 'WBCHSE', 'CBSE', 'ICSE', 'ISC']
    
    # For each class and subject, find and replace the anchor patterns
    for class_num in class_subjects:
        for i, subject in enumerate(class_subjects[class_num], 1):
            # Create the new anchor links
            new_links = []
            for board in boards:
                url = f"{{% url 'study_materials_by_filter' {class_num} '{subject}' '{board}' %}}"
                new_links.append(f'                <a href="{url}" class="btn btn-outline-success fw-medium">{board}</a>')
            
            new_links_str = '\n'.join(new_links)
            
            # Find various possible patterns for this class and subject
            patterns = [
                f'exploresub-buttons-{class_num}-{i}',
                f'exploresub-buttons-{class_num}-{i}-1', 
                f'study-{class_num}-{i}',
                f'exploresub-buttons-5-7-{i}',  # For classes that might use the old pattern
                f'exploresub-buttons-8-10-{i}', # For classes 8-10
            ]
            
            for pattern in patterns:
                # Look for the collapse div with this ID
                regex = rf'<div id="{pattern}" class="collapse mt-3">\s*(<a href="[^"]*" class="btn btn-outline-success fw-medium">[^<]+</a>\s*)+</div>'
                
                if re.search(regex, content):
                    # Replace with new content
                    replacement = f'<div id="{pattern}" class="collapse mt-3">\n{new_links_str}\n              </div>'
                    content = re.sub(regex, replacement, content)
                    print(f"Updated {pattern} for Class {class_num} {subject}")
                    break
    
    # Write the updated content back
    with open('templates/class_details.html', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("Update completed!")

if __name__ == "__main__":
    update_study_material_links()
