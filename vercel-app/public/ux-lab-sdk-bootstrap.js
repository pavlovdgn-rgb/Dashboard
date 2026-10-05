/* Served after ux-lab-collector.js as one SDK. Explicit participant link required. */
(function () {
  if (window.UXLabSDK) return;
  const script = document.currentScript;
  const instances = new Map();
  const valid = value => typeof value === 'string' && /^[a-zA-Z0-9_.:-]{1,120}$/.test(value);
  const notify = detail => { window.dispatchEvent(new CustomEvent('ux-lab-sdk-status', {detail})); };
  // Technical route fingerprint; never transmit URLs, query strings or visible text.
  function pageId() {
    const marker = document.querySelector('[data-ux-page]')?.getAttribute('data-ux-page');
    if (valid(marker)) return marker;
    const route = location.pathname + (location.hash.startsWith('#/') ? location.hash.split('?')[0] : '');
    let hash = 2166136261;
    for (let i=0;i<route.length;i++) hash = Math.imul(hash ^ route.charCodeAt(i),16777619);
    return 'route-' + (hash >>> 0).toString(16);
  }
  async function start({project, api, root = document.body}) {
    if (!valid(project)) throw Error('Некорректный идентификатор подключения');
    const base = new URL(api);
    if (!['http:','https:'].includes(base.protocol)) throw Error('Некорректный адрес сборщика');
    const params = new URLSearchParams(location.search);
    if (params.get('ux_preview') === '1') return null;
    const storageKey = 'ux-lab-sdk-study:' + base.origin + ':' + project;
    const supplied = params.get('ux_study');
    let study = supplied;
    try { if (!supplied) study = sessionStorage.getItem(storageKey); } catch { /* Memory-only session. */ }
    if (!valid(study)) { notify({state:'inactive',message:'Откройте ссылку участника'}); return null; }
    const instanceKey = base.origin + ':' + project;
    if (instances.has(instanceKey)) return instances.get(instanceKey);
    const running = (async () => {
      const query = new URLSearchParams({project,study});
      const configURL = base.origin + '/api/config?' + query;
      const response = await fetch(configURL, {signal:AbortSignal.timeout(5000)});
      if (!response.ok) throw Error('Подключение или исследование не разрешено');
      const config = await response.json();
      if (config.kind !== 'web') throw Error('Для этого подключения нужен Figma-проигрыватель');
      try { sessionStorage.setItem(storageKey,study); } catch { /* Memory-only session. */ }
      let enabled = config.enabled, disposed = false, lastPage = '', checking = false;
      const collector = window.UXLabCollector.attach({root,study,version:'web-sdk-v1',
        namespace:base.origin + ':' + project, endpoint:base.origin + '/api/events?' + query,
        onStatus:detail => notify({state:enabled?'connected':'paused',...detail}),
        getContext:target => enabled ? {page:pageId(),target:valid(target.closest('[data-ux-target]')?.getAttribute('data-ux-target')) ? target.closest('[data-ux-target]').getAttribute('data-ux-target') : target.tagName.toLowerCase()} : null});
      function visit() {
        const page = pageId();
        if (disposed || !enabled || page === lastPage) return;
        lastPage = page;
        collector.record({kind:'visit',page,vw:innerWidth,vh:innerHeight});
      }
      async function policy() {
        if (checking || disposed) return;
        checking = true;
        try {
          const result = await fetch(configURL,{signal:AbortSignal.timeout(2500)});
          if (!result.ok) throw Error();
          const next = await result.json();
          if (disposed) return;
          if (!enabled && next.enabled) lastPage = '';
          enabled = next.enabled;
          visit();
        } catch { enabled = false; notify({state:'error',message:'Не удалось проверить разрешение на сбор'}); }
        finally { checking = false; }
      }
      // Polling avoids patching the host application's History methods.
      const navigationTimer = setInterval(visit,200);
      const policyTimer = setInterval(policy,2000);
      visit();
      const instance = {session:collector.session,flush:collector.flush,dispose() {
        disposed=true;enabled=false;clearInterval(navigationTimer);clearInterval(policyTimer);
        collector.dispose();instances.delete(instanceKey);
      }};
      return instance;
    })();
    instances.set(instanceKey,running);
    try { return await running; } catch (error) { instances.delete(instanceKey);throw error; }
  }
  window.UXLabSDK = {start,attach:window.UXLabCollector.attach};
  if (script?.dataset.project) {
    const run = () => { start({project:script.dataset.project,api:new URL(script.src).origin}).catch(error=>notify({state:'error',message:error.message})); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',run,{once:true});else run();
  }
})();
