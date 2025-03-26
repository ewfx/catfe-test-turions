from playwright.sync_api import sync_playwright
from behave import given, when, then

BASE_URL = "https://parabank.parasoft.com/parabank/index.htm"
VALID_USERNAME = "john"
VALID_PASSWORD = "demo"
INVALID_PASSWORD = "wrongpass"

@given("the user is on the Parabank login page")
def step_open_parabank_page(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()
    context.page.goto(BASE_URL)

@when("the user enters valid credentials")
def step_enter_valid_credentials(context):
    context.page.fill("input[name='username']", VALID_USERNAME)
    context.page.fill("input[name='password']", VALID_PASSWORD)

@when("the user enters invalid credentials")
def step_enter_invalid_credentials(context):
    context.page.fill("input[name='username']", VALID_USERNAME)
    context.page.fill("input[name='password']", INVALID_PASSWORD)

@when("clicks on the login button")
def step_click_login_button(context):
    context.page.click("input[value='Log In']")

@then("the user should be redirected to the Accounts Overview page")
def step_verify_successful_login(context):
    assert context.page.locator("text=Accounts Overview").is_visible()

@then("the user should see an error message")
def step_verify_error_message(context):
    assert context.page.locator("text=Error!").is_visible()

def after_scenario(context, scenario):
    context.page.close()
    context.browser.close()
    context.playwright.stop()
