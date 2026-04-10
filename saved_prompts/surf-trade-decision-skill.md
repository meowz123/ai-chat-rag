# Surf Trade Decision Skill

Source: `.github/skills/surf-trade-decision/SKILL.md`

---
name: surf-trade-decision
description: "Use when: surf trading, T+2/T+3 trades, short-term VN stock analysis, entry/exit planning, intraday momentum checks, risk-reward setup, stop-loss and take-profit decisions, position sizing, trade checklist."
argument-hint: "Provide ticker(s), timeframe, risk per trade, and holding horizon (intraday/T+2/T+3)."
user-invocable: true
disable-model-invocation: false
---

# Surf Trade Decision Skill (Vietnam Stocks)

This skill creates a disciplined short-term trading decision process for Vietnam stocks (HOSE, HNX, UPCoM, VN30). It helps you decide whether to trade now, wait, or skip.

## When To Use
- You need a fast go/no-go decision for a ticker
- You want a T+2/T+3 setup with clear entry, stop-loss, and take-profit
- You need a consistent checklist to avoid emotional trades

## Inputs Required
- Ticker(s)
- Market context: VN-Index/HNX trend and session state
- Time horizon: intraday, T+2, or T+3
- Max risk per trade (for example: 0.5% to 1% of account)
- Preferred confirmation style: aggressive, balanced, conservative

## Default Profile
- Risk per trade: 1.0% of account
- Confirmation mode: Balanced
- Maximum holding horizon: T+2

If the user does not provide overrides, use this default profile automatically.

## Decision Workflow

### Step 1: Market Regime Gate
1. Check VN-Index and sector trend first.
2. Label regime as one of:
- Risk-On: broad market uptrend, healthy breadth
- Mixed: rotation/chop, selective opportunities
- Risk-Off: broad sell-off, weak breadth
3. Rule:
- Risk-Off => default action is WAIT unless there is exceptional relative strength.

### Step 2: Candidate Quality Filter
A ticker qualifies only if at least 3 of 5 conditions are true:
1. Price above MA20 (or reclaim with strong volume)
2. Relative strength versus VN-Index in the same session
3. Volume >= 1.5x recent average on breakout candle
4. Clear level structure (support/resistance not noisy)
5. No immediate high-risk event risk (major binary news unless event-trade is intended)

### Step 3: Setup Type Classification
Classify one setup:
1. Breakout continuation
2. Pullback to support (trend-follow)
3. Reversal from capitulation zone

If setup is unclear => SKIP.

### Step 4: Entry, Stop, Target Plan
Define exact levels before any decision:
1. Entry trigger (price + confirmation condition)
2. Stop-loss (technical invalidation, not arbitrary)
3. Take-profit levels (TP1/TP2)
4. Required risk-reward:
- Minimum RR >= 1:1.8
- Preferred RR >= 1:2.2

If RR below minimum => NO TRADE.

### Step 5: Position Sizing
1. Use fixed-risk sizing:
- Position size = Account risk amount / (Entry - Stop distance)
2. Never exceed pre-defined max position concentration.
3. If volatility is elevated, reduce size by 20%-40%.

### Step 6: Execution Rules
1. Enter only when trigger confirms (no anticipation entries).
2. If slippage invalidates RR threshold, cancel trade.
3. Move stop to breakeven only after structure confirms (for example after TP1 or higher-low formation).

### Step 7: Exit and Review
1. Exit immediately when invalidation condition hits.
2. Scale out at TP1, trail remainder by structure.
3. Log post-trade review:
- Did setup match checklist?
- Was execution disciplined?
- Was risk respected?

## Branching Logic
- If market = Risk-Off and ticker not exceptionally strong => WAIT
- If candidate score < 3/5 => SKIP
- If setup unclear => SKIP
- If RR < 1:1.8 => SKIP
- If all checks pass => EXECUTE with defined size

## Output Format
Return analysis in this exact structure:

1. Market Regime
- Current regime and why

2. Ticker Scorecard (0-5)
- Condition-by-condition pass/fail

3. Trade Plan
- Setup type
- Entry
- Stop-loss
- TP1 / TP2
- Estimated RR
- Position size guidance

4. Decision
- EXECUTE / WAIT / SKIP
- One-sentence rationale

5. Risk Notes
- Key failure trigger
- What would invalidate the thesis

## Quality Criteria (Completion Checks)
A response is complete only if all are present:
1. Regime label (Risk-On/Mixed/Risk-Off)
2. Scorecard with explicit pass/fail checks
3. Numeric entry/stop/target and RR
4. Final action (EXECUTE/WAIT/SKIP)
5. Invalidation condition

## Guardrails
- Do not fabricate market data; fetch first when live values are requested.
- Keep wording analytical, not legal financial advice.
- Prefer fewer high-quality setups over many weak ideas.
