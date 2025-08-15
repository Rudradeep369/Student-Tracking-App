"""
Utility functions for media file management in the Student Management System.
"""
import os
from django.conf import settings
from myapp.models import Teacher, Achievement


def clean_orphaned_media_files():
    """
    Clean up orphaned media files that are no longer referenced by any model instances.
    This function should be run periodically to free up disk space.
    """
    cleaned_files = []
    
    # Check teacher images
    teacher_media_path = os.path.join(settings.MEDIA_ROOT, 'teacher-img')
    if os.path.exists(teacher_media_path):
        # Get all teacher image files currently in use
        used_teacher_files = set()
        for teacher in Teacher.objects.exclude(profile_image__isnull=True).exclude(profile_image__exact=''):
            if teacher.profile_image:
                used_teacher_files.add(os.path.basename(teacher.profile_image.name))
        
        # Check for orphaned files
        for filename in os.listdir(teacher_media_path):
            file_path = os.path.join(teacher_media_path, filename)
            if os.path.isfile(file_path) and filename not in used_teacher_files:
                try:
                    os.remove(file_path)
                    cleaned_files.append(f"teacher-img/{filename}")
                except OSError:
                    pass
    
    # Check achievement images
    achievement_media_path = os.path.join(settings.MEDIA_ROOT, 'achievement-img')
    if os.path.exists(achievement_media_path):
        # Get all achievement image files currently in use
        used_achievement_files = set()
        for achievement in Achievement.objects.exclude(image__isnull=True).exclude(image__exact=''):
            if achievement.image:
                used_achievement_files.add(os.path.basename(achievement.image.name))
        
        # Check for orphaned files
        for filename in os.listdir(achievement_media_path):
            file_path = os.path.join(achievement_media_path, filename)
            if os.path.isfile(file_path) and filename not in used_achievement_files:
                try:
                    os.remove(file_path)
                    cleaned_files.append(f"achievement-img/{filename}")
                except OSError:
                    pass
    
    return cleaned_files


def get_media_usage_stats():
    """
    Get statistics about media file usage.
    """
    stats = {
        'teacher_images': 0,
        'achievement_images': 0,
        'total_files': 0,
        'total_size_mb': 0
    }
    
    # Count teacher images
    teacher_media_path = os.path.join(settings.MEDIA_ROOT, 'teacher-img')
    if os.path.exists(teacher_media_path):
        teacher_files = [f for f in os.listdir(teacher_media_path) 
                        if os.path.isfile(os.path.join(teacher_media_path, f))]
        stats['teacher_images'] = len(teacher_files)
        for filename in teacher_files:
            file_path = os.path.join(teacher_media_path, filename)
            stats['total_size_mb'] += os.path.getsize(file_path)
    
    # Count achievement images
    achievement_media_path = os.path.join(settings.MEDIA_ROOT, 'achievement-img')
    if os.path.exists(achievement_media_path):
        achievement_files = [f for f in os.listdir(achievement_media_path) 
                           if os.path.isfile(os.path.join(achievement_media_path, f))]
        stats['achievement_images'] = len(achievement_files)
        for filename in achievement_files:
            file_path = os.path.join(achievement_media_path, filename)
            stats['total_size_mb'] += os.path.getsize(file_path)
    
    stats['total_files'] = stats['teacher_images'] + stats['achievement_images']
    stats['total_size_mb'] = round(stats['total_size_mb'] / (1024 * 1024), 2)
    
    return stats
