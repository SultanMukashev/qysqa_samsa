const { chromium } = require("playwright");

async function scrapeMoodleCourses(username, password) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto("https://moodle.sdu.edu.kz/login/index.php");
    await page.fill("#username", username);
    await page.fill("#password", password);
    await page.click("#loginbtn");

    // Проверяем, что авторизация прошла успешно
    if (page.url() !== "https://moodle.sdu.edu.kz/my/courses.php") {
      throw new Error("Авторизация не удалась!");
    }

    try {
      // Дополнительная проверка - ждем появления хотя бы одного курса
      await page.waitForSelector(".rui-course-card", {
        state: "attached",
        timeout: 15000,
      });
    } catch (error) {
      console.error("Курсы не загрузились:", error);
      return [];
    }

    // Проверяем количество загруженных курсов
    const courseCount = await page.$$eval(
      ".rui-course-card",
      (cards) => cards.length
    );

    if (courseCount === 0) {
      return [];
    }

    // Парсим курсы с улучшенной обработкой
    const courses = await page.$$eval(".rui-course-card", (cards) => {
      return cards
        .map((card) => {
          try {
            // Извлекаем ID курса
            const courseId = card.getAttribute("data-course-id");

            // Основная информация о курсе
            const titleElement = card.querySelector(
              ".rui-course-card-title .multiline"
            );
            const titleText = titleElement?.innerText.trim() || "";
            return {
              courseId: courseId,
              fullTitle: titleText,
              // details: {
              //   url: card.querySelector(".rui-course-card-title a")?.href,
              // },
            };
          } catch (e) {
            console.warn("Ошибка при парсинге карточки:", e);
            return null;
          }
        })
        .filter(Boolean);
    });

    console.log("Успешно распарсены курсы:", courses.length);
    return courses;
  } catch (error) {
    console.error("Ошибка:", error.message);
    return [];
  } finally {
    await browser.close();
  }
}

(async () => {
  const courses = await scrapeMoodleCourses(
    "220107013@stu.sdu.edu.kz",
    "Ansar2003"
  );

  if (courses.length > 0) {
    console.table(courses);
    // Сохраняем в JSON файл
    const fs = require("fs");
    fs.writeFileSync(
      "./results/courses.json",
      JSON.stringify(courses, null, 2)
    );
    console.log("Данные сохранены в courses.json");
  } else {
    console.log("Курсы не найдены. Проверьте:");
  }
})();
