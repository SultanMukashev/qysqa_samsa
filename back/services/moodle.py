import asyncio
import re
from pathlib import Path
import aiofiles
from uuid import uuid4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from services.s3 import S3Service
from db.models import Lesson

class MoodleService:
    def __init__(self, username=None, password=None, headless=True):
        self.username = username
        self.password = password
        self.headless = headless
        self.download_path = Path("interim_data")
        self.base_url = "https://moodle.sdu.edu.kz"
        self.driver = None

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--download.default_directory={str(self.download_path.absolute())}")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    async def login(self):
        try:
            self._setup_driver()
            self.driver.get(f"{self.base_url}/login/index.php")
            
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.ID, "loginbtn")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            
            if self.driver.current_url != f"{self.base_url}/my/courses.php":
                return {"error": "Authentication failed", "status": 401}
            
            full_name_element = self.driver.find_element(By.CLASS_NAME, "rui-fullname")
            full_name = full_name_element.text.strip()
            
            if full_name:
                parts = full_name.split()
                first_name = parts[0] if len(parts) > 0 else ""
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            else:
                first_name = last_name = ""

            return {
                "username": self.username,
                "first_name": first_name,
                "last_name": last_name,
                "status": 201
            }
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return {"error": str(e), "status": 401}
        finally:
            if self.driver:
                self.driver.quit()

    async def get_courses(self):
        try:
            self._setup_driver()
            self.driver.get(f"{self.base_url}/login/index.php")
            
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.ID, "loginbtn")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            
            if self.driver.current_url != f"{self.base_url}/my/courses.php":
                return []
            
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rui-course-card"))
            )
            
            course_cards = self.driver.find_elements(By.CLASS_NAME, "rui-course-card")
            courses = []
            
            for card in course_cards:
                course_id = card.get_attribute("data-course-id")
                title_element = card.find_element(By.CSS_SELECTOR, ".rui-course-card-title .multiline")
                full_title = title_element.text.strip() if title_element else ""
                
                if course_id:
                    courses.append({
                        "course_id": course_id,
                        "full_title": full_title
                    })
            
            return courses
            
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    async def process_course_files(self, course_id: int, user_id: int):
        self.download_path.mkdir(exist_ok=True, parents=True)
        
        try:
            self._setup_driver()
            self.driver.get(f"{self.base_url}/login/index.php")
            
            # Login
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.ID, "loginbtn")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            
            # Navigate to course page
            self.driver.get(f"{self.base_url}/course/view.php?id={course_id}")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "activity-item"))
            )

            # Get file links
            file_links = []
            resource_links = self.driver.find_elements(By.CSS_SELECTOR, 'div.activityname a.aalink[href*="/mod/resource/view.php"]')
            
            for link in resource_links:
                name = link.find_element(By.CLASS_NAME, "instancename").text.strip()
                name = re.sub(r'[<>:"/\\|?*]', '_', name)
                name = re.sub(r'\s+', ' ', name)
                url = link.get_attribute("href")
                
                file_links.append({
                    "name": name,
                    "url": url
                })

            # Process each file
            for link in file_links:
                try:
                    self.driver.get(link['url'])
                    # Wait for download to complete (you might need to adjust this based on your needs)
                    await asyncio.sleep(2)  # Simple wait for download to start
                    
                    # Find the downloaded file
                    downloaded_file = list(self.download_path.glob(f"*{Path(link['name']).name}"))[0]
                    
                    if downloaded_file:
                        async with aiofiles.open(downloaded_file, 'rb') as f:
                            file_content = await f.read()
                        
                        s3_url = await self.s3_service.upload(
                            file_content=file_content,
                            filename=f"{uuid4()}_{Path(link['name']).name}",
                            user_id=user_id
                        )
                        
                        lesson = Lesson(
                            title=link['name'],
                            content_file_url=s3_url,
                            course_id=course_id
                        )
                        self.db.add(lesson)
                        
                except Exception as e:
                    print(f"Error processing {link['name']}: {str(e)}")
                finally:
                    downloaded_file.unlink(missing_ok=True)
            
            await self.db.commit()

        except Exception as e:
            await self.db.rollback()
            print(f"Course processing failed: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()