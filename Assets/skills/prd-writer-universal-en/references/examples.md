# PRD Examples (Cross-Domain)

> This file contains PRD excerpt examples across 3 different domains, showing how the 14-chapter structure is applied to different product types.
> Each example only highlights how key chapters differ — see `14-chapters-detailed.md` for the full chapter templates and anti-pattern rules.

---

## Example A: SaaS Tool Product (Team Async Collaboration)

**Project**: Async video/voice messaging tool for remote teams (Loom-style), targeting distributed software teams
**Applicable PRD version**: Full 14 chapters

---

### A · Chapter 2: Project Background & Goals

#### 2.1 Background

Remote and hybrid work has become the norm, but existing tools are polarized: synchronous meetings (Zoom, Teams calls) interrupt flow and consume everyone's time; async text messaging (Slack, email) loses semantic fidelity when explaining technical problems, causing long back-and-forth clarification loops.

Distributed software teams face frequent "not worth a meeting, but too nuanced for text" communication scenarios: code review feedback, feature demos, bug repro recordings, technical design walkthroughs. The current workflow is: screen-record → upload to cloud storage → share link → recipient downloads / waits for buffering → replies in text. The process is fragmented and inefficient.

We are building a lightweight async video/voice messaging tool that transforms the above workflow from a "5-step fragmented process" into "1-click record + instant link + play immediately," with timeline comments so async feedback feels as natural as real-time conversation.

#### 2.2 Goals

- **Business goal**: Reach 500 paying teams (5+ members each) within 6 months of launch; monthly MRR ≥ $30,000
- **Product goal**: Users complete a full "record → share → receive first comment" loop in ≤ 3 minutes
- **Learning goal**: Validate the hypothesis that "software teams will pay to reduce meeting frequency"

#### 2.3 Non-Goals

- No real-time video conferencing — that is Zoom's positioning, we don't compete there
- No livestreaming / webinar — deferred to v3.0
- No mobile recording — v1.0 is Chrome extension + Desktop App only

#### 2.4 Strategic Alignment

Aligned with company 2026 strategy: enter via individual productivity tooling, expand toward team collaboration

---

### A · Chapter 3: Target Users & Personas

#### 3.1 Primary Persona P1: Remote Software Engineer "Alex"

- **Background**: 28 years old, full-stack engineer, team spans 3 time zones, primarily WFH
- **Goal**: Explain technical problems clearly without interrupting teammates' workflows
- **Pain points**:
  1. Screen recording tools and communication tools are separate — every recording requires manual upload + link sharing
  2. Text-only PR comments lack context — unclear which line or scenario the reviewer is referring to
  3. A 5-minute verbal explanation takes 30 minutes to write in text
  4. Large video files buffer slowly for colleagues in remote locations
- **Usage frequency**: 2–5 times per day
- **Devices**: MacBook Pro / Windows laptop, Chrome browser
- **Willingness to pay**: $8 / person / month for a team plan

#### 3.2 Secondary Persona P2: Engineering Team Lead "Sam"

