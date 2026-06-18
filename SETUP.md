# Build Your First Bank Support Voice Agent — Step by Step

This is a weekend project that gets you from zero to **"I built a working voice agent"** —
the single most valuable thing you can say in a Deployment Strategist interview.

You'll end with an agent that:
1. Talks in a natural voice.
2. Calls a (fake) bank API to look up a balance and recent transactions — this is the key skill.
3. Answers fee questions from a knowledge base instead of making them up.
4. Can be reached by phone (optional).
5. Gets scored automatically on whether it solved the caller's problem.

**Time:** about 45–60 minutes. **You do NOT need to be a programmer.** You need to be
unafraid of a terminal and able to copy/paste. Every command is given to you.

---

## The big picture (read this once)

Three things are running and talking to each other:

```
   You (speaking)  ←→  ElevenLabs Agent (the brain + voice, runs in the cloud)
                              │
                              │  when you ask "what's my balance?"
                              ▼
                       Your Mock Bank API (a tiny program on your laptop)
```

The only mildly technical part is letting the ElevenLabs cloud reach the little
program on your laptop. A free tool called **ngrok** does that in one command.
Don't worry — it's spelled out below.

---

## Step 0 — What you need

- A computer with **Python 3.9 or newer**. Check by running `python3 --version`.
- A **free ElevenLabs account**: https://elevenlabs.io
- (For the tool step) A **free ngrok account**: https://ngrok.com
- (Optional, for the phone step) A **free Twilio trial**: https://twilio.com

Put all the files from this folder somewhere easy, like `~/bank-agent`. Open a
terminal **in that folder**. (On Mac: right-click the folder → "New Terminal at Folder".)

---

## Step 1 — Install the project

In your terminal, run these one at a time:

```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If the last line errors on **pyaudio**, that's only the microphone feature. Either:
- Mac: run `brew install portaudio`, then `pip install -r requirements.txt` again, OR
- just continue — you can talk to the agent in the dashboard without it.

---

## Step 2 — Get your ElevenLabs API key

1. Sign in at https://elevenlabs.io
2. Bottom-left, click your profile → **API Keys** → **Create API Key**.
3. Copy it. Then copy the file `.env.example` to a new file named `.env` and paste your key in.

---

## Step 3 — Create the agent (in the dashboard — easiest)

1. In ElevenLabs, go to **Agents** (left sidebar) → **Create agent** → **Blank template**.
2. Name it `Bank Support – Tier 1`.
3. Find the **System prompt** box and paste in the prompt from `system_prompt.txt`
   (it's in this folder). This is the agent's rulebook.
4. Pick a **voice** you like, and set the language to English.
5. Save. On the agent's page, copy the **Agent ID** into your `.env` file.

**Talk to it now.** Click **Test AI agent** and have a chat. It can talk, but it
can't look anything up yet — that's the next step. (This is already a win — you
created a working voice agent.)

---

## Step 4 — Start your fake bank API

In your terminal (with `venv` still active), run:

```bash
uvicorn mock_bank:app --reload --port 8000
```

Leave this running. Open http://127.0.0.1:8000/get_balance in your browser —
you should see fake balance data. That means your "bank" works.

---

## Step 5 — Make your laptop reachable with ngrok

Open a **second terminal window** (leave the first one running the bank) and run:

```bash
ngrok http 8000
```

It prints a public web address like `https://abc123.ngrok-free.app`. **Copy it.**
That address now points to the bank API on your laptop. (Note: it changes each
time you restart ngrok — if you restart it, update your tool URL in Step 6.)

---

## Step 6 — Give the agent "hands" (the webhook tool) ⭐

This is the most important step — it's the skill the job is really testing.

1. In your agent's settings, find **Tools** → **Add tool** → **Webhook** (sometimes
   called "Server tool" or "Custom tool").
2. Create the first tool exactly like this:
   - **Name:** `get_account_balance`
   - **Description:** `Gets the customer's current account balance and available balance. Use this whenever the caller asks how much money they have.`
   - **Method:** `GET`
   - **URL:** your ngrok address + `/get_balance`
     (example: `https://abc123.ngrok-free.app/get_balance`)
3. Add a second tool the same way:
   - **Name:** `list_recent_transactions`
   - **Description:** `Lists the customer's most recent transactions. Use this when the caller asks about recent activity, charges, or a specific payment.`
   - **Method:** `GET`
   - **URL:** your ngrok address + `/list_transactions`
4. Save.

> **The #1 thing people get wrong:** the **description** is how the agent decides
> when to use the tool. Write it in plain, specific language. Vague descriptions =
> the agent never calls the tool.

---

## Step 7 — Watch it work

Click **Test AI agent** again and say: **"What's my balance?"**

- The agent should call your tool and answer with `$1240.55`.
- Look at your **second terminal** (ngrok) — you'll see the request hit it.
- Then ask: **"What were my last few transactions?"** and **"What's that GADGETS charge?"**

🎉 You now have an agent that takes a real action through an API. That's the core
of every enterprise deployment.

---

## Step 8 — Ground it with a knowledge base

1. In the agent settings, find **Knowledge base** → **Add document** → upload
   `northwind_fees_faq.md` from this folder.
2. Save, then test: ask **"What's your overdraft fee?"** It should answer **$29**
   *from the document* rather than inventing a number.

---

## Step 9 — Measure it (the part buyers care about)

1. In the agent settings, open the **Analysis** (or **Evaluation**) section.
2. Add an **evaluation criterion**:
   - **Name:** `solved_user_inquiry`
   - **Prompt:** `Return success if the agent correctly answered the caller's question or completed their request, otherwise failure.`
3. Now every call gets auto-graded success/failure with a reason. After a few test
   calls, open the call history and look at the scores. **Being able to show this
   is what closes enterprise deals.**

---

## Step 10 (optional flex) — Talk to it from your terminal

With your `.env` filled in and `pyaudio` installed:

```bash
python talk_to_agent.py
```

Speak out loud; press `Ctrl+C` to hang up. Now you've run the agent through the
**Python SDK**, not just the dashboard.

---

## Step 11 (optional flex) — Put it on a real phone

1. Get a free Twilio trial number.
2. In ElevenLabs, go to **Phone Numbers** → add your Twilio number using your
   Twilio **Account SID** and **Auth Token**.
3. Assign your agent to the number.
4. **Call the number** and talk to your agent over a real phone line.

---

## What you can now say in the interview

> "I built a Tier-1 bank support voice agent on ElevenLabs. I wired a webhook tool
> to a balance-lookup API and watched the agent call it mid-conversation, grounded
> its fee answers in a knowledge base, ran it over a Twilio phone number, and added
> an evaluation criterion so each call is scored on whether it resolved the query.
> The hardest part wasn't the model — it was the integration and making sure the
> tool descriptions were precise enough for the agent to call the right thing."

That answer demonstrates you've actually done the job. Most candidates only talk
about it in theory.

---

## Troubleshooting

- **Agent won't call the tool** → improve the tool **description**; make it specific
  about when to use it. Check the tool **Name** has no typos (names are case-sensitive).
- **Tool errors / "could not reach"** → is `uvicorn` still running? Did the ngrok
  address change after a restart? Update the tool URL.
- **`401 Unauthorized` in the Python script** → your API key in `.env` is wrong or missing.
- **`pyaudio` won't install** → skip Step 10 and use the dashboard's Test button instead.
- **Stuck** → the official quickstart mirrors these steps: search "ElevenLabs Agents quickstart".
```
