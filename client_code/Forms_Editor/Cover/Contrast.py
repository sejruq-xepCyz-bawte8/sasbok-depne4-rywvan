import anvil.server
import math

def hex_to_rgb(hex_color):
    # Strip potential '#' and convert to RGB
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b):
    # Calculate relative luminance according to WCAG 2.1 guidelines
    a = [x / 255.0 for x in (r, g, b)]
    a = [(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4) for x in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def contrast_ratio(l1, l2):
    # Calculate contrast ratio
    l1, l2 = sorted((l1, l2))
    return (l2 + 0.05) / (l1 + 0.05)

def adjust_color_for_contrast(base_color, second_color, target_contrast):
    base_rgb = hex_to_rgb(base_color)
    second_rgb = hex_to_rgb(second_color)
    base_lum = luminance(*base_rgb)
    second_lum = luminance(*second_rgb)
    current_contrast = contrast_ratio(base_lum, second_lum)

    if current_contrast >= target_contrast:
        return second_color  # Return if current contrast is already adequate

    # Adjust both lighter and darker to find closest contrast near target
    best_contrast = current_contrast
    best_color = second_color
    direction = 1 if base_lum > second_lum else -1  # Determine adjustment direction based on luminance
    
    for adjustment in range(0, 256, 5):  # Increment by 5 for broader exploration
        new_rgb = [(max(0, min(255, x + direction * adjustment))) for x in second_rgb]
        new_lum = luminance(*new_rgb)
        new_contrast = contrast_ratio(base_lum, new_lum)
        
        if new_contrast > best_contrast and new_contrast <= target_contrast:
            best_contrast = new_contrast
            best_color = f"#{new_rgb[0]:02X}{new_rgb[1]:02X}{new_rgb[2]:02X}"

            if new_contrast >= target_contrast:
                return best_color  # Early exit if exact target is met

    # If no exact match found, try opposite direction of initial guess
    direction *= -1
    for adjustment in range(0, 256, 5):
        new_rgb = [(max(0, min(255, x + direction * adjustment))) for x in second_rgb]
        new_lum = luminance(*new_rgb)
        new_contrast = contrast_ratio(base_lum, new_lum)
        
        if new_contrast > best_contrast and new_contrast <= target_contrast:
            best_contrast = new_contrast
            best_color = f"#{new_rgb[0]:02X}{new_rgb[1]:02X}{new_rgb[2]:02X}"

    best_color = best_color.lstrip('#')
    return f'#{best_color}'  # Return best found if no exact match to target






if __name__ == "__main__":
    # Example usage:
    base_color = "20BA37"
    # Suppose the second color is '00FF00' (green), and we need to adjust it.
    second_color = "20BA37"
    target_contrast = 6

    adjusted_color = adjust_color_for_contrast(base_color, second_color, target_contrast)
    print("Adjusted Color:", adjusted_color)
