from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using a key.
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary and key:
        return dictionary.get(key, "Time not set")
    return "Time not set"

@register.filter
def format_time(time_str):
    """
    Template filter to format time string.
    Converts 24-hour format to 12-hour format if needed.
    """
    if not time_str or time_str == "Time not set":
        return "Time not set"
    
    try:
        # If it's already in the right format, return as is
        if time_str.upper().endswith(('AM', 'PM')):
            return time_str
        
        # If it's in 24-hour format, convert to 12-hour
        from datetime import datetime
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str
