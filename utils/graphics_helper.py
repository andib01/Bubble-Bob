import pygame

def scale_surfaces_in_dict(surfaces_dict, max_width):
    """
    Scales each surface in the given dictionary so that its width 
    does not exceed `max_width`, preserving the aspect ratio.

    :param surfaces_dict: A dict with any keys and Pygame Surface values
                          e.g. {"idle": Surface, "run": Surface, ...}
    :param max_width:     The maximum allowed width for each surface
    """
    for key, surface in surfaces_dict.items():
        original_w, original_h = surface.get_width(), surface.get_height()
        
        if original_w > max_width:
            scale_factor = max_width / float(original_w)
            new_w = int(original_w * scale_factor)
            new_h = int(original_h * scale_factor)
            
            # Replace the original surface with the scaled one
            surfaces_dict[key] = pygame.transform.smoothscale(surface, (new_w, new_h))