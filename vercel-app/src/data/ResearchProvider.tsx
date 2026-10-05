import type { ReactNode } from 'react';
import { ResearchContext, useResearchStore, type MockOptions } from './researchStore';

export function ResearchProvider({children,...options}:MockOptions&{children:ReactNode}) {
  return <ResearchContext.Provider value={useResearchStore(options)}>{children}</ResearchContext.Provider>;
}
