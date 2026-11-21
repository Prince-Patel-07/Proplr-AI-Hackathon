import type { Investigation } from "../types";

export const investigations: Investigation[] = [
  {
    alertId: "ALR-001",
    service: "payments-api",
    severity: "Critical",
    status: "Investigating",
    title: "Database connection pool exhausted",
    description: "Requests timing out; database connections maxed",
    time: "Today, 10:42 AM",
    likelyCause: "Database connection pool exhaustion",
    confidence: 92,
    causeNote: "A highly similar historical incident was resolved by adjusting the connection pool and recycling saturated workers. This is a strong match, not proof that the current incident has the identical cause.",
    relatedIncidents: [
      {
        id: "INC-0087",
        title: "Payments API DB connection pool exhausted",
        date: "Nov 14, 2026",
        similarity: 94,
        resolution: "Raised the pool limit after confirming database capacity, then recycled affected workers.",
        runbookId: "RB-012"
      }
    ],
    recentChanges: [
      { id: "CHG-0408", service: "payments-api", title: "Connection timeout configuration updated", time: "Today, 9:58 AM", author: "Platform team", kind: "Configuration" }
    ],
    knownFix: "Review RB-012. Confirm database capacity before changing pool limits; then recycle affected workers if appropriate.",
    runbookId: "RB-012",
    evidence: ["Alert reports database connections at maximum.", "Historical incident INC-0087 has a 94% text similarity match.", "The historical incident references runbook RB-012."],
    limitations: ["The dashboard uses demonstration data until connected to the team's backend.", "The historical resolution is guidance for an engineer to verify, not an automatic fix."]
  },
  {
    alertId: "ALR-002",
    service: "checkout-service",
    severity: "High",
    status: "Investigating",
    title: "Elevated HTTP 5xx errors",
    description: "5xx errors at 8% of requests",
    time: "Today, 10:30 AM",
    likelyCause: "Recent deployment may be contributing to the errors",
    confidence: 78,
    causeNote: "A deployment to checkout-service occurred 15 minutes before this alert. Timing makes it a plausible lead, but correlation alone does not establish causation.",
    relatedIncidents: [],
    recentChanges: [
      { id: "DEP-0412", service: "checkout-service", title: "Deployment released to production", time: "Today, 10:15 AM", author: "Release pipeline", kind: "Deployment" },
      { id: "CHG-0411", service: "checkout-service", title: "Checkout validation rules updated", time: "Today, 9:50 AM", author: "Checkout team", kind: "Configuration" }
    ],
    knownFix: null,
    runbookId: null,
    evidence: ["Alert reports an 8% HTTP 5xx rate.", "Deployment DEP-0412 occurred 15 minutes before the alert.", "No sufficiently similar past incident is available in this demo dataset."],
    limitations: ["The deployment is a possible cause, not a confirmed root cause.", "Check deployment health, error traces and rollback criteria before taking action."]
  },
  {
    alertId: "ALR-003",
    service: "notification-service",
    severity: "High",
    status: "Investigating",
    title: "Email delivery backlog",
    description: "Email queue backlog; SMTP failures",
    time: "Today, 10:51 AM",
    likelyCause: "Not enough evidence to identify a likely cause",
    confidence: 0,
    causeNote: "No historical notification-service email incident matched the configured similarity threshold. Sentinel is deliberately showing uncertainty rather than inventing a fix.",
    relatedIncidents: [],
    recentChanges: [
      { id: "CHG-0402", service: "notification-service", title: "SMTP retry interval adjusted", time: "Today, 10:20 AM", author: "Messaging team", kind: "Configuration" }
    ],
    knownFix: null,
    runbookId: null,
    evidence: ["Alert reports an email queue backlog and SMTP failures.", "No matching historical email incident was found above the demo similarity threshold.", "A recent SMTP retry configuration change is available to investigate."],
    limitations: ["No known fix was found in the available incident history.", "Inspect SMTP provider status, credentials, rate limits and queue consumer health."]
  }
];