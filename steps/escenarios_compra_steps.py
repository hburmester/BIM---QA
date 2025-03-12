from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from appium.webdriver.common.appiumby import AppiumBy
from utils.screenshot_helper import take_screenshot

def wait_for_element(context, locator, condition=EC.presence_of_element_located, timeout=15):
    """Waits for an element to be present and returns it."""
    wait = WebDriverWait(context.driver, timeout)

    for _ in range(3):  # Retry mechanism
        try:
            return wait.until(condition(locator))
        except (TimeoutException, NoSuchElementException):
            print(f"Retrying to locate element: {locator}")

    raise Exception(f"Failed to locate element: {locator} after retries")

def fill_input_field(context, field_id, value, retries=3):
    """Waits for the input field and fills it with the given value, retrying if needed."""
    locator = (AppiumBy.ACCESSIBILITY_ID, field_id + "* input field")

    for _ in range(retries):
        try:
            input_field = wait_for_element(context, locator, EC.visibility_of_element_located)
            input_field.clear()
            input_field.send_keys(value)
            return  # Éxito, salir de la función
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException en {field_id}, reintentando...")

    raise Exception(f"No se pudo llenar el campo {field_id} después de {retries} intentos")

def click_button(context, button_id):
    """Waits for a button to be clickable and clicks it."""
    wait = WebDriverWait(context.driver, 15)

    for _ in range(5):  # Retry mechanism
        try:
            locator = (By.ACCESSIBILITY_ID, button_id)
            button = wait.until(EC.element_to_be_clickable(locator))  # Locate fresh element
            button.click()
            return
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException encountered for '{button_id}', retrying...")

    raise Exception(f"Failed to click button '{button_id}' after retries")

@when('visualizo el numero de productos')
def step_add_products(context):
    # Locate the cart badge container
    cart_badge_locator = (AppiumBy.ACCESSIBILITY_ID, "cart badge")
    cart_badge = wait_for_element(context, cart_badge_locator)

    # Find the TextView inside the cart badge
    context.cantidad = cart_badge.find_element(By.XPATH, ".//android.widget.TextView").text

@then('borro todos los productos')
def step_delete_all_products(context):
    take_screenshot(context, "before_delete")
    for i in range(int(context.cantidad)):
            rmove_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Remove Item").instance(0)')
            wait_for_element(context, rmove_button_locator).click()
    take_screenshot(context, "after_deletion")

@then('validar mensajes de error')
def step_verify_payment_details(context):
    """Checks if payment details are correctly filled and validates errors."""
    take_screenshot(context, "card_details")
    payment_fields = {
        "Full Name": "Full Name* input field",
        "Card Number": "Card Number* input field",
        "Expiration Date": "Expiration Date* input field",
        "Security Code": "Security Code* input field",
    }

    error_messages = {
        "Full Name": "Full Name*-error-message",
        "Card Number": "Card Number*-error-message",
        "Expiration Date": "Expiration Date*-error-message",
        "Security Code": "Security Code*-error-message",
    }

    for field, locator in payment_fields.items():
        input_element = context.driver.find_element(By.XPATH, f'//android.widget.EditText[@content-desc="{locator}"]')
        input_value = input_element.text.strip()

        error_element = context.driver.find_elements(By.XPATH, f'//android.view.ViewGroup[@content-desc="{error_messages[field]}"]')

        # Capture error message if it exists
        error_message = error_element[0].text if error_element else ""

        # Print validation result
        if not input_value or error_message:
            print(f"{field}: Value looks invalid. (Error: {error_message})")
        else:
            print(f"{field}: Valid input.")

        # Assert all fields are valid
        assert not error_message, f"Error in {field}: {error_message}"

        take_screenshot(context, "invalid_card")