import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page(browser):
    # Create new context and page for each test
    context = browser.new_context()
    page = context.new_page()
    yield page
    # Clean up after test
    context.close()

def test_full_navigation_flow(page: Page):
    # Step 1: Start at home page
    page.goto("http://localhost:4200/")
    expect(page).to_have_url("http://localhost:4200/")
    
    # Step 2: Click "Start updating" button
    start_updating_btn = page.locator("button:has-text('Start updating')")
    expect(start_updating_btn).to_be_visible()
    with page.expect_navigation():
        start_updating_btn.click()
    
    # Verify we're on test-update page
    expect(page).to_have_url("http://localhost:4200/test-update")
    expect(page.locator("text=Existent Test Suites")).to_be_visible()
    
    # Step 3: Find and click "User Authentication" test card
    user_auth_card = page.locator("div.bg-gray-500:has-text('User Authentication')").first
    expect(user_auth_card).to_be_visible()
    
def test_full_navigation_flow(page: Page):
    # 1. Start at home
    page.goto("http://localhost:4200/")
    
    # 2. Navigate to test-update
    start_updating_btn = page.locator("button:has-text('Start updating')")
    with page.expect_navigation():
        start_updating_btn.click()
    
    # 3. Select test suite (with debug)
    page.on("response", lambda r: print(r.url))  # Debug
    user_auth_card = page.locator("div.bg-gray-500:has-text('User Authentication')").first
    
    try:
        with page.expect_response("**/F001*", timeout=5000):  # Broad pattern
            user_auth_card.click()
    except TimeoutError:
        print("No API response detected - proceeding anyway")
        user_auth_card.click()
    
    # 4. Verify content
    page.wait_for_selector("div.bg-gray-700")  # Basic wait
    expect(page.locator("text=Preview Generated Tests")).to_be_visible()