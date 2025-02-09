import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.tsx'
import './index.css'


createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <App/>
    </StrictMode>,
)

interface WindowType {
    frappe: {
        csrf_token: string;
        session: {
            user: string;
        };
    };
}

declare global {
    interface Window extends WindowType {
    }
}
