import json
from behave import given, when, then
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.screenshot_helper import take_screenshot

@given("la aplicación está abierta")
def step_open_app(context):
    appium_options = UiAutomator2Options()
    with open("config/capabilities.json") as f:
        capabilities = json.load(f)
        appium_options.platform_name = capabilities.get("platformName")
        appium_options.device_name = capabilities.get("device_name")
        appium_options.app = capabilities.get("app")

    context.driver = webdriver.Remote("http://127.0.0.1:4723", options=appium_options)

@when('ingreso a la pantalla de inicio de sesión')
def step_open_login_page(context):
    context.driver.find_element(By.ACCESSIBILITY_ID,"open menu").click()
    take_screenshot(context, "login_page")
    wait = WebDriverWait(context.driver, 3)  # Wait up to 10 seconds
    element = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "menu item log in")))
    element.click()

@when('ingreso el usuario "{username}"')
def step_enter_username(context, username):
    context.driver.find_element(By.ACCESSIBILITY_ID, "Username input field").send_keys(username)
    take_screenshot(context, "username")

@when('ingreso la contraseña "{password}"')
def step_enter_password(context, password):
    take_screenshot(context, "password")
    context.driver.find_element(By.ACCESSIBILITY_ID,"Password input field").send_keys(password)

@when('presiono el botón de inicio de sesión')
def step_press_login(context):
    take_screenshot(context, "login_button")
    context.driver.find_element(By.ACCESSIBILITY_ID,"Login button").click()

@then('debería ver la pantalla de inicio')
def step_verify_login(context):
    wait = WebDriverWait(context.driver, 3)  # Wait up to 10 seconds
    take_screenshot(context, "login_successful")
    element = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "products screen")))
    assert element.is_displayed()

@when('logout')
def step_logout(context):
    context.driver.find_element(By.ACCESSIBILITY_ID,"open menu").click()
    wait = WebDriverWait(context.driver, 3)  # Wait up to 10 seconds
    take_screenshot(context, "logout_page")
    log_out = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "menu item log out")))
    log_out.click()
    take_screenshot(context, "logout_button")
    confirm_log_out = wait.until(EC.presence_of_element_located((By.ID, "android:id/button1")))
    confirm_log_out.click()
    take_screenshot(context, "logout_successful")
    confirm = wait.until(EC.presence_of_element_located((By.ID, "android:id/button1")))
    confirm.click()

@when('inicio sesión con "{username}" y "{password}"')
def step_login(context, username, password):
    step_open_login_page(context)
    step_enter_username(context, username)
    step_enter_password(context, password)
    step_press_login(context)
    step_verify_login(context)