- **Background**: 35 years old, Tech Lead managing an 8-person distributed team
- **Goal**: Reduce unnecessary meetings; make async communication traceable and accountable
- **Pain points**: Team communication scattered across multiple platforms; code review comments lack context; new hire onboarding relies on tribal knowledge
- **Usage frequency**: 3–8 times per day (including reviewing others' recordings)
- **Devices**: Multiple devices (PC + mobile for viewing)
- **Willingness to pay**: As a purchasing decision-maker, focused on team-wide efficiency ROI

#### 3.3 Anti-Personas (explicitly not served)

- **Sales / customer-support teams that require real-time interaction**: Their core scenario is live demos and instant answers — async video doesn't satisfy that need
- **Individual vloggers / content creators**: They need professional editing features — not our direction
- **Large enterprise compliance departments**: They have strict requirements on video storage location; v1.0 does not support on-premises deployment

---

### A · Chapter 5: Feature Scope

#### 5.1 In-Scope (MVP v1.0 must-haves)

| ID | Feature | One-line description | User stories | Priority |
|---|---|---|---|:--:|
| F1 | One-click record | Camera / screen / combined, click to record | US-01, US-02 | P0 |
| F2 | Instant share link | Auto-upload after recording; generate a directly playable link | US-01 | P0 |
| F3 | Timeline comments | Viewers can leave comments at any timestamp on the video | US-03 | P0 |
| F4 | Workspace management | Shared team recording library, organized by project / channel | US-04 | P1 |
| F5 | View status tracking | Sender can see who watched and how far they got | US-05 | P1 |

#### 5.2 Out-of-Scope (v1.0 exclusions)

- ❌ Video editing — deferred to v1.1 (validate core scenario first)
- ❌ AI auto-captions / summarization — deferred to v2.0 (high cost; reach PMF first)
- ❌ Mobile recording — not planned (engineer scenarios are desktop-primary)
- ❌ On-premises deployment — not planned (v1.0 is SaaS-first)
- ❌ Deep integration with Jira / GitHub Issues — deferred to v1.1

---

### A · Chapter 7: Non-Functional Requirements

- **Performance**: Video playable within ≤ 30 seconds of upload completion (720p, 5-minute video); first frame render ≤ 2 seconds
- **Availability**: Monthly uptime ≥ 99.5%; automatic local draft save if recording is interrupted
- **Security**: Video links default to workspace-member-only access; configurable link expiry (7 days / permanent); TLS encryption throughout
- **Compliance**: GDPR-compliant (EU user right to erasure); user choice of storage region (EU / US)
- **Data**: Videos permanently deleted from storage within 30 days of user deletion request; not used for ad targeting or model training

---

### A · Chapter 9: Acceptance Criteria

```
### AC-F1-01: Recording starts successfully
Given  User has installed the Chrome extension and granted camera/screen permissions
When   User clicks the extension icon → selects "Screen + Camera" → clicks "Start Recording"
Then   Recording indicator lights up within 3 seconds; recording timer appears in the lower-right corner of the screen

### AC-F2-01: Shareable link ready after recording ends
Given  User has completed a recording of ≤ 10 minutes
When   User clicks "Stop Recording"
Then   Within 30 seconds, the link is auto-copied to clipboard and a "Link ready" toast appears;
       clicking the link opens the video directly in the browser (no download required)

### AC-F3-01: Timeline comment positioned accurately
Given  A viewer is watching a video
When   The viewer clicks "Comment" at timestamp 2:34 and submits a text comment
Then   The comment appears at the 2:34 position on the timeline;
       the sender and all members with access can see it;
       clicking the comment jumps the video playback to 2:34

### AC-NFR-01: Concurrent performance acceptance
Given  1,000 users simultaneously streaming videos
When   Users request playback of any video
Then   p95 first-frame load time < 2 seconds; p99 < 5 seconds
```

---

### A · Chapter 13: Risks & Open Questions

#### 13.1 Risk Register

| ID | Risk | Severity | Probability | Mitigation |
|---|---|:--:|:--:|---|
| R-01 | Video storage costs scale linearly with usage, exceeding projections | High | Medium | Set free-tier storage cap (25 GB / team); charge for overage |
| R-02 | Recording permissions (camera/screen) blocked by enterprise IT policy on corporate devices | Medium | Medium | Provide "screen-only" fallback mode; publish enterprise IT allowlist configuration guide |
| R-03 | Competitor (Loom) reduces pricing or opens more free features, intensifying competition | High | Medium | Differentiate on engineer-specific features (code highlighting, PR integration); monitor competitor moves |

#### 13.2 Open Questions

- [ ] OQ-01: Free tier — unlimited recordings with storage cap, or per-recording duration limit (≤5 min)? @PM decision — affects paid conversion strategy
- [ ] OQ-02: Should timeline comments support emoji reactions (like GitHub reactions)? @Design — estimate effort
- [ ] OQ-03: Enterprise pricing: per-seat or per-storage? @Business team — decision deadline: 2026-07-01
- [ ] OQ-04: What is the SLA for handling GDPR data deletion requests? @Legal to confirm

---

## Example B: Consumer App (Personal Health Tracking)

**Project**: Personal sleep quality tracking and improvement recommendations app, for health-conscious professionals
**Applicable PRD version**: Condensed 9 chapters (consumer app — drop #8 UI spec, #12 dependencies/constraints, #14 milestones; keep the rest)

---

### B · Chapter 2: Project Background & Goals

#### 2.1 Background

Sleep problems among urban professionals are worsening: average bedtime has shifted past midnight, and over 60% get fewer than 7 hours of sleep (source: Sleep Research Society 2024 report). Users know their sleep is poor, but they don't know specifically what's wrong or how to fix it.

Existing solutions fall into two categories: smart wearables (e.g., Apple Watch, Fitbit) provide sleep stage data, but with limited analytical dimensions and almost no actionable improvement guidance; manual journal apps (e.g., sleep diaries) depend on user discipline and have low long-term retention. Neither category closes the "data → insight → action" loop.

We are building a lightweight sleep tracking app that passively collects overnight data via the phone's microphone and accelerometer, overlays user-entered lifestyle factors (caffeine intake, exercise, screen time), and uses AI to generate personalized improvement recommendations — helping users experience a measurable improvement in sleep quality within 4 weeks.

#### 2.2 Goals

- **Product goal**: After 4 consecutive weeks of use, users' self-reported sleep quality score improves by ≥ 1 point (on a 5-point scale)
- **Business goal**: MAU ≥ 10,000 within 3 months of launch; paid conversion rate ≥ 8%
- **Learning goal**: Validate the hypothesis that "users will consistently log lifestyle habits in exchange for personalized sleep recommendations"

#### 2.3 Non-Goals

- No medical diagnosis or treatment advice — this is a regulatory red line; we provide "wellness reference" only
- No dependency on wearables — v1.0 is phone-only; wearable integration is v2.0
- No social / leaderboard features — sleep is private data; avoid social pressure dynamics

---

### B · Chapter 3: Target Users & Personas

#### 3.1 Primary Persona P1: Overworked Knowledge Worker "Jordan"

- **Background**: 29 years old, product manager at a tech company, high work stress, difficulty falling asleep
- **Goal**: Understand which habits are hurting sleep; find actionable improvement steps
- **Pain points**:
  1. Knows sleep is poor but can't identify the root cause (caffeine? phone? stress?)
  2. Generic sleep advice online — doesn't know which tips apply personally
  3. Bought a smartwatch, but the app only says "1.5 hrs deep sleep" — no idea if that's good or how to improve
  4. Health-tracking apps get abandoned after a few days
- **Usage frequency**: Checks previous night's data every morning; reviews weekly trend report
- **Devices**: iPhone 14 (primary); has Apple Watch but doesn't rely on it
- **Willingness to pay**: Annual subscription of ~$20/year (≤ $2/month)

#### 3.2 Secondary Persona P2: New Parent "Morgan"

- **Background**: 34 years old, infant at home, severely fragmented sleep, wants to know how much effective sleep is actually happening
- **Goal**: Quantify sleep fragmentation; find ways to maximize sleep quality within the infant's schedule
- **Special needs**: Doesn't want too many notifications; needs silent mode so alerts don't wake the baby

#### 3.3 Anti-Personas (explicitly not served)

- **Users with sleep disorders (insomnia / sleep apnea) who need medical care**: Require professional medical intervention; our app is not a substitute and carries medical-legal risk
- **Users over 60**: Different usage habits and sleep problem etiologies; not optimizing for this group in v1.0
- **Users seeking clinical-grade precision data**: Need PSG-level accuracy; phone microphone approach does not meet that bar

---

### B · Chapter 4: User Stories

```
### US-01 Quickly log today's lifestyle factors before sleep
As    a professional concerned about sleep quality
I want to log today's caffeine intake, exercise duration, and screen-off time in under 1 minute at bedtime
So that  the app can correlate these factors with my sleep quality

Trigger context: 10:00–11:00 PM, user is preparing for bed
Expected outcome: log is complete; app enters "monitoring" state; user can put the phone down

### US-02 Check last night's sleep report after waking up
As    a user who wants to understand their sleep
I want to see last night's key sleep data and one targeted recommendation within 30 seconds of picking up my phone
So that  I know how well I slept and what habit to adjust today

Trigger context: 6:00–8:00 AM, user picks up phone
Expected outcome: sees sleep score, inferred primary cause of issues, one actionable improvement tip for today

### US-03 View 4-week trend analysis
As    a user who has continuously used the app for 4+ weeks
I want to see how my sleep quality has trended over time and which habits correlate most strongly with my sleep
So that  I can confirm the app is helping me and know what to focus on improving next
```

---

### B · Chapter 5: Feature Scope

#### 5.1 In-Scope (MVP v1.0 must-haves)

| ID | Feature | One-line description | User stories | Priority |
|---|---|---|---|:--:|
| F1 | Pre-sleep quick log | Record 5 lifestyle factors in ≤ 30 seconds | US-01 | P0 |
| F2 | Passive overnight monitoring | Microphone captures sound events + accelerometer detects movement | US-01 | P0 |
| F3 | Morning sleep report | Sleep score + stage durations + 1 personalized recommendation | US-02 | P0 |
| F4 | 4-week trend analysis | Habit-sleep correlation chart + progress comparison | US-03 | P1 |
| F5 | Smart alarm | Wake during light sleep phase to avoid deep-sleep interruption | US-02 | P1 |

#### 5.2 Out-of-Scope (v1.0 exclusions)

- ❌ Wearable integration (Apple Watch, Fitbit) — deferred to v2.0
- ❌ Social / friend comparison features — not planned (privacy-sensitive)
- ❌ Meditation / sleep audio content — deferred to v1.1 (validate data collection value first)
- ❌ Doctor / expert consultation portal — deferred to v2.0 (requires regulatory compliance)

---

### B · Chapter 11: Metrics

#### 11.1 North Star Metric

**7-day consecutive usage rate** (measures genuine habit formation, not just install-and-forget)

#### 11.2 Key Metrics

**Activation**
- % of users who complete their first pre-sleep log after install ≥ 60%
- % of users who use the app on ≥ 2 consecutive nights within 3 days of signup ≥ 40%

**Retention**
- D7 retention ≥ 40%
- D30 retention ≥ 20%
- 7-day consecutive usage rate (core North Star) ≥ 25%

**Revenue**
- Paid conversion rate among users with ≥ 14 days of usage ≥ 12%
- Annual subscription renewal rate ≥ 70%

#### 11.3 Counter-Metrics (guard against "gaming the metric")

- High open rate but low log completion rate (users open and immediately close): log completion rate must be ≥ 80% to count as a valid DAU
- Alarm feature usage rate vs. report view rate: report view rate should be ≥ alarm usage rate (guard against users only using the alarm, never reading the insights)

---

### B · Chapter 13: Risks & Open Questions

#### 13.1 Risk Register

| ID | Risk | Severity | Probability | Mitigation |
|---|---|:--:|:--:|---|
| R-01 | Phone microphone accuracy insufficient, leading to poor data quality and incorrect recommendations | High | Medium | Clearly label all data as "reference only, not medical grade"; establish beta feedback loop for data quality |
| R-02 | AI recommendations cross the "medical advice" regulatory line, triggering compliance risk | High | Low | Prepend all recommendations with "For wellness reference only — consult a doctor for sleep disorders"; legal review of all recommendation templates |
| R-03 | Always-on overnight microphone triggers user privacy concerns, increasing uninstall rate | Medium | High | Privacy disclosure as first onboarding step; all audio processed on-device, raw audio never uploaded; only extracted feature vectors are transmitted |
| R-04 | Android fragmentation causes background process termination, interrupting monitoring | Medium | High | Provide per-brand "battery whitelist" setup guides; log monitoring interruption events and prompt users |

#### 13.2 Open Questions

- [ ] OQ-01: Who reviews and approves the AI recommendation template library? Is an external sleep specialist consultant needed? @Founder decision
- [ ] OQ-02: Do recent OS background audio permission changes affect the feasibility of the overnight monitoring approach? @iOS/Android engineers to confirm
- [ ] OQ-03: User data storage — local device or cloud sync? Local: better privacy but data lost on phone change; cloud: better experience but raises privacy concerns. @PM decision
- [ ] OQ-04: Will the free tier show ads? If so, does advertising conflict with the health / wellness brand positioning? @Monetization discussion

---

---

Example C (B2B internal tool) and the comparison across all three are in `references/examples-b2b.md`.
