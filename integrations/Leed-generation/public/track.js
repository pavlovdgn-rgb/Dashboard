/**
 * Трекер юзер-тестов. Вставляется в прототип (директива делает это сама).
 * Пишет события по экранам/элементам — без пиксельных координат и без ввода пользователя.
 *
 * Конфиг (любой из):
 *   - <script src=".../track.js" data-endpoint="https://IP:порт/collect"></script>
 *   - window.__UT_ENDPOINT__ = "https://IP:порт/collect" до подключения скрипта
 *
 * События: session_start, pageview, click, screen_time, session_end.
 */
(function () {
  "use strict";

  var endpoint =
    (document.currentScript && document.currentScript.dataset.endpoint) ||
    window.__UT_ENDPOINT__ ||
    "/collect";

  // ── Сессия ───────────────────────────────────────────────
  function uid() {
    return (
      Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10)
    );
  }
  var sessionId;
  try {
    sessionId = sessionStorage.getItem("ut_sid");
    if (!sessionId) {
      sessionId = uid();
      sessionStorage.setItem("ut_sid", sessionId);
    }
  } catch (e) {
    sessionId = uid();
  }
  // постоянный id тестировщика (между сессиями) — чтобы считать УНИКАЛЬНЫХ людей, а не сессии
  var visitorId;
  try {
    visitorId = localStorage.getItem("ut_vid");
    if (!visitorId) {
      visitorId = uid();
      localStorage.setItem("ut_vid", visitorId);
    }
  } catch (e) {
    visitorId = sessionId;
  }

  // ── Метка U-теста ────────────────────────────────────────
  // Ссылка вида .../prototype?ut_task=<id-сценария> привязывает весь визит
  // к конкретному сценарию. Держим метку весь визит (даже после смены маршрута).
  var task = null;
  try {
    var q = new URLSearchParams(location.search);
    var fromUrl = q.get("ut_task");
    if (fromUrl) {
      task = fromUrl;
      sessionStorage.setItem("ut_task", task);
    } else {
      task = sessionStorage.getItem("ut_task");
    }
  } catch (e) {
    task = null;
  }

  // ── Очередь и отправка ───────────────────────────────────
  var queue = [];
  var FLUSH_MS = 4000;
  var FLUSH_MAX = 20;

  function now() {
    return new Date().toISOString();
  }

  function push(type, extra) {
    var ev = {
      ts: now(),
      sessionId: sessionId,
      visitorId: visitorId,
      type: type,
      screen: currentScreen(),
    };
    if (task) ev.task = task;
    if (extra) for (var k in extra) ev[k] = extra[k];
    queue.push(ev);
    if (queue.length >= FLUSH_MAX) flush();
  }

  function flush(useBeacon) {
    if (!queue.length) return;
    var batch = queue.splice(0, queue.length);
    var body = JSON.stringify({ events: batch });
    try {
      if (useBeacon && navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
      } else {
        fetch(endpoint, {
          method: "POST",
          headers: /ngrok/i.test(endpoint)
            ? { "Content-Type": "application/json", "ngrok-skip-browser-warning": "1" }
            : { "Content-Type": "application/json" },
          body: body,
          keepalive: true,
        }).catch(function () {
          /* тест продолжается даже если сбор недоступен */
        });
      }
    } catch (e) {
      /* не мешаем прототипу */
    }
  }

  // ── Текущий экран ────────────────────────────────────────
  function currentScreen() {
    // путь без query/hash — это «экран» в SPA
    return location.pathname || "/";
  }

  // ── Время на экране ──────────────────────────────────────
  var screenEnteredAt = Date.now();
  var lastScreen = currentScreen();

  function leaveScreen() {
    var ms = Date.now() - screenEnteredAt;
    if (ms > 0) push("screen_time", { screen: lastScreen, ms: ms });
  }

  function enterScreen() {
    screenEnteredAt = Date.now();
    lastScreen = currentScreen();
    push("pageview", { screen: lastScreen });
  }

  // ── Переходы (history API + popstate) ────────────────────
  function onRouteChange() {
    var next = currentScreen();
    if (next === lastScreen) return;
    leaveScreen();
    enterScreen();
  }

  ["pushState", "replaceState"].forEach(function (m) {
    var orig = history[m];
    if (typeof orig === "function") {
      history[m] = function () {
        var r = orig.apply(this, arguments);
        onRouteChange();
        return r;
      };
    }
  });
  window.addEventListener("popstate", onRouteChange);

  // ── Клики (по элементу, не по пикселям) ──────────────────
  function describe(el) {
    if (!el) return "unknown";
    // приоритет — явная разметка data-track, затем роль/текст
    var dt = el.closest && el.closest("[data-track]");
    if (dt) return dt.getAttribute("data-track");
    var t = el.closest && el.closest("button, a, [role='button'], input, select");
    if (t) {
      var label =
        (t.getAttribute && (t.getAttribute("aria-label") || t.name)) ||
        (t.textContent || "").trim().slice(0, 40);
      return (t.tagName.toLowerCase() + (label ? ": " + label : "")).trim();
    }
    return el.tagName ? el.tagName.toLowerCase() : "unknown";
  }

  // выглядел ли клик «по интерактивному» (для честного dead-клика на стороне анализа)
  function isInteractive(el) {
    return !!(
      el && el.closest &&
      el.closest("button, a, [role='button'], input, select, textarea, label, [data-track], [onclick], [tabindex]")
    );
  }

  document.addEventListener(
    "click",
    function (e) {
      push("click", { screen: currentScreen(), target: describe(e.target), interactive: isInteractive(e.target) });
    },
    true
  );

  // ── Жизненный цикл ───────────────────────────────────────
  window.addEventListener("load", function () {
    push("session_start", { ua: navigator.userAgent });
    enterScreen();
  });

  setInterval(function () {
    flush(false);
  }, FLUSH_MS);

  window.addEventListener("pagehide", function () {
    leaveScreen();
    push("session_end", {});
    flush(true);
  });
})();
