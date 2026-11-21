export type Severity = "Critical" | "High" | "Medium";
export type IncidentStatus = "Investigating" | "Monitoring" | "Resolved";

export interface RelatedIncident {
  id: string;
  title: string;
  date: string;
  similarity: number;
  resolution: string;
  runbookId?: string;
}

export interface Change {
  id: string;
  service: string;
  title: string;
  time: string;
  author: string;
  kind: string;
}

export interface Investigation {
  alertId: string;
  service: string;
  severity: Severity;
  status: IncidentStatus;
  title: string;
  description: string;
  time: string;
  likelyCause: string;
  confidence: number;
  causeNote: string;
  relatedIncidents: RelatedIncident[];
  recentChanges: Change[];
  knownFix: string | null;
  runbookId: string | null;
  evidence: string[];
  limitations: string[];
}