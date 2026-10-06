# EP062 Strategy Directory — Five-Video Script Series

**Version:** 1.0.0 · 2026-10-06  
**Status:** Script draft for the approved questions; narration and video have not been generated.  
**Audience:** People selecting among strategies that have already been defined and are in action.  
**Narrator:** Thomas — Microsoft Azure English (UK) male Neural voice, `en-GB-ThomasNeural`, matching the earlier sample. Delivery: natural, warm, lower register, measured pace, conversational emphasis; avoid flat, over-polished reading.

## Production and evidence guardrails

- The central story is a decision among established strategies—not market analysis, strategy creation, or prediction.
- The live-directory workflow described by the user ranks strategies continuously. Users can define a comparison group using criteria or add strategies to a portfolio, then compare within that chosen set. Treat ranking as order and criteria/portfolio as membership; do not conflate the two.
- The standalone Hermes explorer is a frozen historical copy, with Crypto and Forex data as of 2026-10-05 16:14. It is not a live feed, does not execute trades, and should not be shown as if its rankings update continuously. It has a six-closed-position eligibility floor and a historical switch-versus-hold replay.
- Before final screen recording, verify the live directory’s actual labels and behavior for continuous ranking, criteria-based groups, and portfolios. Use those real controls in Video 2; do not invent buttons, thresholds, or states.
- “Top-ranked” means top under the selected ranking rule and comparison set at that decision point. It does not mean universally best or necessarily positive net. A rank is not a positive-return filter. Positive net return and a 100% win-rate threshold are different criteria; state the exact one being used.
- Historical and replayed performance must be labeled with its data period and calculation context. Past performance cannot predict how an investment strategy will perform in the future. See the SEC’s Investor Bulletin on performance claims: https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-47.
- Do not claim improved returns, a proven edge, guaranteed profitability, or live switching. The replay assumes switching is free.
- Audio-generation note: this file specifies the previously used Thomas voice, but no TTS request has been made. Check and disclose any metered voice/rendering cost before generating audio.

---

# Video 1 — Why use a strategy directory?

**Approved viewer question:** How does the directory help reduce analysis paralysis?  
**Purpose:** Explain that the decision is which existing strategy to select at a decision point—not what the market will do or which new strategy to invent.  
**Visual source:** Live strategy directory for active rankings. Do not use the frozen explorer to imply live operation.

### Narration — Thomas

**Opening**  
“Imagine that a number of strategies have already been designed and put into action. The question is not, ‘What will the market do next?’ The strategies already exist. The practical question is simpler: at this decision point, which of the competing strategies should I choose?”

**Context**  
“That is where a directory can help. When many strategies are available, their results can be difficult to compare consistently. One screen may emphasise one measure, another may use a different period, and it can become hard to remember why one strategy was preferred over another.

“Here, analysis paralysis is really choice overload. The user is not being asked to conduct market analysis or build a new strategy. They are making a deliberate selection from strategies that are already in action.”

**How the directory supports the decision**  
“The directory keeps the comparison organised. Strategies can be ranked using a stated measure, and the user can decide which candidates belong in the comparison. At the decision point, they can review the alternatives and select the strategy that performs best under the chosen rule.

“‘Best’ needs a clear meaning. Best by net result may not be best by win rate, and a strategy that ranks first within one group may rank differently in another. The directory makes the choice more structured; it does not turn one ranking into a universal answer.”

**Close**  
“The aim is not to remove judgement. It is to make one specific decision easier to see, compare, and explain.”

### Visual direction and on-screen text

- Open on several named, already-established strategy cards or rows; show that they are existing candidates, not newly generated strategies.
- Cut to the directory’s current ranking and highlight the selected ranking label.
- Show the user selecting or reviewing the comparison set, then making a single selection.
- Avoid market charts, forecasts, or strategy-generation visuals; they would imply a different task.
- On-screen: **“One decision at a time”**, **“Compare existing strategies”**, **“Best under the selected rule—not a guarantee”**.

### Evidence note

The live directory’s current-state display and selection action must be captured from the actual live interface. Any performance shown must carry its period and selected metric.

