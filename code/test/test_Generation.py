import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("http://localhost:4200/test-generation")
    yield

def test_test_generation_component_renders(page: Page):
    expect(page.locator("text=Enter Context")).to_be_visible()
    expect(page.locator("text=Preview Generated Tests")).to_be_visible()
    expect(page.locator("textarea")).to_be_visible()
    expect(page.locator("button:has-text('Generate Tests')")).to_be_visible()

def test_textarea_input_and_test_generation(page: Page):
    textarea = page.locator("textarea")
    textarea.fill("Sample step definition")
    expect(textarea).to_have_value("Sample step definition")
    
    page.locator("button:has-text('Generate Tests')").click()
    
    # More specific selector for test preview sections
    expect(page.locator("div.bg-gray-700.p-4.rounded-lg").first).to_be_visible()

def test_generated_test_display(page: Page):
    # Example of testing specific test scenario
    page.locator("button:has-text('Generate Tests')").click()
    expect(page.locator("div.bg-gray-700 h3").first).to_be_visible()