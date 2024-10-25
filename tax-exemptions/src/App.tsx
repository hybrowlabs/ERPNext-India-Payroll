import './App.css'
import {FrappeProvider} from 'frappe-react-sdk'
import {EmployeeTaxExemptionDashboard} from "@/components/EmployeeTaxExemptionDashboard.tsx";

function App() {

    return (
        <div className="App">
            <FrappeProvider>
                <EmployeeTaxExemptionDashboard/>
            </FrappeProvider>
        </div>
    )
}

export default App