---

# Video 2 — How do I set up a strategy comparison?

**Approved viewer question:** How do I set up a strategy comparison?  
**Purpose:** Explain the two user-described routes to a comparison set, then show ranking as a separate ordering step.  
**Visual source:** Actual live directory, after verifying the controls. The static explorer cannot demonstrate continuous ranking or portfolio construction.

### Narration — Thomas

**Opening**  
“Before comparing results, decide which strategies belong in the comparison. That is the first important choice: define the set, then compare within it.”

**Continuous ranking**  
“The directory ranks strategies continuously according to the stated ranking rule. A ranking answers, ‘How are these strategies ordered right now under this measure?’ It does not, by itself, answer, ‘Which strategies are allowed into my comparison?’ Those are related, but different questions.”

**Route one: criteria-defined group**  
“One option is to define a group using specific criteria. The criteria create the group of candidates; the ranking then orders that group. This is useful when you want to compare strategies that share a relevant context rather than mixing every available strategy together.

“Be precise about the criteria. A product or category condition defines membership. A ranking measure orders the members. If the intention is to include only strategies above a performance threshold, show that threshold explicitly and confirm that the directory really applies it.”

**Route two: portfolio**  
“Another option is to build a portfolio by adding the strategies you want to compare. The portfolio becomes the comparison set. You can then examine how its members rank or perform relative to one another, without losing sight of the exact strategies you chose to include.”

**Put the steps together**  
“So the workflow is: choose the comparison set—by criteria or by portfolio—then read the continuous ranking within that set. This makes the decision easier to reproduce: another person can see both which strategies were considered and how they were ordered.”

**Close**  
“Set first. Rank second. Compare like with like.”

### Visual direction and on-screen text

- Show the live ranking updating or refreshing, but only if that behavior is verified in the current build.
- Demonstrate the criteria-defined group path; use the real field names and actual resulting group size.
- Demonstrate the portfolio path by adding strategies and opening the portfolio comparison.
- Show the comparison set remaining visible while the ranking is read.
- On-screen: **“Criteria or portfolio = comparison set”**; **“Ranking = order within the set”**.
- If a positive-return criterion is available, show its actual control and state its definition. Do not treat “Top Net” or “Top Win Rate” as equivalent to a minimum threshold.

### Evidence note

The user described continuous ranking, criteria-defined groups, and portfolio comparison. Capture those actual states before final recording. The frozen HTML explorer is not evidence of those live functions.

---

# Video 3 — How should I interpret the results?

**Approved viewer question:** How should I read a candidate’s historical metrics and similar strategies?  
**Purpose:** Explain what the visible measures say, what they do not say, and how the static explorer marks below-threshold references.

### Narration — Thomas

“Once the comparison set is clear, the next step is to understand what each result means. A ranking only makes sense when you know the measure behind it.

“Net result and win rate answer different questions. Net describes the combined result under the app’s calculation. Win rate describes the share of closed positions recorded as wins. A high win rate does not tell you the size of losses, and a positive net result does not require every position to have won. Check the period and the way each measure is calculated before comparing two strategies.

“Also look at the number of closed positions. In the static explorer, six closed positions is the minimum eligibility floor for selection. It is a rule for inclusion, not proof that the strategy is statistically reliable or will remain profitable.

“The explorer may show similar strategies that fall below that floor. Those rows are marked reference-only. They can provide context, but they are not eligible as the selected strategy or as a switch target under the six-position rule.

“Finally, keep the decision time in view. The historical explorer uses the last available snapshot at or before the chosen time. Later observations are not used to make that original selection.”

### Visual direction and on-screen text

- Zoom in on net, win rate, closed-position count, and the selected ranking label.
- Expand the app’s explanation of the measures and six-position floor.
- Highlight a below-six Similar row with its **REFERENCE ONLY** label; contrast it with an eligible candidate.
- Show the selected decision time and the snapshot used at or before it.
- On-screen: **“Net ≠ win rate”**, **“Six positions = eligibility floor”**, **“Reference-only rows are not switch targets”**.

