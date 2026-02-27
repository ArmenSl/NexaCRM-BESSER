import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Generatedemail from "./pages/Generatedemail";
import Enrichmentlog from "./pages/Enrichmentlog";
import Scorehistory from "./pages/Scorehistory";
import Contact from "./pages/Contact";
import ContactDetail from "./pages/ContactDetail";
import Company from "./pages/Company";
import Opportunity from "./pages/Opportunity";
import Task from "./pages/Task";
import Emailtemplate from "./pages/Emailtemplate";
import Interaction from "./pages/Interaction";
import Tag from "./pages/Tag";
import User from "./pages/User";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

function App() {
  return (
    <AuthProvider>
      <TableProvider>
        <div className="app-container">
          <main className="app-main">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/generatedemail" element={<ProtectedRoute><Generatedemail /></ProtectedRoute>} />
              <Route path="/enrichmentlog" element={<ProtectedRoute><Enrichmentlog /></ProtectedRoute>} />
              <Route path="/scorehistory" element={<ProtectedRoute><Scorehistory /></ProtectedRoute>} />
              <Route path="/contact" element={<ProtectedRoute><Contact /></ProtectedRoute>} />
              <Route path="/contact/:id" element={<ProtectedRoute><ContactDetail /></ProtectedRoute>} />
              <Route path="/company" element={<ProtectedRoute><Company /></ProtectedRoute>} />
              <Route path="/opportunity" element={<ProtectedRoute><Opportunity /></ProtectedRoute>} />
              <Route path="/task" element={<ProtectedRoute><Task /></ProtectedRoute>} />
              <Route path="/emailtemplate" element={<ProtectedRoute><Emailtemplate /></ProtectedRoute>} />
              <Route path="/interaction" element={<ProtectedRoute><Interaction /></ProtectedRoute>} />
              <Route path="/tag" element={<ProtectedRoute><Tag /></ProtectedRoute>} />
              <Route path="/user" element={<ProtectedRoute><User /></ProtectedRoute>} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </main>
        </div>
      </TableProvider>
    </AuthProvider>
  );
}
export default App;
