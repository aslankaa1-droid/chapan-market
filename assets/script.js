// Чапан · общий скрипт сайта: переключатель темы

(function() {
  const STORAGE_KEY = 'chapan-theme';
  const html = document.documentElement;

  // Получить сохранённую или определить дефолтную тему
  function getTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && ['light', 'dark', 'auto'].includes(saved)) return saved;
    return 'auto';
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    // Обновить активную кнопку
    document.querySelectorAll('.theme-switch button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === theme);
    });
  }

  // Инициализация при загрузке
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(getTheme());

    // Подключить обработчики кнопок темы
    document.querySelectorAll('.theme-switch button').forEach(btn => {
      btn.addEventListener('click', () => applyTheme(btn.dataset.theme));
    });
  });

  // Применить тему сразу (до DOMContentLoaded, чтобы не было flash)
  applyTheme(getTheme());
})();
