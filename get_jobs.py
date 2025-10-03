import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.errors import TimeoutError, ElementHandleError
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import requests
import json
import re
import sys
import os

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
]

def find_chrome_executable():
    """Find Chrome executable path across different platforms"""
    possible_paths = [
        # Custom path from your code
        'chrome-win/chrome.exe',
        # Windows paths
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(os.getenv('USERNAME', '')),
        
        # macOS paths
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        # Linux paths
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium',
        # Generic fallback
        'chrome',
        'chromium',
        'google-chrome'
    ]
    
    for path in possible_paths:
        if os.path.exists(path) or (not os.path.sep in path):
            return path
    
    return None

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def make_request(url, retries=3, use_session=True, headers=None):
    """Make HTTP request with enhanced error handling and anti-detection"""
    for attempt in range(retries):
        try:
            if use_session:
                session = requests.Session()
                default_headers = {
                    'User-Agent': get_random_user_agent(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                }
                if headers:
                    default_headers.update(headers)
                session.headers.update(default_headers)
                
                response = session.get(url, timeout=20, allow_redirects=True)
                response.raise_for_status()
                return response.text
            else:
                req_headers = headers or {'User-Agent': get_random_user_agent()}
                req = urllib.request.Request(url, headers=req_headers)
                response = urllib.request.urlopen(req, timeout=20)
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                delay = (2 ** attempt) + random.uniform(1, 3)
                time.sleep(delay)
            else:
                return None

def setup_selenium_driver(headless=True):
    """Setup Selenium driver with advanced anti-detection measures"""
    try:
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless=new')  # Use new headless mode
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-component-extensions-with-background-pages')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-domain-reliability')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-background-downloads')
        chrome_options.add_argument('--disable-add-to-shelf')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-gpu-logging')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={get_random_user_agent()}')
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
                "geolocation": 2,
                "plugins": 1,
                "popups": 2,
                "automatic_downloads": 2,
            },
            "profile.managed_default_content_settings": {
                "images": 1
            },
            "profile.default_content_settings": {
                "popups": 0
            },
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-gpu-logging')
        chrome_options.add_argument('--disable-extensions-http-throttling')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # --- Start of the corrected code ---
        # The 'stealth_js' code block and its subsequent call (driver.execute_script(stealth_js))
        # have been completely removed as they cause the 'Cannot redefine property: chrome' error.
        
        # We will still perform the basic navigator property modifications
        # that are less likely to cause issues.
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: parameters =>
                            parameters.name === 'notifications' ? 
                            Promise.resolve({ state: Notification.permission }) :
                            Promise.resolve({ state: 'granted' })
                    })
                });
            '''
        })
        # --- End of the corrected code ---
        
        driver.set_window_size(1920, 1080)
        driver.execute_script("window.scrollTo(0, 100);")
        
        return driver
    except Exception as e:
        print(f"Could not setup Selenium driver: {e}")
        print("Make sure ChromeDriver is installed and in PATH")
        return None
def simulate_human_behavior(driver):
    """Simulate human-like behavior to avoid detection"""
    try:
        # Random mouse movements
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(10, 100), random.randint(10, 100))
        actions.perform()
        
        # Random scroll
        driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Random wait
        time.sleep(random.uniform(1, 3))
    except:
        pass  # Ignore errors in behavior simulation
# Helper function to get text content from an element safely
async def get_text_content(element):
    """Safely gets text from a Pyppeteer element handle."""
    if not element:
        return None
    content = await element.getProperty('textContent')
    return await content.jsonValue() if content else None

# Helper function to get an attribute value from an element safely
async def get_attribute(element, attribute):
    """Safely gets an attribute from a Pyppeteer element handle."""
    if not element:
        return None
    value = await element.getProperty(attribute)
    return await value.jsonValue() if value else None
async def handle_cloudflare_turnstile(page):
    """
    Handles the Cloudflare Turnstile challenge based on the provided HTML structure.
    Returns True if verification is successful, False otherwise.
    """
    try:
        # Step 1: Wait for the main challenge container to be present.
        print("Waiting for Turnstile content container...")
        await page.waitForSelector('.main-wrapper', {'timeout': 65000})
        await asyncio.sleep(6)
        # Step 2: Check if the checkbox is visible and available to be clicked.
        print("Checking for the 'Verify you are human' checkbox...")
        await page.screenshot({"path": "screenshot.png"})
        is_checkbox_visible = await page.evaluate('''() => {
            const checkboxContainer = document.querySelector('.main-wrapper #content :first-child div.cb-c label.cb-lb');
            const checkbox = checkboxContainer ? checkboxContainer.querySelector('input[type="checkbox"]') : null;
            
            // Check for visibility and that the container is not 'none'
            return checkbox && window.getComputedStyle(checkboxContainer).display !== 'none';
        }''')
        
        if not is_checkbox_visible:
            # This covers the cases where a challenge is not needed,
            # or it has already been solved by cookies.
            print("No verification checkbox found or it's not visible. Assuming no action is needed.")
            return True

        # Step 3: Click the checkbox using human-like behavior.
        print("Verification checkbox found. Clicking with human-like behavior...")
        checkbox_pos = await page.evaluate('''() => {
            const rect = document.querySelector('label.cb-lb').getBoundingClientRect();
            return {
                x: rect.x + rect.width / 2,
                y: rect.y + rect.height / 2
            };
        }''')
        
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        await page.mouse.move(checkbox_pos['x'] + offset_x, checkbox_pos['y'] + offset_y, steps=random.randint(5, 10))
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await page.click('label.cb-lb')
        
        print("Verification checkbox clicked. Waiting for resolution...")

        # Step 4: Wait for a final resolution state (success or failure)
        return await wait_for_verification_completion(page)
            
    except Exception as e:
        print(f"Error during Cloudflare verification: {e}")
        return False

# --- Helper function for verification status ---

async def wait_for_verification_completion(page, timeout=30000):
    """
    Waits for the Turnstile challenge to resolve into a success or error state.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout / 1000:
        status = await page.evaluate('''() => {
            const getStyleDisplay = (id) => {
                const element = document.getElementById(id);
                return element && window.getComputedStyle(element).display !== 'none';
            };
            
            if (getStyleDisplay('success')) return 'success';
            if (getStyleDisplay('verifying')) return 'verifying';
            if (getStyleDisplay('fail')) return 'fail';
            if (getStyleDisplay('expired')) return 'expired';
            if (getStyleDisplay('timeout')) return 'timeout';
            if (getStyleDisplay('challenge-error')) return 'challenge-error';
            
            return 'unknown';
        }''')

        if status == 'success':
            print("Cloudflare verification successful!")
            return True
        elif status in ['fail', 'expired', 'timeout', 'challenge-error']:
            print(f"Cloudflare verification failed with status: {status}")
            return False
        elif status == 'verifying':
            # This is an intermediate state, so we continue to wait.
            print("Verification in progress...")
        
        # Wait a short while before checking the status again
        await asyncio.sleep(random.uniform(1, 2))
    
    print("Verification timed out.")
    return False
async def get_upwork_jobs(keywords, location=None):
    """
    Corrected Upwork scraper using pyppeteer with proper error handling
    """
    query = ' '.join(keywords) if isinstance(keywords, list) else keywords
    search_url = f'https://www.upwork.com/nx/search/jobs/?q={urllib.parse.quote(query)}&per_page=20'

    # Step 1: Try requests first (fast method)
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        if response.text and ('job-tile' in response.text or 'JobTile' in response.text):
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            
            # Try multiple selectors for job elements
            job_selectors = [
                'article[data-test="JobTile"]',
                'div[data-test="JobTile"]',
                '.job-tile',
                'section[data-test="job-tile"]'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements[:10]
                    break
            
            for job in job_elements:
                try:
                    # Try multiple title selectors
                    title_selectors = [
                        'h2[data-test="job-title"] a',
                        'h3[data-test="job-title"] a',
                        'h2 a[data-test="UpLink"]',
                        'h3 a[data-test="UpLink"]',
                        '.job-tile-title a',
                        'a[data-test="UpLink"]'
                    ]
                    
                    title_elem = None
                    for selector in title_selectors:
                        title_elem = job.select_one(selector)
                        if title_elem:
                            break
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        
                        # Get budget/payment info
                        budget_selectors = [
                            '[data-test="job-type-label"]',
                            '.job-tile-info-list span',
                            '.job-type',
                            '.budget'
                        ]
                        
                        budget_elem = None
                        for selector in budget_selectors:
                            budget_elem = job.select_one(selector)
                            if budget_elem:
                                break
                        
                        budget = budget_elem.get_text(strip=True) if budget_elem else 'Budget not specified'
                        
                        # Get company/client info
                        client_selectors = [
                            '[data-test="client-name"]',
                            '.client-name',
                            '.up-n-link'
                        ]
                        
                        client_elem = None
                        for selector in client_selectors:
                            client_elem = job.select_one(selector)
                            if client_elem:
                                break
                        
                        client = client_elem.get_text(strip=True) if client_elem else 'Client not specified'
                        
                        jobs.append({
                            'title': title,
                            'link': f"https://www.upwork.com{link}" if link.startswith('/') else link,
                            'budget': budget,
                            'client': client,
                            'platform': 'Upwork'
                        })
                except Exception as e:
                    print(f"Error parsing individual job: {e}")
                    continue
            
            if jobs:
                print(f"Successfully scraped {len(jobs)} Upwork jobs using requests.")
                return jobs
                
    except Exception as e:
        print(f"Requests-based Upwork scrape failed: {e}. Falling back to pyppeteer.")
    
    # Step 2: Fallback to pyppeteer with improved configuration
    browser = None
    try:
        chrome_path = find_chrome_executable()
        if not chrome_path:
            print("Chrome executable not found. Please install Chrome or set the correct path.")
            return []
        
        launch_options = {
            'headless': False,
            'args': [
                '--no-sandbox',
                '--disable-features=CrossOriginEmbedderPolicy',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--window-size=1920,1080',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certificate-errors',
                '--ignore-certificate-errors-spki-list',
                f'--user-agent={get_random_user_agent()}'
            ],
            'ignoreHTTPSErrors': True
        }
        
        # Only set executablePath if we found a specific Chrome path
        if chrome_path and os.path.exists(chrome_path):
            launch_options['executablePath'] = chrome_path
        
        browser = await launch(**launch_options)
        page = await browser.newPage()
           
        # Apply stealth evasions
        await stealth(page)
        # Set viewport and additional headers
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }')
        await page.setViewport({'width': 1920, 'height': 1080})
        await page.setUserAgent(get_random_user_agent())
        
        # Set additional headers to appear more like a real browser
        await page.setExtraHTTPHeaders({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        })

        
        print(f"Navigating to: {search_url}")
        await page.goto(search_url, {'waitUntil': 'networkidle2', 'timeout': 60000})
        await handle_cloudflare_turnstile(page)
        # Handle Cloudflare verification if present
        # try:
        #     # Wait for Cloudflare challenge iframe
        #     await page.waitForSelector('iframe[src*="challenge"]', {'timeout': 10000})
            
        #     # Get all frames and find the challenge frame
        #     frames = page.contentFrame()
        #     print(frames)
        #     challenge_frame = None
            
        #     for frame in frames:
        #         if 'challenge' in frame.url:
        #             challenge_frame = frame
        #             break
                    
        #     if challenge_frame:
        #         # Wait for and click the checkbox
        #         await challenge_frame.waitForSelector('input[type="checkbox"]', {'timeout': 5000})
        #         await asyncio.sleep(2)  # Brief pause to appear more human
        #         await challenge_frame.click('input[type="checkbox"]')
                
        #         # Wait for verification to complete
        #         await page.waitForNavigation({'timeout': 15000})
                
        # except Exception as e:
        #     print(f"No Cloudflare challenge detected or error: {e}")
        

        # Wait a bit for the page to load
        await asyncio.sleep(3)
        # Wait for navigation after verification
        await page.waitForNavigation()
        # Handle potential consent/cookie popups
        try:
            consent_selectors = [
                'button[data-test="consent-accept"]',
                'button[data-cy="consent-accept"]',
                '#consent',
                'button:contains("Accept")',
                'button:contains("Agree")'
            ]
            
            for selector in consent_selectors:
                try:
                    await page.waitForSelector(selector, {'timeout': 2000})
                    await page.click(selector)
                    await asyncio.sleep(1)
                    break
                except:
                    continue
        except:
            pass  # No consent popup found
        
        # Simulate human-like scrolling
        for i in range(3):
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(random.uniform(2, 4))
        
        # Wait for job elements to load
        job_loaded = False
        job_selectors = [
            'article[data-test="JobTile"]',
            'div[data-test="JobTile"]', 
            '.job-tile',
            'section[data-test="job-tile"]'
        ]
        
        for selector in job_selectors:
            try:
                await page.waitForSelector(selector, options={'timeout': 15000})
                job_loaded = True
                await asyncio.sleep(random.uniform(2, 4))
                break
            except:
                continue
        
        if not job_loaded:
            print("No job elements found on Upwork page")
            page_content = await page.content()
            if 'blocked' in page_content.lower() or 'captcha' in page_content.lower():
                print("Upwork page appears to be blocked or showing CAPTCHA")
            return []

        jobs = []
        
        # Find job elements using multiple selectors
        job_elements = await page.querySelectorAll('article[data-test="JobTile"]')
        for job_element in enumerate(job_elements):
            try:
                # Use page.querySelector() and element.getProperty('textContent')
                # for a more direct and efficient way to get text.
                title_element = await job_element.querySelector('h2.job-tile-title > a')
                title = await title_element.getProperty('textContent')
                title = await title.jsonValue() if title else 'No title'
                
                # Get the 'href' attribute
                link = await title_element.getProperty('href')
                link = await link.jsonValue() if link else 'No link'

                # Pyppeteer's evaluate() is used to run a JS function on the element
                # It's a powerful way to handle null cases and get text directly.
                description = await job_element.querySelectorEval(
                    'div[data-test="JobTileDetails"] > div > div > p',
                    '(element) => element.textContent'
                )
                description = description.strip() if description else "No description available"
                
                job_info = await job_element.querySelector('ul.job-tile-info-list')

                job_type = "Type not specified"
                experience_level = "Level not specified"
                budget = "Budget not specified"

                if job_info:
                    # Use querySelectorEval for a concise way to get text from a single element
                    job_type_element = await job_info.querySelector('li[data-test="job-type-label"]')
                    if job_type_element:
                        job_type = await job_type_element.getProperty('textContent')
                        job_type = await job_type.jsonValue()
                    
                    experience_element = await job_info.querySelector('li[data-test="experience-level"]')
                    if experience_element:
                        experience_level = await experience_element.getProperty('textContent')
                        experience_level = await experience_level.jsonValue()

                    # The logic to find the budget element remains similar
                    budget_element = await job_info.querySelector('li[data-test="is-fixed-price"]')
                    if not budget_element:
                        budget_element = await job_info.querySelector('li[data-test="duration-label"]')

                    if budget_element:
                        budget = await budget_element.getProperty('textContent')
                        budget = await budget.jsonValue()
            except Exception as e:
                print(f'Error parsing a single job listing: {e}')
                continue
        
        if not job_elements:
            print("No job elements found in page content")
            return []

        for job in job_elements:
            try:
                # Try multiple title selectors
                title_selectors = [
                    'h2[data-test="job-title"] a',
                    'h3[data-test="job-title"] a', 
                    'h2 a[data-test="UpLink"]',
                    'h3 a[data-test="UpLink"]',
                    '.job-tile-title a',
                    'a[data-test="UpLink"]'
                ]
                
                title_elem = None
                for selector in title_selectors:
                    title_elem = job.select_one(selector)
                    if title_elem:
                        break
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                # Get budget info
                budget_selectors = [
                    '[data-test="job-type-label"]',
                    '.job-tile-info-list span',
                    '.job-type',
                    '.budget'
                ]
                
                budget_elem = None
                for selector in budget_selectors:
                    budget_elem = job.select_one(selector)
                    if budget_elem:
                        break
                
                budget = budget_elem.get_text(strip=True) if budget_elem else 'Budget not specified'
                
                # Get description
                desc_elem = job.select_one('[data-test="job-description"]')
                description = desc_elem.get_text(strip=True)[:200] + '...' if desc_elem else 'No description'
                
                if title:
                    jobs.append({
                        'title': title,
                        'link': f"https://www.upwork.com{link}" if link.startswith('/') else link,
                        'budget': budget,
                        'description': description,
                        'platform': 'Upwork'
                    })
            except Exception as e:
                print(f"Error parsing job with pyppeteer: {e}")
                continue
        
        print(f"Successfully scraped {len(jobs)} jobs from Upwork using pyppeteer.")
        return jobs
        
    except Exception as e:
        print(f"Error scraping Upwork with pyppeteer: {e}")
        return []
    finally:
        if browser:
            try:
                await browser.close()
            except:
                pass

def get_freelancer_jobs(keywords, location=None):
    """Improved Freelancer.com scraper"""
    try:
        query = ' '.join(keywords) if isinstance(keywords, list) else keywords
        base_url = 'https://www.freelancer.com'
        search_url = f'{base_url}/job-search/{urllib.parse.quote(query)}'
        
        # Alternative URL format
        if not make_request(search_url):
            search_url = f'{base_url}/jobs/search/projects/?query={urllib.parse.quote(query)}'
        
        html_content = make_request(search_url)
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Updated selectors for Freelancer
        job_selectors = [
            '.JobSearchCard-item',
            '.ProjectCard',
            'div[data-project-id]',
            '.project-card',
            'article.JobSearchCard-item'
        ]
        
        job_elements = []
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                job_elements = elements
                break
        
        for job in job_elements[:10]:
            try:
                # Try multiple title selectors
                title_selectors = [
                    '.JobSearchCard-primary-heading a',
                    'h3.project-title a',
                    'h2 a', 'h3 a',
                    '.project-title',
                    'a[data-project-title]'
                ]
                
                title_elem = None
                for selector in title_selectors:
                    title_elem = job.select_one(selector)
                    if title_elem:
                        break
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    # Get budget info
                    budget_selectors = [
                        '.JobSearchCard-secondary-price',
                        '.project-budget',
                        '.budget'
                    ]
                    
                    budget_elem = None
                    for selector in budget_selectors:
                        budget_elem = job.select_one(selector)
                        if budget_elem:
                            break
                    
                    budget = budget_elem.get_text(strip=True) if budget_elem else 'Budget not specified'
                    
                    jobs.append({
                        'title': title,
                        'link': f"{base_url}{link}" if link.startswith('/') else link,
                        'budget': budget,
                        'platform': 'Freelancer'
                    })
            except Exception as e:
                continue
        
        return jobs
    except Exception as e:
        print(f"Error scraping Freelancer: {e}")
        return []

def get_indeed_jobs(keywords, location=None):
    """Improved Indeed scraper using Selenium"""
    driver = None
    try:
        driver = setup_selenium_driver()
        if not driver:
            print("Selenium driver not available, skipping Indeed")
            return []
        
        query = ' '.join(keywords) if isinstance(keywords, list) else keywords
        location_param = location if location else ''
        url = f'https://www.indeed.com/jobs?q={urllib.parse.quote(query)}&l={urllib.parse.quote(location_param)}&sort=date'
        
        driver.get(url)
        time.sleep(random.uniform(3, 6))
        
        # Handle potential popup/modal
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='modal-close-button'], .icl-CloseButton")
            close_button.click()
            time.sleep(1)
        except:
            pass  # No modal to close
        
        # Wait for jobs to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-jk], .job_seen_beacon, .result"))
            )
        except:
            print("Jobs didn't load on Indeed")
            return []
        
        jobs = []
        
        # Find job elements
        job_selectors = [
            "div[data-jk]",
            ".job_seen_beacon",
            ".result",
            "td.resultContent"
        ]
        
        job_elements = []
        for selector in job_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and len(elements) > 2:
                    job_elements = elements
                    break
            except:
                continue
        
        for job in job_elements[:10]:
            try:
                # Title extraction
                title_elem = None
                title_selectors = [
                    "h2.jobTitle a[data-jk] span",
                    "h2.jobTitle a span", 
                    ".jobTitle a",
                    "a[data-jk]",
                    "h2 a span"
                ]
                
                for selector in title_selectors:
                    try:
                        title_elem = job.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                # Company extraction
                company_elem = None
                company_selectors = [
                    "span.companyName a",
                    "span.companyName", 
                    ".companyName"
                ]
                
                for selector in company_selectors:
                    try:
                        company_elem = job.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if title_elem:
                    title = title_elem.text.strip()
                    company = company_elem.text.strip() if company_elem else 'Company not specified'
                    
                    # Get job link
                    try:
                        link_elem = job.find_element(By.CSS_SELECTOR, "h2.jobTitle a[data-jk]")
                        link = link_elem.get_attribute('href') or ''
                    except:
                        link = ''
                    
                    if title:  # Only add if we have a title
                        jobs.append({
                            'title': title,
                            'company': company,
                            'link': link,
                            'platform': 'Indeed'
                        })
                        
            except Exception as e:
                continue
        
        return jobs
        
    except Exception as e:
        print(f"Error scraping Indeed with Selenium: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def get_fiverr_jobs(keywords, location=None):
    """Enhanced Fiverr scraper with better anti-detection"""
    driver = None
    try:
        driver = setup_selenium_driver()
        if not driver:
            print("Selenium driver not available, skipping Fiverr")
            return []
        
        query = ' '.join(keywords) if isinstance(keywords, list) else keywords
        url = f'https://www.fiverr.com/search/gigs?query={urllib.parse.quote(query)}&source=top-bar'
        
        driver.get(url)
        simulate_human_behavior(driver)
        
        time.sleep(random.uniform(5, 8))
        
        # Handle cookie consent more reliably
        try:
            cookie_selectors = [
                "[data-testid='cookie-accept']",
                ".cookie-banner button",
                "button[id*='cookie']",
                "button[class*='cookie']"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    cookie_button.click()
                    time.sleep(1)
                    break
                except:
                    continue
        except:
            pass
        
        for i in range(3):
            driver.execute_script(f"window.scrollTo(0, {300 * (i + 1)});")
            time.sleep(random.uniform(1, 2))
        
        # Wait for gigs with multiple selector attempts
        gig_elements = []
        gig_selectors = [
            ".gig-card-layout",
            "[data-gig-id]",
            ".gig-wrapper",
            "article.gig-card",
            ".gig-card"
        ]
        
        for selector in gig_selectors:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and len(elements) > 2:
                    gig_elements = elements[:10]
                    break
            except:
                continue
        
        if not gig_elements:
            print("No gigs found on Fiverr - possible blocking")
            return []
        
        jobs = []
        for gig in gig_elements:
            try:
                title_selectors = [
                    ".gig-card-layout h3 a",
                    "h3 a",
                    ".gig-title a",
                    "a[href*='/gigs/']",
                    ".gig-card-header a"
                ]
                
                title_elem = None
                for selector in title_selectors:
                    try:
                        title_elem = gig.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute('href') or ''
                    
                    # Get seller info
                    seller = 'Seller not specified'
                    seller_selectors = [
                        ".seller-name",
                        ".username",
                        ".seller-link",
                        "[data-username]"
                    ]
                    
                    for selector in seller_selectors:
                        try:
                            seller_elem = gig.find_element(By.CSS_SELECTOR, selector)
                            seller = seller_elem.text.strip()
                            break
                        except:
                            continue
                    
                    # Get price
                    price = 'Price not specified'
                    price_selectors = [
                        ".price",
                        ".gig-price", 
                        "[data-testid='price']",
                        ".price-wrapper"
                    ]
                    
                    for selector in price_selectors:
                        try:
                            price_elem = gig.find_element(By.CSS_SELECTOR, selector)
                            price = price_elem.text.strip()
                            break
                        except:
                            continue
                    
                    if title:
                        jobs.append({
                            'title': title,
                            'seller': seller,
                            'price': price,
                            'link': link,
                            'platform': 'Fiverr'
                        })
                        
            except Exception as e:
                continue
        
        return jobs
        
    except Exception as e:
        print(f"Error scraping Fiverr: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def get_angellist_jobs(city, keywords):
    """Fetches jobs from AngelList (Wellfound) using its API."""
    jobs = []
    headers = {
        'Authorization': 'YOUR_API_KEY_HERE', # You must replace this with your actual API key
        'Content-Type': 'application/json'
    }
    # The Wellfound API is complex and may not have a simple job search endpoint.
    # This is a placeholder for a hypothetical job search API call.
    url = f"https://api.wellfound.com/v1/jobs"
    
    try:
        response = requests.get(url, headers=headers, params={'query': keywords, 'location': city})
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        # Example of how you would parse the JSON data
        for job in data.get('jobs', []):
            jobs.append({
                'title': job.get('title'),
                'link': job.get('permalink'),
                'company': job.get('startup').get('name')
            })
            
        print(f"Successfully fetched {len(jobs)} jobs from AngelList via API")
        return jobs
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        print("Please check your API key and permissions for the Wellfound API.")
    except Exception as e:
        print(f"Error fetching jobs from AngelList API: {e}")
        
    return []

def get_toptal_jobs(keywords, location=None):
    """Improved Toptal scraper - Note: Toptal is invitation-only"""
    try:
        # Toptal doesn't have public job listings like other platforms
        # They work on an invitation/application basis
        print("Note: Toptal is an invite-only platform. Public job listings are not available.")
        return []
    except Exception as e:
        print(f"Error accessing Toptal: {e}")
        return []

# Alternative job sources that are easier to scrape
def get_timesjobs_jobs(keywords, location=None):
    """Scrape jobs from TimesJobs.com"""
    try:
        query = ' '.join(keywords) if isinstance(keywords, list) else keywords
        location_param = location if location else ''
        url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={urllib.parse.quote(query)}&txtLocation={location_param}'
        
        html_content = make_request(url)
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'lxml')
        jobs = []
        
        job_elements = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        
        for job in job_elements[:10]:
            try:
                published_date_element = job.find('span', class_='sim-posted')
                if published_date_element and published_date_element.span:
                    published_date = published_date_element.span.text
                    # Focus on recently posted jobs
                    if 'few' in published_date.lower() or 'today' in published_date.lower():
                        company_name_elem = job.find('h3', class_='joblist-comp-name')
                        company_name = company_name_elem.text.replace(' ', '').strip() if company_name_elem else 'N/A'
                        
                        skills_element = job.find('span', class_='srp-skills')
                        skills = skills_element.text.replace(' ', '').strip() if skills_element else 'Skills not specified'
                        
                        title_elem = job.header.h2.a if job.header and job.header.h2 and job.header.h2.a else None
                        title = title_elem.text.strip() if title_elem else 'Job Title Not Found'
                        link = title_elem['href'] if title_elem and title_elem.get('href') else ''
                        
                        jobs.append({
                            'title': title,
                            'company': company_name,
                            'skills': skills,
                            'link': link,
                            'platform': 'TimesJobs',
                            'posted': published_date
                        })
            except Exception as e:
                continue  # Skip problematic job entries
        
        return jobs
    except Exception as e:
        print(f"Error scraping TimesJobs: {e}")
        return []

async def get_glassdoor_jobs(keywords, location=None):
    """
    Glassdoor scraper using pyppeteer with anti-detection measures
    """
    browser = None
    try:
        query = ' '.join(keywords) if isinstance(keywords, list) else keywords
        location_param = location if location else 'Indonesia'
        string=['locT=C&locId=2762404','locT=C&locId=2203308']
        for i in range(len(string)):
            # Construct Glassdoor search URL                                                           
            search_url = f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(query)}&{string[i]}&locKeyword={urllib.parse.quote(location_param)}&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=1'
            chrome_path = find_chrome_executable()
            if not chrome_path:
                print("Chrome executable not found. Please install Chrome or set the correct path.")
                return []
            
            launch_options = {
                'headless': False,
                'args': [
                    '--no-sandbox',
                    '--disable-features=CrossOriginEmbedderPolicy',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--window-size=1920,1080',
                    '--disable-setuid-sandbox',
                    '--disable-infobars',
                    '--window-position=0,0',
                    '--ignore-certificate-errors',
                    '--ignore-certificate-errors-spki-list',
                    f'--user-agent={get_random_user_agent()}'
                ],
                'ignoreHTTPSErrors': True
            }
            
            # Only set executablePath if we found a specific Chrome path
            if chrome_path and os.path.exists(chrome_path):
                launch_options['executablePath'] = chrome_path
            
            browser = await launch(**launch_options)
            page = await browser.newPage()

            # Apply stealth evasions
            await stealth(page)
            # Set viewport and additional headers
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }')
            await page.setViewport({'width': 1920, 'height': 1080})
            await page.setUserAgent(get_random_user_agent())
            
            # Set additional headers to appear more like a real browser
            await page.setExtraHTTPHeaders({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                # 'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })

            
            print(f"Navigating to: {search_url}")
            # Navigate to search page
            await page.goto(search_url, {'waitUntil': 'networkidle2', 'timeout': 100000})
            
            await page.waitForSelector(
                "[class*='JobsList_jobsList__'], .react-job-listing, .jobContainer, [data-test='job-listing']",
                timeout=30000
            )


            # Random delay to simulate human behavior
            await page.waitFor(random.randint(2000, 4000))
            
            jobs_data = await page.evaluate('''() => {
                const jobs = [];
                
                // Try to find job list container first
                let jobElements = [];
                
                // Primary selector for new Glassdoor structure
                const jobListItems = document.querySelectorAll('[class*="JobsList_jobListItem__"]');
                if (jobListItems.length > 0) {
                    // Filter out non-job items (like carousel cards, nudge cards, etc.)
                    jobElements = Array.from(jobListItems).filter(item => {
                        return item.querySelector('[class*="JobCard_jobCardWrapper__"]') &&
                            item.querySelector('[data-test="job-title"]') &&
                            !item.matches('[class*="ProfileAttributesCarousel_carouselWrapper__"]') &&
                            !item.matches('[class*="ForYouNudgeCard_cardWrapper__"]');
                    });
                }
                
                // Fallback selectors for older structures
                if (jobElements.length === 0) {
                    const fallbackSelectors = [
                        '.react-job-listing',
                        '.jobContainer',
                        '[data-test="job-listing"]',
                        '[class*="job-search-key-"]'
                    ];
                    
                    for (const selector of fallbackSelectors) {
                        const elements = document.querySelectorAll(selector);
                        if (elements.length > 0) {
                            jobElements = Array.from(elements);
                            break;
                        }
                    }
                }

                // Extract job data from first 20 jobs
                jobElements.slice(0, 20).forEach(job => {
                    try {
                        // Extract job title and link
                        let titleElement = job.querySelector('[class*="JobCard_jobTitle__"]');
                        if (!titleElement) {
                            // Fallback selectors
                            const titleSelectors = [
                                'a[data-test="job-title"]',
                                '.jobTitle a',
                                'h2 a',
                                '.job-title a'
                            ];
                            for (const selector of titleSelectors) {
                                titleElement = job.querySelector(selector);
                                if (titleElement) break;
                            }
                        }

                        if (!titleElement) return; // Skip if no title found

                        const title = titleElement.textContent.trim();
                        const link = titleElement.href || '';

                        // Extract company name
                        let company = 'Company not specified';
                        const companyElement = job.querySelector('[class*="EmployerProfile_compactEmployerName__"]');
                        if (companyElement) {
                            company = companyElement.textContent.trim();
                        } else {
                            // Fallback selectors
                            const companySelectors = [
                                '[data-test="employer-name"]',
                                '.employerName',
                                '.companyName',
                                '.employer-name'
                            ];
                            for (const selector of companySelectors) {
                                const fallbackElement = job.querySelector(selector);
                                if (fallbackElement) {
                                    company = fallbackElement.textContent.trim();
                                    break;
                                }
                            }
                        }

                        // Extract location
                        let jobLocation = 'Location not specified';
                        const locationElement = job.querySelector('[class*="JobCard_location__"]');
                        if (locationElement) {
                            jobLocation = locationElement.textContent.trim();
                        } else {
                            const locationSelectors = [
                                '[data-test="job-location"]',
                                '[data-test="emp-location"]',
                                '.location',
                                '.jobLocation'
                            ];
                            for (const selector of locationSelectors) {
                                const fallbackElement = job.querySelector(selector);
                                if (fallbackElement) {
                                    jobLocation = fallbackElement.textContent.trim();
                                    break;
                                }
                            }
                        }

                        // Extract salary
                        let salary = 'Salary not specified';
                        const salaryElement = job.querySelector('[class*="JobCard_salaryEstimate__"]');
                        if (salaryElement) {
                            salary = salaryElement.textContent.trim();
                            salary = salary.replace(/\s+/g, ' ').trim();
                        } else {
                            const salarySelectors = [
                                '[data-test="detailSalary"]',
                                '.salary',
                                '.salaryText'
                            ];
                            for (const selector of salarySelectors) {
                                const fallbackElement = job.querySelector(selector);
                                if (fallbackElement) {
                                    salary = fallbackElement.textContent.trim();
                                    break;
                                }
                            }
                        }

                        // Extract job age/posting date
                        let jobAge = '';
                        const ageElement = job.querySelector('[class*="JobCard_listingAge__"]');
                        if (ageElement) {
                            jobAge = ageElement.textContent.trim();
                        }

                        // Extract company rating
                        let rating = '';
                        const ratingElement = job.querySelector('[class*="rating-single-star_RatingText__"]');
                        if (ratingElement) {
                            rating = ratingElement.textContent.trim();
                        }

                        // Check for Easy Apply
                        const easyApply = job.querySelector('[class*="JobCard_easyApplyTag__"]') ? 'Yes' : 'No';

                        // Push job data
                        if (title && title !== '') {
                            const jobData = {
                                title: title,
                                company: company,
                                location: jobLocation,
                                salary: salary,
                                link: link.startsWith('http') ? link : `https://www.glassdoor.com${link}`,
                                platform: 'Glassdoor'
                            };

                            if (jobAge) jobData.posted = jobAge;
                            if (rating) jobData.company_rating = rating;
                            if (easyApply === 'Yes') jobData.easy_apply = true;

                            jobs.push(jobData);
                        }
                    } catch (error) {
                        console.log('Error extracting job data:', error);
                    }
                });

                return jobs;

            }''')
        
            await browser.close()
        
        print(f"Successfully scraped {len(jobs_data)} jobs from Glassdoor")
        return jobs_data
        
    except Exception as e:
        print(f"Error scraping Glassdoor with pyppeteer: {e}")
        if browser:
            await browser.close()
        return []


async def get_remote_jobs(keywords, location=None):
    """
    Corrected Remote.co scraper using pyppeteer
    """
    query = ' '.join(keywords) if isinstance(keywords, list) else keywords
    search_url = f'https://remote.co/remote-jobs/search?searchkeyword={urllib.parse.quote(query)}&useclocation=false'

    # Step 1: Try requests first
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        if response.text and 'job_listing' in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            
            job_elements = soup.select('.job_listing, .job-listing-item')
            for job in job_elements[:10]:
                try:
                    title_elem = job.select_one('h3 a, h2 a, .job-title a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        
                        company_elem = job.select_one('.company_name, .company-name')
                        company = company_elem.get_text(strip=True) if company_elem else 'Company not specified'
                        
                        jobs.append({
                            'title': title,
                            'link': f"https://remote.co{link}" if link.startswith('/') else link,
                            'company': company,
                            'platform': 'Remote.co'
                        })
                except Exception as e:
                    continue
            
            if jobs:
                print(f"Successfully scraped {len(jobs)} Remote.co jobs using requests.")
                return jobs
                
    except Exception as e:
        print(f"Requests-based Remote.co scrape failed: {e}. Falling back to pyppeteer.")
    
    # Step 2: Fallback to pyppeteer
    browser = None
    try:
        chrome_path = find_chrome_executable()
        if not chrome_path:
            print("Chrome executable not found for Remote.co scraping.")
            return []
        
        launch_options = {
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox', 
                '--disable-dev-shm-usage',
                '--window-size=1920,1080',
                f'--user-agent={get_random_user_agent()}'
            ]
        }
        
        if chrome_path and os.path.exists(chrome_path):
            launch_options['executablePath'] = chrome_path
            
        browser = await launch(**launch_options)
        page = await browser.newPage()
        
        await page.setViewport({'width': 1920, 'height': 1080})
        await page.goto(search_url, {'waitUntil': 'networkidle2', 'timeout': 30000})
        
        # Wait and scroll
        await asyncio.sleep(3)
        for i in range(2):
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(random.uniform(1.5, 3))

        # Wait for jobs to load
        try:
            await page.waitForSelector('#job-table-wrapper', {'timeout': 10000})
        except:
            print("No job listings found on Remote.co")
            return []
        jobs = []
        # First, get the parent element
        jobs_wrapper = await page.waitForSelector('#job-table-wrapper', {'timeout': 10000})

        # Use element.querySelectorAll() with the universal selector '*'
        # This selects all direct child elements of jobs_wrapper.
        job_elements = await jobs_wrapper.querySelectorAll(':scope > *')
        for job_index, job in enumerate(job_elements[:10]):
            try:
                job_data = await page.evaluate('''jobElement => {
                    const root = jobElement.querySelector('div');
                    let parent = null;
                    let titleElement = null;
                    let postedDate = null;
                    let locationElement = null;
                    let categoriesContainer = null
                    if (root) {
                        // Find direct children within the root container
                        const children = Array.from(root.children);
                        
                        // Assuming 'a' tag is the first child of the first child
                        const parent = children[0];
                        if (parent) {
                            titleElement = parent.querySelector('a:first-child');
                            // Find the second span, assuming it's the posted date
                            postedDate = parent.querySelector('span:nth-child(2)');
                        }
                        
                        // Assuming categories are the second child of root
                        categoriesContainer = children[1];
                        
                        // Assuming location icon is the third child of root
                        locationElement = children[2];
                    }

                    let descriptions = [];
                    if (categoriesContainer) {
                        const categoryElements = categoriesContainer.querySelectorAll('li');
                        descriptions = Array.from(categoryElements).map(p => p.innerText.trim());
                    }

                    const location = locationElement ? locationElement.textContent.trim() : null;
                    const link = titleElement ? titleElement.href : '';

                    return {
                        title: titleElement ? titleElement.textContent.trim() : 'oii',
                        location: location,
                        posted_date: postedDate ? postedDate.textContent.trim() : null, // Get innerText
                        link: link,
                        descriptions: descriptions
                    };
                }''', job)

                if job_data:
                    print(f"Successfully scraped data for: {job_data['title']}")
                    jobs.append(job_data)

            except Exception as e:
                print(f"Error scraping job {job_index + 1}: {e}")
                continue
        
        print(f"Successfully scraped {len(jobs)} jobs from Remote.co using pyppeteer.")
        return jobs
        
    except Exception as e:
        print(f"Error scraping Remote.co with pyppeteer: {e}")
        return []
    finally:
        if browser:
            try:
                await browser.close()
            except:
                pass

async def scroll_to_selector(page, selector, timeout=10000):
    """
    Scrolls the page down until a specific selector is found or the end of the page is reached.
    """
    start_time = time.time()
    last_height = await page.evaluate('document.body.scrollHeight')
    
    while True:
        try:
            # Check if the selector is visible within the timeout
            await page.waitForSelector(selector, {'timeout': 500}) # Short timeout for each check
            print(f"Selector '{selector}' found.")
            return True
        except:
            pass # Selector not found yet, continue scrolling

        # Scroll down
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        await asyncio.sleep(0.5) # Wait for new content to load

        new_height = await page.evaluate('document.body.scrollHeight')
        
        # If no new content is loading, we've reached the end
        if new_height == last_height:
            print(f"Reached end of page. Selector '{selector}' not found.")
            return False
        
        last_height = new_height
        
        # Check for overall timeout
        if time.time() - start_time > timeout / 1000:
            print(f"Scrolling timed out after {timeout/1000} seconds. Selector not found.")
            return False
async def get_jobs_from_categories(page, search_url, max_sections=3):
    """
    Scrapes jobs and then navigates to the detail page for each to get more data.
    """
    job_details = []

    # Wait for the main job listings to be visible
    try:
        target_selector = 'section.jobs > article'
        found_selector = await scroll_to_selector(page, target_selector, timeout=60000)
        
        if not found_selector:
            print("Failed to find the job listings after scrolling.")
            return []
    except Exception as e:
        print(f"Main job listings not found: {e}")
        return job_details

    # Get the first 3 job articles to scrape
    job_sections = await page.querySelectorAll('section.jobs > article')
    print(f"Found {len(job_sections)} job sections. Scraping first {max_sections}...")
    sections_to_scrape = job_sections[:max_sections]
    
    for i, article in enumerate(sections_to_scrape):
        try:
            # Find the "view all" link within the article
            view_all_link = await article.querySelector('li.view-all a')
            
            # Check if the link was actually found before proceeding
            if not view_all_link:
                print(f"No 'view-all' link found for job {i+1}. Skipping.")
                continue
            
            # Get the URL directly from the ElementHandle
            link_href = await page.evaluate('(element) => element.href', view_all_link)
            
            print(f"Navigating to job {i+1} detail page at: {link_href}")
            # Open a new tab
            new_tab = await page.browser.newPage()
            await new_tab.setViewport({'width': 1366, 'height': 768})
            
            # Navigate to the job detail page in the new tab
            await new_tab.goto(link_href, {'waitUntil': 'networkidle2', 'timeout': 60000})

            # Wait for job listings to load on the detail page
            try:
                # Wait for job listings to load on the detail page
                await page.waitForSelector('li.new-listing-container', {'timeout': 10000})
                
            except:
                print(f"Job listings not found on detail page {i+1}")
                await new_tab.close()
                continue
            # Get all job listings on the detail page
            job_items = await new_tab.querySelectorAll('li.new-listing-container')
            for job_index, job in enumerate(job_items):
                try:
                    # Scrape data from the job element using page.evaluate
                    job_data = await new_tab.evaluate('''(jobElement) => {
                        const titleElement = jobElement.querySelector('.new-listing__header__title');
                        const companyElement = jobElement.querySelector('.new-listing__company-name');
                        const locationElement = jobElement.querySelector('.new-listing__company-headquarters');
                        const linkElement = jobElement.querySelector('a');
                        const categoriesContainer = jobElement.querySelector('.new-listing__categories');

                        let descriptions = [];
                        if (categoriesContainer) {
                            const categoryElements = categoriesContainer.querySelectorAll('p');
                            descriptions = Array.from(categoryElements).map(p => p.innerText.trim());
                        }
                        const link = linkElement ? linkElement.getAttribute('href') : '';
                        const fullLink = link.startsWith('/') ? 'https://weworkremotely.com' + link : link;

                        return {
                            title: titleElement ? titleElement.innerText.trim() : null,
                            company: companyElement ? companyElement.innerText.trim() : null,
                            headquarters: locationElement ? locationElement.innerText.trim() : null,
                            link: fullLink,
                            descriptions: descriptions
                        };
                    }''', job)
                    if job_data and job_data.get('title'):
                        print(f"Successfully scraped data for: {job_data['title']}")
                        category_name = await new_tab.evaluate('''() => {
                            const anchor = document.querySelector('h2 a');
                            return anchor ? anchor.innerText.trim() : null;
                        }''')
                        job_data['skills'] = category_name
                        job_details.append(job_data)
                except Exception as e:
                    print(f"Error scraping job {job_index+1} on detail page: {e}")
                    continue

            # Close the tab when done
            await new_tab.close()
        except Exception as e:
            print(f"Error while processing job {i+1}: {e}")
            # Try to go back to the main page if we're stuck
            try:
                await page.goBack({'waitUntil': 'networkidle2', 'timeout': 200000})
            except:
                # If we can't go back, reload the main page
                await page.goto(search_url, {'waitUntil': 'networkidle2', 'timeout': 60000})
            continue

    print(f"Successfully scraped details for {len(job_details)} jobs.")
    return job_details

async def get_weworkremotely_jobs(keywords, location=None):
    """
    Corrected We Work Remotely scraper
    """
    query = ' '.join(keywords) if isinstance(keywords, list) else keywords
    search_url = f'https://weworkremotely.com/remote-jobs/search?term={urllib.parse.quote(query)}'
    jobs = []
    # Step 1: Try with BeautifulSoup
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Look for job listings in both 'li' with classes 'feature' and regular ones
        for job_item in soup.select('li.feature, li:not(.feature)'):
            # Skip if it's a view-all or non-job item
            if job_item.find('a', class_='view-all'):
                continue
                
            link = job_item.find('a', href=True)
            title_span = job_item.find('span', class_='title')
            company_span = job_item.find('span', class_='company')
            
            if link and title_span and company_span:
                job_url = f"https://weworkremotely.com{link['href']}"
                jobs.append({
                    'title': title_span.get_text(strip=True),
                    'company': company_span.get_text(strip=True),
                    'url': job_url,
                    'platform': 'We Work Remotely'
                })
        
        if jobs:
            print(f"Successfully scraped {len(jobs)} We Work Remotely jobs using JSON API.")
            return jobs[:10]  # Limit to 10 results
            
    except Exception as e:
        print(f"Scrape failed: {e}. Falling back to pyppeteer.")
    
    # Step 2: Fallback to web scraping
    browser = None
    
    try:
        chrome_path = find_chrome_executable()
        if not chrome_path:
            print(f"No chrome executable exist.")
            return []
            
        launch_options = {
            'headless': False,
            'args': ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            'executablePath': chrome_path
        }
        
        # if chrome_path and os.path.exists(chrome_path):
        #     launch_options['executablePath'] = chrome_path
            
        browser = await launch(**launch_options)
        page = await browser.newPage()

        await page.goto(search_url, {'waitUntil': 'networkidle2', 'timeout': 180000})
        # Simulate human scrolling
        for i in range(3):
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(random.uniform(3.5, 5))
            
        job_elements = await get_jobs_from_categories(page, search_url)

        # Extract job details
        for job in job_elements:
            jobs.append(job) # Check if all fields are non-null
                
        return jobs
        
    except Exception as e:
        print(f"Error scraping We Work Remotely: {e}")
        return []
    finally:
        if browser:
            try:
                await browser.close()
            except:
                pass

def get_remoteok_jobs(keywords, location=None):
    """Scrape jobs from Remote OK (good alternative)"""
    try:
        query = '+'.join(keywords) if isinstance(keywords, list) else keywords
        url = f'https://remoteok.io/remote-{query.lower()}-jobs'
        
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []
        
        job_elements = soup.select('tr.job')
        
        for job in job_elements[:10]:
            try:
                title_elem = job.select_one('h2')
                company_elem = job.select_one('.company h3')
                location_elem = job.select_one('.location')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True) if company_elem else 'Company not specified'
                    job_location = location_elem.get_text(strip=True) if location_elem else 'Remote'
                    
                    link_elem = job.select_one('a')
                    link = f"https://remoteok.io{link_elem.get('href')}" if link_elem else ''
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'link': link,
                        'platform': 'RemoteOK'
                    })
            except Exception as e:
                continue
                
        return jobs
    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")
        return []

# Updated job sources dictionary
all_jobs = {
    'freelancer': {
        'jobs': get_freelancer_jobs,
        'link': 'https://www.freelancer.com',
        'description': 'Global freelancing platform for various skills'
    },
    'glassdoor': {
        'jobs': get_glassdoor_jobs,
        'link': 'https://www.glassdoor.com',
        'description': 'Job search and company reviews platform'
    },
    # 'upwork': {
    #     'jobs': get_upwork_jobs,
    #     'link': 'https://www.upwork.com',
    #     'description': 'Professional freelancing platform'
    # },
    # 'fiverr': {
    #     'jobs': get_fiverr_jobs,
    #     'link': 'https://www.fiverr.com',
    #     'description': 'Marketplace for digital services and gigs'
    # },
    'indeed': {
        'jobs': get_indeed_jobs,
        'link': 'https://www.indeed.com',
        'description': 'Global job search engine'
    },
    'angellist': {
        'jobs': get_angellist_jobs,
        'link': 'https://wellfound.com',
        'description': 'Startup jobs and talent platform'
    },
    'remoteok': {
        'jobs': get_remoteok_jobs,
        'link': 'https://remoteok.io',
        'description': 'Remote job board with good API access'
    },
    'timesjobs': {
        'jobs': get_timesjobs_jobs,
        'link': 'https://www.timesjobs.com',
        'description': 'Leading job portal in India'
    },
    'remote': {
        'jobs': get_remote_jobs,
        'link': 'https://remote.co',
        'description': 'Remote work job board'
    },
    'weworkremotely': {
        'jobs': get_weworkremotely_jobs,
        'link': 'https://weworkremotely.com',
        'description': 'Remote-first job board'
    }
}

def safe_scrape_with_fallback(scraper_func, platform_name, keywords, location=None, max_retries=2):
    """Safely execute scraper with fallback and retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"Attempting to scrape {platform_name} (attempt {attempt + 1})")
            jobs = scraper_func(keywords, location)
            if jobs:
                print(f"Successfully scraped {len(jobs)} jobs from {platform_name}")
                return jobs
            else:
                print(f"No jobs found on {platform_name}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(3, 6))
        except Exception as e:
            print(f"Error scraping {platform_name} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(5, 10))
    
    print(f"Failed to scrape {platform_name} after {max_retries} attempts")
    return []

# Test function to verify scrapers work
def test_scrapers(keywords="python developer"):
    """Test all scrapers with given keywords"""
    print(f"Testing scrapers with keywords: {keywords}")
    
    for platform, config in all_jobs.items():
        print(f"\n--- Testing {platform.upper()} ---")
        try:
            # Use the safe scraper function
            jobs = safe_scrape_with_fallback(config['jobs'], platform, keywords)
            if jobs:
                print(f"Found {len(jobs)} jobs")
                for i, job in enumerate(jobs[:3], 1):  # Show first 3
                    print(f"{i}. {job.get('title', 'No title')}")
            else:
                print("No jobs found or scraping failed")
        except Exception as e:
            print(f"Error testing {platform}: {e}")
        
        time.sleep(1)  # Be respectful to servers

async def main_task():
    upwork_jobs = await get_upwork_jobs(keywords=['python', 'developer'])
    print(upwork_jobs)

if __name__ == "__main__":
    test_scrapers()
