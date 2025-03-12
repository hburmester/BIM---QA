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

@when('selecciono {cantidad} productos y los agrego al carrito')
def step_add_products(context, cantidad):
    take_screenshot(context, "products")
    for i in range(int(cantidad)):
        product_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("store item").instance({i})')
        wait_for_element(context, product_locator).click()
        click_button(context, "Add To Cart button")
        take_screenshot(context, f"products_{i}")
        click_button(context, "open menu")
        click_button(context, "menu item catalog")

@when('abro el carrito')
def step_open_cart(context):
    click_button(context, 'cart badge')
    take_screenshot(context, "cart")

@when('procedo al pago')
def step_checkout(context):
    click_button(context, "Proceed To Checkout button")
    take_screenshot(context, "checkout")

@when('agrego una dirección')
def step_enter_address(context):
    """Fills out the address form field by field and proceeds to payment."""
    address_fields = [
        "Full Name",
        "Address Line 1",
        "City",
        "Zip Code",
        "Country"
    ]

    address = {row[0]: row[1] for row in context.table if row[0] in address_fields}
    take_screenshot(context, "address_empty")

    for field, value in address.items():
        fill_input_field(context, field, value)  # Fill each field as it's found

    take_screenshot(context, "address_added")

    click_button(context, "To Payment button")

@when('agrego un método de pago')
def step_enter_payment_details(context):
    """Fills out the payment form field by field and reviews order."""
    payment_fields = [
        "Full Name",
        "Card Number",
        "Expiration Date",
        "Security Code"
    ]

    take_screenshot(context, "payment_empty")
    payment = {row[0]: row[1] for row in context.table if row[0] in payment_fields}

    for field, value in payment.items():
        fill_input_field(context, field, value)  # Fill each field as it's found
    take_screenshot(context, "payment_added")

    click_button(context, "Review Order button")

@then('revisar por última vez la orden y presionar Place Order')
def step_place_order_after_review(context):
    take_screenshot(context, "review_order")
    click_button(context, "Review Order button")
    take_screenshot(context, "place_order")
    click_button(context, "Place Order button")

@then('aparece pantalla de confirmación de compra')
def step_confirmation_page(context):
    confirmation_messages = [
        "Checkout Complete",
        "Thank you for your order",
        "Your new swag is on its way",
        "Your order has been dispatched and will arrive as fast as the pony gallops!"
    ]
    wait = WebDriverWait(context.driver, 10)
    for message in confirmation_messages:
        try:
            locator = (By.XPATH, f'//android.widget.TextView[@text="{message}"]')
            if wait.until(EC.presence_of_element_located(locator)):
                return  # Confirmation found, exit function
        except:
            continue
    assert False, "No confirmation message found"
    take_screenshot(context, "purchase_confirm")

@when('compro "{cantidad}" productos')
def step_buy_number_items(context, cantidad):
    step_add_products(context, int(cantidad))
    step_open_cart(context)
    step_checkout(context)
    context.table = context.table
    step_enter_address(context)
    step_enter_payment_details(context)
    step_place_order_after_review(context)
    step_confirmation_page(context)