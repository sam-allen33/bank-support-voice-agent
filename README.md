# Bank Support Voice Agent — A Hands-On Study of Voice AI Deployment

A working prototype of a Tier-1 banking phone-support agent, built on ElevenLabs
Agents. I built this to understand — by doing, not just reading — what it actually
takes to deploy a voice AI agent against a real business problem: where the work is,
where it breaks, and what would have to change to put something like this in front
of real customers.

<img width="1078" height="946" alt="Conversation History" src="https://github.com/user-attachments/assets/c3cb3cfe-4082-4a82-9e0e-614414c6caaa" />


---

## What it does

A caller can speak to an AI agent that:

- **Looks up live account data** — calls a balance/transactions API mid-conversation
  (a webhook tool) and speaks the result back, rather than inventing numbers.
- **Answers policy questions from a source of truth** — fees, transfers, disputes,
  and card questions are grounded in a knowledge base (RAG), not guessed.
- **Stays in its lane** — it declines money transfers and financial advice and offers
  to hand off to a human, enforced as a guardrail.
- **Scores itself** — every conversation is auto-evaluated on whether it resolved the
  caller's request, so quality is measurable, not anecdotal.

```
  Caller (voice)  ──►  ElevenLabs Agent  ──►  Balance / Transactions API  (mock "core banking")
                         │  brain + voice        ▲
                         │                       │ webhook tool call
                         └── Knowledge base ─────┘ (fees & policy, via RAG)
```

## How it's built

| Piece | What it is |
|---|---|
| **Agent** | ElevenLabs Agent: system prompt = the "conversation contract" (verify, don't advise, escalate). |
| **`mock_bank.py`** | A small FastAPI service standing in for a bank's core systems. Returns demo balance + transactions. |
| **Webhook tools** | `get_account_balance` and `list_recent_transactions` — how the agent reaches the API. |
| **Knowledge base** | `northwind_fees_faq.md` — fee/policy doc the agent grounds its answers in. |
| **Evaluation** | A `solved_user_inquiry` criterion that grades each call success/failure with a rationale. |

Full build steps are in **[SETUP.md](./SETUP.md)** if you want to run it yourself.

## What I learned

Although this is a simple tool to navigate the deployment process and outline integration, certain key principles became clear. 
The voice and agent itself was instantaneous. The real work behinding deploying these tools to drive efficiency isn't picking a voice,
it's ensuring the system is wired correctly. Reliably connecting the agent to a backend and making it call the right thing, at
the write time is the work. Finally, determining outcomes and setting guidelines to conversations of success or failure. Insights,
at this level are crucial to the development of the model and analytics for the user. 

## What production would actually require

This is a learning prototype. Shipping something like it at a real bank would mean
addressing the parts a demo gets to skip — which is where most of the deployment work
really lives:

- **Identity & payments security.** Replace the mock check with the bank's real
  step-up auth (OTP / push), and keep card numbers out of the voice channel entirely
  (secure DTMF capture) to stay out of PCI scope. The agent should never handle raw
  secrets — only trigger the bank's existing auth and read a pass/fail.
- **Data handling & compliance.** Zero-Retention processing for PII and financial
  data, EU data residency, and the controls behind SOC 2 / ISO 27001 / GDPR. Pipe
  transcripts and evaluation results to the bank's data lake for audit.
- **Telephony.** Swap the demo phone setup for a SIP trunk into the bank's existing
  contact center (no number porting), with encrypted signaling/media — rather than a
  standalone test number.
- **Conversation design.** Promote the single agent to a workflow with a *deterministic*
  identity gate before any account data is disclosed, and put consequential actions
  (freeze card, open dispute) behind explicit read-back confirmation, with read-only
  lookups kept fast.
- **Scale & reliability.** Size for peak concurrency (e.g. Monday-morning call spikes),
  with a clean fallback to a human queue and real-time monitoring.
- **Measurement.** Split evaluation into separate criteria — resolution, scope
  adherence, and escalation — and track containment rate as the headline metric.
- **Duty of care.** Route suspected fraud, financial hardship, and vulnerable callers
  straight to a human, as a first-class behavior rather than an afterthought.



---

Samuel Allen - Deployment - Identifying Opportunity