### Evidence note

The frozen explorer data is as of 2026-10-05 16:14 for Crypto and Forex. State that date and time whenever using its results. Do not select a single positive result without showing its criteria and context.

---

# Video 4 — How do I compare switching with holding?

**Approved viewer question:** How can I compare switching with holding?  
**Purpose:** Explain the historical replay while keeping decision-time evidence separate from later observations.

### Narration — Thomas

“At a decision point, there are two paths to compare. One is to keep holding the strategy already selected. The other is to follow the stated rule and switch to the alternative chosen from the comparison.

“The historical explorer lets you look back at what happened along those paths. The important distinction is timing. Information available at the decision point supports the original choice. What happened afterwards belongs to the replay: it helps us examine the outcome, but it must not be fed back into the historical decision as though it had been known at the time.

“There is also an assumption to keep in mind. This replay treats switching as free. It does not include a live execution step, and the result does not prove that the switching rule has an edge. It shows a historical comparison under the app’s stated setup.

“Think of it as a way to inspect a decision process—not as a forecast of what will happen next.”

### Visual direction and on-screen text

- Show the selected strategy and alternative at a marked decision point.
- Draw a clear visual boundary between **“At decision time”** and **“After the decision: historical replay”**.
- Display the hold and switch paths; do not imply the app places orders.
- On-screen: **“Switching assumed free”**, **“Replay is not a forecast”**, **“Historical comparison—not proof of an edge”**.

### Evidence note

Use only the app’s actual replay outputs. Do not describe the replay as live switching, a guarantee, or evidence of improved returns.

---

# Video 5 — How do we know whether the directory adds value?

**Approved viewer question:** How do we measure the app’s value versus doing this manually?  
**Purpose:** Show how to evaluate the workflow benefit without claiming trading-performance gains.

### Narration — Thomas

“The directory is intended to improve the way a comparison is made—not to promise that a selected strategy will earn more.

“To test whether it adds practical value, compare the same decision task with and without the directory. Give people the same candidate strategies, the same data period, and the same decision rule. In one run, let them work manually. In another, let them use the directory.

“Then measure the process. How long did it take to define the comparison set? Did different users apply the same criteria? Could someone else reproduce the selected group and explain why one strategy ranked above another? How often were eligibility rules missed? Was the final decision easier to trace?

“These measures can tell us whether the directory makes the process more consistent, traceable, or efficient. They do not establish that it improves trading returns. That would require separate, carefully designed evidence and should never be inferred from a smoother interface or a historical replay.

“The value proposition is a clearer decision process: see the candidates, understand the rule, compare the set, and record the choice.”

### Visual direction and on-screen text

- Split screen: manual workflow versus directory-assisted workflow, using the same candidate set and rules.
- Show a simple test log: time to define the set, criteria consistency, reproducibility, eligibility errors, and traceability.
- Avoid fabricated before-and-after numbers; use real study results only after a measured evaluation.
- On-screen: **“Measure process value”**, **“Do not infer better returns”**.
- Optional end card: “Explore the directory” and, if desired, the existing Arena waitlist CTA. Do not imply that joining guarantees live access.

### Evidence note

The current app has not demonstrated measured time savings, fewer errors, or improved returns. Present these as outcomes to test, not achieved results.

---

## Series-wide final checks before recording

1. Confirm every control shown exists in the exact build being recorded; use live-directory footage for continuous rankings, criteria groups, and portfolios.
2. Label historical material with its data period. The Hermes explorer is a frozen history copy, not a live directory.
3. Keep ranking order, comparison-set membership, and threshold filtering conceptually separate.
4. Keep net return, win rate, and closed-position count separate; disclose the exact criterion used.
5. Preserve the boundary between information available at selection time and later replay outcomes.
6. Keep the free-switch assumption and the lack of live execution clear in the replay video.
7. Do not claim guaranteed profit, improved returns, or a proven trading edge.
8. No narration or video has been generated from this script. Before using metered TTS or rendering, disclose potential cost and obtain approval.
