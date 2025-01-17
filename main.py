import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from termcolor import colored
import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.simplefilter("ignore", NotOpenSSLWarning)


def randstringwlength(length):
    """Generate a random string of the specified length using characters 0-9 and a-z."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def construct_url():
    """Construct a URL using the specified format."""
    base_url = "https://order.eventix.io/"
    random_part = f"{randstringwlength(8)}-{randstringwlength(4)}-{randstringwlength(4)}-{randstringwlength(4)}-{randstringwlength(12)}"
    return base_url + random_part

def wait_for_page_change(driver, interval=0.1, timeout=60):
    """
    Monitor the page for changes in its content.
    
    Args:
        driver: Selenium WebDriver instance.
        interval (int): Time (in seconds) to wait between checks.
        timeout (int): Maximum time (in seconds) to wait for changes.
    """
    #print(colored("Monitoring the page for changes...", "blue"))

    # Get the initial content
    initial_content = driver.page_source
    #print(colored("Initial content captured. Waiting for changes...", "cyan"))

    start_time = time.time()

    # while True:
    #     # Wait for the specified interval
    #     time.sleep(interval)

    #     # Refresh the page and get the current content
    #     driver.refresh()
    #     current_content = driver.page_source

    #     # Check if the page content has changed
    #     if current_content != initial_content:
    #         print(colored("Page content has changed!", "green"))
    #         break

    #     # Exit if the timeout is exceeded
    #     if time.time() - start_time > timeout:
    #         print(colored("Timeout exceeded. No changes detected.", "yellow"))
    #         break

    while True:
        # Wait for the specified interval
        time.sleep(interval)

        # Refresh the page and get the current content
        #driver.refresh()
        current_content = driver.page_source
        current_url = driver.current_url  # Capture the current URL

        # Check for specific success or error messages
        # if "Success, your order is confirmed!" in current_content:
        #     print(colored(f"Success: Your order is confirmed at {current_url}", "green"))
        #     break
        if "Order details" in current_content:
            print(colored(f"Success: Your order is confirmed at {current_url}", "green"))
            
            # Generate a random file name
            filename = f"/Users/behrad/Desktop/eventix{randstringwlength(8)}.txt" 
            
            # Write the URL to the file
            with open(filename, "w") as file:
                file.write(current_url)
            
            break

        elif "Something went wrong!" in current_content:
            print(colored(f"Error: Something went wrong at {current_url}", "red"))
            break

        # Exit if the timeout is exceeded
        if time.time() - start_time > timeout:
            print(colored(f"Timeout exceeded. No matching messages detected at {current_url}", "yellow"))
            break


def scrape_mode():
    """Continuously open random URLs in a browser and monitor for changes."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open browser maximized

    # ChromeDriver installed via Homebrew doesn't require a specified path
    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            url = construct_url()
            print(colored(f"Opening {url} in the browser...", "cyan"))
            driver.get(url)
            wait_for_page_change(driver)
    finally:
        driver.quit()

def debug_mode():
    """Open a single random URL in a browser and monitor for changes."""
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")  # Open browser maximized

    # ChromeDriver installed via Homebrew doesn't require a specified path
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = construct_url()
        print(colored(f"Opening {url} in the browser...", "cyan"))
        driver.get(url)
        wait_for_page_change(driver)
    finally:
        driver.quit()

def ownurlFunc(own_url):
    """Open a single URL in a browser and monitor for changes."""
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")  # Open browser maximized

    # ChromeDriver installed via Homebrew doesn't require a specified path
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(colored(f"Opening {own_url} in the browser...", "cyan"))
        driver.get(own_url)
        wait_for_page_change(driver)
    finally:
        driver.quit()

def main():
    """Main menu to choose between Scrape and Debug modes."""
    while True:
        print("\nMenu:")
        print("1. Scrape (continuous crawling with browser)")
        print("2. Debug (open one URL in browser and monitor changes)")
        print("3. Own url")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            print(colored("\nEntering Scrape Mode...\n", "green"))
            scrape_mode()
        elif choice == "2":
            print(colored("\nEntering Debug Mode...\n", "cyan"))
            debug_mode()
        elif choice == "3":
            own_url = input("Enter your own URL: ").strip()
            ownurlFunc(own_url);
        elif choice == "4":
            print(colored("\nExiting the program. Goodbye!", "yellow"))
            break
        else:
            print(colored("Invalid choice. Please enter 1, 2, or 3.", "red"))

if __name__ == "__main__":
    main()