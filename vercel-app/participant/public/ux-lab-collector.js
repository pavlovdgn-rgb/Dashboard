/* Standalone, opt-in collector. No cookies, field values, text content or HTML. */
(function () {
  if (window.UXLabCollector) return;
  window.UXLabCollector = {
    attach({ root, study, version, endpoint, onStatus = () => {}, getContext, namespace = '' }) {
      const key = `ux-lab-clicks:${study}:${version}${namespace ? ':' + namespace : ''}`;
      let state;
      try { state = JSON.parse(sessionStorage.getItem(key)); } catch { /* New tab/session. */ }
      if (!state || !Array.isArray(state.queue)) state = { session: crypto.randomUUID(), seq: 0, queue: [] };
      let busy = false, disposed = false, dropped = 0;
      const persist = () => { try { sessionStorage.setItem(key, JSON.stringify(state)); } catch { onStatus({pending:state.queue.length,error:'Не удалось сохранить очередь в браузере'}); } };
      const status = (error = '') => { if (!disposed) onStatus({ session:state.session, pending:state.queue.length, dropped, error }); };
      async function flush() {
        if (busy || !state.queue.length) return;
        busy = true;
        const events = state.queue.slice(0, 50);
        try {
          const response = await fetch(endpoint, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({events}),keepalive:true,signal:AbortSignal.timeout(5000)});
          if (!response.ok) throw Error('Сервер недоступен. Клики остаются в очереди.');
          const result = await response.json();
          if (!Array.isArray(result.accepted)) throw Error('Сервер не подтвердил приём кликов.');
          const accepted = new Set(result.accepted);
          state.queue = state.queue.filter(event => !accepted.has(event.id));
          persist();status();
        } catch { status('Сервер недоступен. Клики остаются в очереди и будут отправлены повторно.'); }
        finally { busy = false; }
      }
      const record = data => {
        if (disposed) return;
        if (state.queue.length >= 1000) { dropped++;status('Очередь заполнена: новые события не сохранены');return; }
        state.queue.push({...data,id:crypto.randomUUID(),study,session:state.session,seq:++state.seq,version,timestamp:Date.now()});
        persist();status();void flush();
      };
      const capture = event => {
        if (!event.isTrusted || event.detail === 0 || event.button !== 0) return;
        const target = event.target instanceof Element ? event.target : null;
        if (!target || !root.contains(target) || target.closest('[data-ux-private]')) return;
        const context = getContext?.(target);
        if (getContext && !context) return;
        const surface = context ? root : root.querySelector('[data-ux-page]');
        if (!surface || !surface.contains(target)) return;
        const bounds = context ? {left:0,top:0,width:innerWidth,height:innerHeight} : surface.getBoundingClientRect();
        if (!bounds.width || !bounds.height) return;
        const x = (event.clientX - bounds.left) / bounds.width, y = (event.clientY - bounds.top) / bounds.height;
        if (x < 0 || x > 1 || y < 0 || y > 1) return;
        // Only developer-supplied identifiers; never form content or arbitrary selectors.
        const marked = target.closest('[data-ux-target]');
        const targetId = context?.target || marked?.getAttribute('data-ux-target') || target.tagName.toLowerCase();
        record({
          page:context?.page || surface.getAttribute('data-ux-page'),version,target:targetId,
          ...(context ? {context:context.view} : {}),
          x,y,vw:innerWidth,vh:innerHeight,rw:Math.round(bounds.width*100)/100,rh:Math.round(bounds.height*100)/100,
          scroll_x:scrollX,scroll_y:scrollY,timestamp:Date.now()});
      };
      // Capture phase measures the old page before React handles navigation.
      root.addEventListener('click',capture,true);
      const hidden = () => {
        if (document.visibilityState !== 'hidden' || !state.queue.length) return;
        // Keep queued events until an acknowledged retry; the server deduplicates IDs.
        navigator.sendBeacon(endpoint,new Blob([JSON.stringify({events:state.queue.slice(0,50)})],{type:'application/json'}));
      };
      document.addEventListener('visibilitychange',hidden);
      window.addEventListener('online',flush);
      const interval = setInterval(flush,1500);
      persist();status();void flush();
      return {flush,record,session:state.session,dispose() { disposed=true;clearInterval(interval);root.removeEventListener('click',capture,true);document.removeEventListener('visibilitychange',hidden);window.removeEventListener('online',flush);void flush(); }};
    }
  };
})();
