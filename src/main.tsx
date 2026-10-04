import ReactDOM from 'react-dom/client';
import './icons';
import './fonts';
import './tokens/primitives.css';
import './tokens/semantics.css';
import './tokens/typography.css';
import './global.css';
import { Showcase } from './pages/Showcase';
import { ResultsOverview } from './pages/ResultsOverview';
import { LocalTarget } from './heatmap/LocalTarget';
import { ExportHeatmap } from './heatmap/ExportHeatmap';
import { ThemeFrame } from './storybook/ThemeFrame';
import { ConnectionPilot } from './connections/ConnectionPilot';

// EUI 106's legacy EuiObserver disconnects on StrictMode's simulated unmount
// without reconnecting on remount. Keep the catalog's dev layout consistent
// with production (accordions and other measured components depend on it).
const screen=new URLSearchParams(window.location.search).get('screen');
ReactDOM.createRoot(document.getElementById('root')!).render(screen==='connections'?<ThemeFrame mode="light" scale="medium" product><ConnectionPilot/></ThemeFrame>:screen==='heatmap-export'?<ThemeFrame mode="light" scale="medium" product><ExportHeatmap/></ThemeFrame>:screen==='heatmap-target'?<ThemeFrame mode="light" scale="medium" product><LocalTarget/></ThemeFrame>:screen==='results-overview'
  ? <ThemeFrame mode="light" scale="medium" product><ResultsOverview live/></ThemeFrame>
  : screen==='showcase'||new URLSearchParams(location.search).has('component')?<Showcase />:<ThemeFrame mode="light" scale="medium" product><ResultsOverview live/></ThemeFrame>);
