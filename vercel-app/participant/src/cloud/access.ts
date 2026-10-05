/** A shared workspace login. Credentials stay in an HttpOnly server cookie. */
export async function ensureAccess():Promise<void> {
  const response=await fetch('/api/auth',{cache:'no-store'}).catch(()=>null);
  if(response?.ok)return;
  const root=document.getElementById('root')!;
  root.innerHTML='<main class="cloud-login"><form><h1>UX-Lab</h1><p>Вход в рабочее пространство</p><label for="workspace-password">Пароль</label><input id="workspace-password" name="password" type="password" autocomplete="current-password" required /><p role="status" aria-live="polite"></p><button type="submit">Войти</button><p>Пароль предоставляет организатор исследования.</p></form></main>';
  const status=root.querySelector<HTMLElement>('[role="status"]')!;
  if(response?.status===503){const data=await response.json().catch(()=>({}));status.textContent=data.error||'Рабочее пространство ещё не настроено.';}
  if(!response)status.textContent='Нет связи с сервером. Попробуйте войти ещё раз.';
  await new Promise<void>(resolve=>{
    root.querySelector('form')!.onsubmit=async event=>{
      event.preventDefault();const button=root.querySelector('button')!;button.disabled=true;
      status.textContent='Проверяем пароль…';
      try {
        const password=root.querySelector<HTMLInputElement>('input')!.value;
        const result=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password})});
        const data=await result.json();
        if(!result.ok)throw Error(data.error||'Не удалось войти.');
        root.replaceChildren();resolve();
      }catch(error){status.textContent=error instanceof Error?error.message:'Не удалось войти.';}
      finally{button.disabled=false;}
    };
  });
}
