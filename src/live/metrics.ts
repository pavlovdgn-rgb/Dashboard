import type { LiveSummary } from './types';

/** Repeated bursts in one session still count as one affected session per page. */
export function pageSignalMetrics(data:Pick<LiveSummary,'pages'|'signals'>) {
  const sessionsByPage=new Map<string,Set<string>>();
  for(const signal of data.signals) {
    const sessions=sessionsByPage.get(signal.page)??new Set<string>();
    sessions.add(signal.session);
    sessionsByPage.set(signal.page,sessions);
  }
  return data.pages.map(page=>({...page,affectedSessions:[...(sessionsByPage.get(page.id)??[])]}));
}
