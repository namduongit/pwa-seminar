import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App'
import { AuthProvider } from './providers/AuthProvider'
import { PoiOwnerProvider } from './providers/PoiOwnerProvider'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <PoiOwnerProvider>
        <App />
      </PoiOwnerProvider>
    </AuthProvider>
  </StrictMode>,
)
