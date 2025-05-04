from pathlib import Path
import aiofiles
from uuid import uuid4
from playwright.async_api import async_playwright
from .entities import Lesson

class MoodleService:
    def __init__(self, username, password, headless=True):
        self.username = username
        self.password = password
        self.headless = headless
        self.download_path = Path("interim_data")
        self.base_url = "https://moodle.sdu.edu.kz"


    async def login(self):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                await page.goto(f"{self.base_url}/login/index.php")
                await page.fill("#username", self.username)
                await page.fill("#password", self.password)
                await page.click("#loginbtn")
                
                if page.url != f"{self.base_url}/my/courses.php":
                    return {"error": "Authentication failed", "status": 401}
                
                full_name = await page.text_content(".rui-fullname")
                if full_name:
                    parts = full_name.strip().split()
                    first_name = parts[0] if len(parts) > 0 else ""
                    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
                else:
                    first_name = last_name = ""

                return {
                    "username": self.username,
                    "firstName": first_name,
                    "lastName": last_name,
                    "status": 201
                }
                
            except Exception as e:
                print(f"Authentication error: {str(e)}")
                return {"error": str(e), "status": 401}
            finally:
                await browser.close()

        
    async def get_courses(self):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Authenticate
                await page.goto(f"{self.base_url}/login/index.php")
                await page.fill("#username", self.username)
                await page.fill("#password", self.password)
                await page.click("#loginbtn")
                
                if page.url != f"{self.base_url}/my/courses.php":
                    return []
                
                await page.wait_for_selector(".rui-course-card", timeout=15000)
                
                courses = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rui-course-card'))
                        .map(card => {
                            const titleElement = card.querySelector(
                                '.rui-course-card-title .multiline'
                            );
                            return {
                                courseId: card.dataset.courseId,
                                fullTitle: titleElement?.innerText.trim() || ''
                            };
                        }).filter(c => c.courseId);
                }''')
                
                return courses
            
            except Exception as e:
                print(f"Scraping error: {str(e)}")
                return []
            finally:
                await browser.close()

        
    async def process_course_files(self, course_id: int, user_id: int):
        self.download_path.mkdir(exist_ok=True, parents=True)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                accept_downloads=True,
                downloads_path=str(self.download_path)
            )
            
            try:
                page = await context.new_page()
                
                # Authenticate
                await self._moodle_login(page, user_id)
                
                # Navigate to course page
                await page.goto(f"{self.base_url}/course/view.php?id={course_id}")
                await page.wait_for_selector(".activity-item", timeout=15000)

                # Get file links
                file_links = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll(
                        'div.activityname a.aalink[href*="/mod/resource/view.php"]'
                    )).map(link => ({
                        name: link.querySelector('.instancename')
                            .textContent.trim()
                            .replace(/[<>:"/\\\\|?*]/g, '_')
                            .replace(/\\s+/g, ' '),
                        url: link.href
                    }));
                }''')

                # Process each file
                for link in file_links:
                    file_path = await self._download_file(context, link['url'], link['name'])
                    if file_path:
                        try:
                            async with aiofiles.open(file_path, 'rb') as f:
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
                            file_path.unlink(missing_ok=True)
                
                await self.db.commit()

            except Exception as e:
                await self.db.rollback()
                print(f"Course processing failed: {str(e)}")
                raise
            finally:
                await context.close()
                await browser.close()