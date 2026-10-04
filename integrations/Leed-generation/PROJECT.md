# PROJECT

- Репозиторий: https://github.com/pavlovdgn-rgb/Leed-generation
- Ветка: main
- Содержимое репозитория: React-база (`app/` из основного рабочего каталога) — Vite + TypeScript + Storybook.
- Живая ссылка (Vercel): https://app-rose-nine-12.vercel.app
  - Путь: Vercel (проект `alex-p2/app`, подключён к GitHub-репозиторию — автопересборка на каждый пуш в `main`)
  - SPA-маршрутизация: `vercel.json` (rewrite всех путей на `/index.html`)
- Живая ссылка (свой сервер): http://45.139.76.34:8080
  - Путь: nginx на порту 8080 (`/etc/nginx/sites-available/lead-generation-app`), статика в `/var/www/lead-generation-app`
  - SPA-маршрутизация: `try_files $uri /index.html`
  - Порт 8080 выбран свободным — VPN (Amnezia, порты 49224/udp, 38467/tcp) не задет; 80/443 заняты боевым доменом pavlovdgn.ru — не трогали
  - Обновление: пересобрать локально (`npm run build`) и перезалить `dist/` на сервер (ручной шаг, авто-деплоя нет)
  - `http`, без сертификата — браузер покажет «не защищено»; для теста/демо нормально
