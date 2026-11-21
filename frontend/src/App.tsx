import { useEffect, useState } from "react";
import { Activity, ArrowDownRight, ArrowUpRight, Bell, ChevronDown, CircleHelp, Command, Filter, MoreHorizontal, Search, ShieldCheck, Timer, Zap } from "lucide-react";
import Sidebar from "./components/Sidebar";
import InvestigationPanel from "./components/InvestigationPanel";
import { getInvestigation } from "./lib/api";
import { investigations } from "./data/demo";
import type { Investigation } from "./types";

type Page = "Overview" | "Active incidents" | "Incident history" | "Recent changes" | "Settings";

export default function App() {
  const [page, setPage] = useState<Page>("Active incidents");
  const [selectedId, setSelectedId] = useState("ALR-001");
  const [item, setItem] = useState<Investigation>(investigations[0]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [toast, setToast] = useState("");

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getInvestigation(selectedId)
      .then((data) => { if (mounted) setItem(data); })
      .catch(() => { if (mounted) setToast("Could not load investigation. Showing the last available demo view."); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [selectedId]);

  const notify = (message: string) => {
    setToast(message);
    window.setTimeout(() => setToast(""), 2600);
  };

  const filtered = investigations.filter((x) => `${x.alertId} ${x.service} ${x.title}`.toLowerCase().includes(search.toLowerCase()));
  const pageTitle = page === "Active incidents" ? "Active incidents" : page;

  return (
    <div className="app-shell">
      <Sidebar page={page} onNavigate={setPage} />
      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs"><span>Workspace</span><span>/</span><b>{pageTitle}</b></div>
          <div className="top-actions"><div className="environment"><span className="pulse-dot" /> DEMO ENVIRONMENT</div><button className="icon-button" aria-label="Help" onClick={() => notify("Demo workspace — sample incident data only.")}><CircleHelp size={18} /></button><button className="icon-button notification-button" aria-label="Notifications" onClick={() => notify("You’re all caught up.")}><Bell size={18} /><i /></button><div className="top-avatar">K</div></div>
        </header>

        <div className="page-content">
          <div className="welcome-row"><div><div className="eyebrow">SATURDAY, NOVEMBER 21, 2026 <span className="dot-separator">·</span> ENGINEERING OPERATIONS</div><h1>{page === "Active incidents" ? "Incident command" : page}</h1><p className="page-subtitle">Turn alerts into evidence-backed understanding. Faster.</p></div><button className="primary-button" onClick={() => notify("Demo refresh complete. All three sample alerts are loaded.")}><Activity size={16} /> Refresh signals</button></div>

          <div className="metrics-grid">
            <Metric icon={<Bell size={17} />} label="Active incidents" value="03" delta="2 high priority" tone="red" />
            <Metric icon={<ShieldCheck size={17} />} label="Investigations ready" value="03" delta="Evidence assembled" tone="green" />
            <Metric icon={<Timer size={17} />} label="Avg. time to know" value="2m 14s" delta="Demo metric" tone="blue" />
            <Metric icon={<Zap size={17} />} label="Known fix coverage" value="33%" delta="1 of 3 alerts matched" tone="purple" />
          </div>

          <section className="incident-workspace">
            <div className="incident-list-panel">
              <div className="list-heading"><div><span className="eyebrow">LIVE QUEUE</span><h2>Alerts <span className="count-pill">3</span></h2></div><button className="icon-button" onClick={() => notify("Showing all demo alerts.")}><Filter size={17} /></button></div>
              <div className="search-box"><Search size={15} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search alerts..." /><kbd>⌘ K</kbd></div>
              <div className="alert-items">
                {filtered.map((alert) => <button className={`alert-item ${selectedId === alert.alertId ? "selected" : ""}`} key={alert.alertId} onClick={() => { setSelectedId(alert.alertId); setPage("Active incidents"); }}>
                  <div className="alert-item-top"><span className={`severity-dot ${alert.severity.toLowerCase()}`} /> <span className={`severity-label ${alert.severity.toLowerCase()}`}>{alert.severity}</span><span className="alert-time">{alert.time.replace("Today, ", "")}</span></div>
                  <b>{alert.title}</b><span className="service-name">{alert.service}</span><p>{alert.description}</p>
                  <div className="alert-item-bottom"><span className="alert-id">{alert.alertId}</span><span className="investigating-label">● Investigating</span></div>
                </button>)}
                {!filtered.length && <div className="empty-state">No alerts match your search.</div>}
              </div>
              <button className="view-all-button" onClick={() => setSearch("")}>Clear search <ArrowUpRight size={14} /></button>
            </div>

            <div className="investigation-area">
              <div className="selected-alert-bar"><div><span className="eyebrow">SELECTED ALERT</span><h2>{item.alertId} <span className="service-chip">{item.service}</span></h2></div><div className="selected-actions"><span className="status-pill"><span className="pulse-dot" /> Investigating</span><button className="icon-button" onClick={() => notify("More incident actions are coming soon.")}><MoreHorizontal size={18} /></button></div></div>
              <div className="alert-summary"><div><span className={`severity-tag ${item.severity.toLowerCase()}`}>{item.severity} severity</span><h3>{item.description}</h3><p>Detected {item.time} <span>·</span> Source: Synthetic alert feed</p></div><button className="outline-button" onClick={() => notify("Incident note copied to the demo workspace.")}>Add incident note <ArrowDownRight size={14} /></button></div>
              {loading ? <div className="loading-state">Assembling investigation evidence…</div> : <InvestigationPanel item={item} />}
            </div>
          </section>

          <footer className="page-footer"><span><ShieldCheck size={14} /> Proplr Sentinel <span className="footer-divider">·</span> Human-led incident response</span><span>Sample data for hackathon demonstration <span className="footer-divider">·</span> v0.1.0</span></footer>
        </div>
      </main>
      {toast && <div className="toast"><CheckIcon />{toast}</div>}
    </div>
  );
}

function Metric({ icon, label, value, delta, tone }: { icon: React.ReactNode; label: string; value: string; delta: string; tone: string }) {
  return <div className="metric-card"><div className={`metric-icon ${tone}`}>{icon}</div><span>{label}</span><strong>{value}</strong><small>{delta}</small></div>;
}
function CheckIcon() { return <ShieldCheck size={16} />; }