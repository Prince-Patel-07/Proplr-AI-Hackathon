import { AlertTriangle, ArrowUpRight, BookOpen, CheckCircle2, Clock3, GitCommitHorizontal, Search, ShieldAlert, Sparkles } from "lucide-react";
import type { Investigation } from "../types";

export default function InvestigationPanel({ item }: { item: Investigation }) {
  const confidenceClass = item.confidence >= 85 ? "strong" : item.confidence > 0 ? "moderate" : "none";
  return (
    <div className="investigation-layout">
      <section className="main-column">
        <div className="section-heading"><div><span className="eyebrow">AI INVESTIGATION</span><h2>What’s most likely happening?</h2></div><span className="live-tag"><span className="pulse-dot" /> ANALYSIS READY</span></div>
        <div className="cause-card">
          <div className="cause-top"><div className="sparkle-icon"><Sparkles size={18} /></div><span>LIKELY CAUSE</span><span className={`confidence ${confidenceClass}`}>{item.confidence ? `${item.confidence}% confidence` : "Insufficient evidence"}</span></div>
          <h3>{item.likelyCause}</h3>
          <p>{item.causeNote}</p>
          {item.confidence > 0 && <div className="confidence-track"><div style={{ width: `${item.confidence}%` }} /></div>}
        </div>

        <div className="section-heading compact"><div><span className="eyebrow">SUPPORTING CONTEXT</span><h2>Evidence & signals</h2></div><span className="muted-small">{item.evidence.length} signals</span></div>
        <div className="evidence-list">
          {item.evidence.map((signal, i) => <div className="evidence-row" key={i}><div className="evidence-check"><CheckCircle2 size={16} /></div><p>{signal}</p><span>Signal {String(i + 1).padStart(2, "0")}</span></div>)}
        </div>

        <div className="section-heading compact"><div><span className="eyebrow">CHANGE CORRELATION</span><h2>Recent changes</h2></div><span className="muted-small">{item.recentChanges.length} found</span></div>
        <div className="change-list">
          {item.recentChanges.length ? item.recentChanges.map((change) => (
            <div className="change-row" key={change.id}><div className="change-icon"><GitCommitHorizontal size={17} /></div><div className="change-info"><b>{change.title}</b><small>{change.id} · {change.author} · {change.kind}</small></div><time>{change.time}</time></div>
          )) : <div className="empty-state">No relevant recent changes found in the demo data.</div>}
        </div>
      </section>

      <aside className="side-column">
        <div className="side-card">
          <div className="side-card-title"><BookOpen size={17} /><b>Known fix / runbook</b></div>
          {item.knownFix ? <><span className="runbook-id">{item.runbookId}</span><p>{item.knownFix}</p><button className="text-button" onClick={() => window.alert(`Demo runbook ${item.runbookId}: ${item.knownFix}`)}>View runbook <ArrowUpRight size={14} /></button></> :
            <div className="no-fix"><Search size={19} /><b>No known fix found</b><span>There isn’t a verified historical resolution for this alert in the available data.</span></div>}
        </div>
        <div className="side-card">
          <div className="side-card-title"><Clock3 size={17} /><b>Related incidents</b><span className="count-pill">{item.relatedIncidents.length}</span></div>
          {item.relatedIncidents.length ? item.relatedIncidents.map((incident) => <div className="related-incident" key={incident.id}><div><b>{incident.id}</b><span>{incident.similarity}% match</span></div><p>{incident.title}</p><small>{incident.date}</small><div className="resolution-note">{incident.resolution}</div></div>) :
            <div className="no-match"><ShieldAlert size={19} /><b>No close historical match</b><span>Sentinel found no incident above the demo similarity threshold.</span></div>}
        </div>
        <div className="side-card caution-card">
          <div className="side-card-title"><AlertTriangle size={17} /><b>Investigation boundaries</b></div>
          {item.limitations.map((note, i) => <p className="limitation" key={i}>{note}</p>)}
          <div className="human-note">Engineer review required · No automated remediation</div>
        </div>
      </aside>
    </div>
  );
}