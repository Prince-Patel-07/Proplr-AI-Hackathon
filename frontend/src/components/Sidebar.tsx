import { Activity, Bell, BookOpen, Clock3, LayoutDashboard, Settings, ShieldCheck, GitCommitHorizontal } from "lucide-react";

type Page = "Overview" | "Active incidents" | "Incident history" | "Recent changes" | "Settings";

const links = [
  { label: "Overview" as Page, icon: LayoutDashboard },
  { label: "Active incidents" as Page, icon: Bell, count: "3" },
  { label: "Incident history" as Page, icon: BookOpen },
  { label: "Recent changes" as Page, icon: GitCommitHorizontal },
  { label: "Settings" as Page, icon: Settings }
];

export default function Sidebar({ page, onNavigate }: { page: Page; onNavigate: (page: Page) => void }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><ShieldCheck size={21} /></div>
        <div><strong>proplr<span>sentinel</span></strong><small>INCIDENT INTELLIGENCE</small></div>
      </div>
      <div className="workspace-label">WORKSPACE</div>
      <div className="workspace-switch"><div className="workspace-dot" /> Proplr Engineering <span>⌄</span></div>
      <nav className="nav-list">
        {links.map(({ label, icon: Icon, count }) => (
          <button key={label} className={`nav-link ${page === label ? "active" : ""}`} onClick={() => onNavigate(label)}>
            <Icon size={17} /><span>{label}</span>{count && <em>{count}</em>}
          </button>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <div className="status-card"><span className="pulse-dot" /><div><b>All systems operational</b><small>Demo environment</small></div></div>
        <div className="profile"><div className="avatar">PS</div><div><b>Proplr Sentinel</b><small>Engineering workspace</small></div><span>···</span></div>
      </div>
    </aside>
  );
}