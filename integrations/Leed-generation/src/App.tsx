import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Showcase from './Showcase'
import { ChatWindowProvider } from './data/ChatWindowContext'
import { LeadsProvider } from './data/LeadsContext'
import { ToastProvider } from './data/ToastContext'
import { GlobalChatWindow } from './screens/_shared/GlobalChatWindow'
import { ScreensIndex } from './screens/ScreensIndex'
import { screens } from './screens/registry'
import { RecordingControls } from './ux-lab/RecordingControls'

function App() {
  return (
    <LeadsProvider>
      <ToastProvider>
        <ChatWindowProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<ScreensIndex />} />
              <Route path="/showcase" element={<Showcase />} />
              {screens.map((screen) => (
                <Route key={screen.id} path={screen.route} element={<screen.component />} />
              ))}
            </Routes>
            {/* Смонтирован рядом с <Routes>, не внутри — переживает переход между разделами (см. ChatWindowContext). */}
            <GlobalChatWindow />
            {new URLSearchParams(location.search).get('ux_preview')!=='1'&&['localhost','127.0.0.1'].includes(location.hostname)?<RecordingControls />:null}
          </BrowserRouter>
        </ChatWindowProvider>
      </ToastProvider>
    </LeadsProvider>
  )
}

export default App
