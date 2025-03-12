import os

def take_screenshot(context, step_name):
    """Takes a screenshot and saves it with the step name."""
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the directory exists

    filename = f"{screenshot_dir}/{step_name.replace(' ', '_')}.png"
    context.driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")