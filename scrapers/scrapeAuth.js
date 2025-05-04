const { chromium } = require("playwright");

async function authMoodleScraper(username, password) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto("https://moodle.sdu.edu.kz/login/index.php");
    await page.fill("#username", username);
    await page.fill("#password", password);
    await page.click("#loginbtn");

    // Проверяем, что авторизация прошла успешно
    if (page.url() !== "https://moodle.sdu.edu.kz/my/courses.php") {
      return { error: "Ошибка авторизации", status: 401 };
    }

    const fullName = await page.textContent(".rui-fullname");
    const [firstName, lastName] = fullName?.trim().split(" ");

    return { username, password, firstName, lastName, status: 201 };
  } catch (error) {
    console.error("Ошибка:", error.message);
    return { error: "Ошибка авторизации", status: 401 };
  } finally {
    await browser.close();
  }
}

(async () => {
  let x = await authMoodleScraper("220107013@stu.sdu.edu.kz", "Ansar2003");
  console.log(x);
})();
