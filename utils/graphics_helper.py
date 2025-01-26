import pygame

def scale_surfaces(collection, max_width):
    """
    Scales each surface in the given list/tuple or dictionary so that
    its width does not exceed `max_width`, preserving aspect ratio.

    :param collection: A dictionary or list/tuple containing Pygame Surfaces.
                       e.g. {"idle": Surface, "run": Surface} or [Surface, Surface, ...]
    :param max_width:  The maximum allowed width for each surface
    """
    
    # A helper function to scale a single Pygame surface
    def scale_surface(surface):
        original_w, original_h = surface.get_width(), surface.get_height()
        if original_w > max_width:
            scale_factor = max_width / float(original_w)
            new_w = int(original_w * scale_factor)
            new_h = int(original_h * scale_factor)
            return pygame.transform.smoothscale(surface, (new_w, new_h))
        return surface

    # If it's a dictionary
    if isinstance(collection, dict):
        for key, surface in collection.items():
            collection[key] = scale_surface(surface)

    # If it's a list or tuple
    elif isinstance(collection, (list, tuple)):
        for i in range(len(collection)):
            collection[i] = scale_surface(collection[i])

    else:
        raise ValueError(
            "scale_surfaces only supports dict, list, or tuple of Pygame Surfaces."
        )

    return collection
