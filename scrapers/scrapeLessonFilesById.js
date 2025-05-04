const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

async function downloadCourseFiles(username, password, courseId) {
  const downloadPath = path.resolve(__dirname, "interim_data");
  fs.mkdirSync(downloadPath, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    acceptDownloads: true,
    downloadPath: downloadPath,
  });

  try {
    const page = await context.newPage();

    // Авторизация
    await page.goto("https://moodle.sdu.edu.kz/login/index.php");
    await page.fill("#username", username);
    await page.fill("#password", password);
    await page.click("#loginbtn");

    // Проверяем, что авторизация прошла успешно
    if (page.url() !== "https://moodle.sdu.edu.kz/my/courses.php") {
      throw new Error("Авторизация не удалась!");
    }

    // Переход к курсу
    await page.goto(`https://moodle.sdu.edu.kz/course/view.php?id=${courseId}`);
    await page.waitForSelector(".activity-item", { timeout: 15000 });

    // Получаем корректные ссылки
    const fileLinks = await page.$$eval(
      'div.activityname a.aalink[href*="/mod/resource/view.php"]',
      (links) =>
        links.map((link) => {
          const url = new URL(link.href);
          //   url.pathname = url.pathname.replace("view.php", "view.php");
          //   url.searchParams.set("forcedownload", "1");

          return {
            name: link
              .querySelector(".instancename")
              .textContent.trim()
              .replace(/[<>:"/\\|?*]/g, "_")
              .replace(/\s+/g, " "),
            url: url.toString(),
          };
        })
    );

    console.log("Найдено файлов:", fileLinks.length);

    // Скачивание файлов
    for (const { name, url } of fileLinks) {
      try {
        console.log(`Инициируем скачивание: ${name}`);

        // Создаем новую вкладку в том же контексте
        const downloadPage = await context.newPage();

        // Включаем логирование сетевых запросов
        downloadPage.on("request", (request) =>
          console.log("Запрос:", request.url())
        );
        downloadPage.on("response", (response) =>
          console.log("Ответ:", response.status(), response.url())
        );

        // Инициируем скачивание через клик по элементу
        const [download] = await Promise.all([
          downloadPage.waitForEvent("download", { timeout: 15000 }),
          downloadPage.evaluate((downloadUrl) => {
            // Эмулируем клик через JavaScript
            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = true;
            link.style.display = "none";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }, url),
        ]);

        // Ожидаем завершения загрузки
        const fileName = await download.suggestedFilename();
        const savePath = path.join(downloadPath, fileName);
        await download.saveAs(savePath);

        console.log(`Успешно сохранено: ${savePath}`);
        await downloadPage.close();
      } catch (err) {
        console.error(`Ошибка при скачивании ${name}:`, err.message);
      }
    }

    console.log(`\nВсего скачано: ${fileLinks.length} файлов`);
  } catch (error) {
    console.error("Критическая ошибка:", error.message);
  } finally {
    await browser.close();
  }
}

(async () => {
  await downloadCourseFiles("220107013@stu.sdu.edu.kz", "Ansar2003", "1729");
})();
