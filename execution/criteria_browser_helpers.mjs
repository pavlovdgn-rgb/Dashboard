/** Shared interaction for the current criteria editor, using a disposable test API. */
export async function seedChatSignal(post){
 await post('/api/project/config',{mode:'free',enabled:true});
 await post('/api/project/task-events',{id:crypto.randomUUID(),study:'leed-local',session:'catalog-fixture',kind:'chat_message_sent',timestamp:1000,page:'leed-leads-table',vw:1280,vh:900});
}
export async function chooseChatCriterion(page,region){
 await region.getByLabel('Что считать успехом',{exact:true}).fill('Отправлено сообщение в чат');
 await region.getByRole('button',{name:'Как проверять результат',exact:true}).click();
 await page.getByRole('menuitemradio',{name:'Автоматически',exact:true}).click();
 await region.getByRole('button',{name:'Записанное событие',exact:true}).click();
 await page.getByRole('menuitemradio',{name:'Отправлено сообщение в чат',exact:true}).click();
}
