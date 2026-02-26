import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Dashboard from "./pages/Dashboard";
import Generatedemail from "./pages/Generatedemail";
import Enrichmentlog from "./pages/Enrichmentlog";
import Scorehistory from "./pages/Scorehistory";
import Contact from "./pages/Contact";
import Company from "./pages/Company";
import Opportunity from "./pages/Opportunity";
import Task from "./pages/Task";
import Emailtemplate from "./pages/Emailtemplate";
import Interaction from "./pages/Interaction";
import Tag from "./pages/Tag";
import User from "./pages/User";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/generatedemail" element={<Generatedemail />} />
            <Route path="/enrichmentlog" element={<Enrichmentlog />} />
            <Route path="/scorehistory" element={<Scorehistory />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/company" element={<Company />} />
            <Route path="/opportunity" element={<Opportunity />} />
            <Route path="/task" element={<Task />} />
            <Route path="/emailtemplate" element={<Emailtemplate />} />
            <Route path="/interaction" element={<Interaction />} />
            <Route path="/tag" element={<Tag />} />
            <Route path="/user" element={<User />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
