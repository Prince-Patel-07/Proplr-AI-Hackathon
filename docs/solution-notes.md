# Solution notes: answers for the judges

**The idea in one line:** when an alert fires, the engineer on call gets a short brief with the evidence already gathered, so they start from what is known and not from scratch.

## 1. How would this connect to Proplr's real tools?

Each lookup in our demo reads a sample file. In production, each one swaps to a real source, and the rest of the pipeline stays the same.

| Question | Demo today | Real source |
|---|---|---|
| What fired? | `alerts.json` | PagerDuty webhook, Google Cloud Monitoring alerts |
| Has this happened before? | `incidents.json` | PagerDuty history, tickets, postmortems |
| What changed? | `deployments.json` | CI/CD runs, infrastructure-as-code history, change tickets |
| What do the logs say? | `logs.json` | Google Cloud Logging |
| Is there a known fix? | `runbooks.json` | Proplr's runbook documents |

## 2. How do we stop the AI from being wrong or making things up?

- **Facts come from records.** Past incidents, changes and runbooks on screen come straight from the data, never from the AI.
- **Citations are checked.** If the AI cites an ID that is not in its evidence, its answer is thrown out.
- **It can say "I don't know."** With no match, the brief says "No known fix found" and lists what to check.
- **It survives failure.** If the AI is down or returns a bad answer, the app builds a plain brief from the records.
- **The engineer decides.** Nothing runs automatically. Approving only records a decision.

## 3. How does it get smarter over time?

After each fix, the system drafts an incident note in one consistent format, linked to the change that caused it. The engineer confirms it and it joins the knowledge base, so the next similar alert matches it. Our sample data already links past incidents to their causing changes and runbooks. The note drafting is the next piece to build.

## 4. What would we build from January to August?

- **Jan–Feb:** connect to real PagerDuty, Google Cloud Logging and deploy history.
- **Mar–Apr:** pilot with one client and measure MTTK before and after.
- **May–Jun:** add planned-work and provider-outage checks, and automatic incident notes.
- **Jul–Aug:** apply low-risk runbooks after engineer approval, and begin early warnings for the predictive stage.

## 5. How would we measure success?

- **MTTK:** time from alert to understanding the cause. This is the main measure.
- **MTTR:** time from alert to fix. Proplr's first submission cited an industry average of around 73 minutes.
- **Repeat incidents resolved from a documented fix:** this should rise each month.
- **Brief accuracy:** how often engineers approve the brief versus reject it.

We would baseline these during the pilot. We have not measured any time savings yet, so we make no claim about them.

## Why this fits mid-market clients

Commercial tools like PagerDuty AIOps are priced out of reach for Proplr's clients. Our matching runs locally at no cost, and the AI step uses a low-cost model and is optional, because the app still works without it.
