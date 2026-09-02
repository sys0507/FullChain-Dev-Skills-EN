# Cold-start heuristics

## When to read this

Read it when the user has given only a one-line idea and you need to generate a working
codename, a broad research assumption, or search keywords.

---

## 1. A working project codename

When the project's name is not settled, **generate a working codename**; do not require the
user to name it first.

**Generation rules**:

| Requirement | Note |
|---|---|
| Take words from the user's own phrasing | Do not introduce concepts the user never said |
| Neutral, implying no positioning | The codename MUST NOT imply a platform, an audience or a business model |
| Short and readable | Two or three words |
| **MUST be labelled "renameable"** | Written **outside** the ledger's "user confirmed" section |

**Examples**:

| The user said | Acceptable codename | Unacceptable | Why it fails |
|---|---|---|---|
| "a tool to help people manage reading notes" | `reading-notes-tool` | `ReadFlow Pro` | Invented wording, and "Pro" implies commercial tiering |
| "an assistant for watching the stock market" | `market-watch-assistant` | `StockWatch Web` | `Web` is an unconfirmed platform inference |
| "an internal team knowledge base" | `team-knowledge-base` | `KnowledgeHub SaaS` | `SaaS` is an unconfirmed delivery form |

**Where the codename goes in the ledger**: not in the "user confirmed" section (the user has
confirmed no such name). Put it at the top of the file as an identifier, annotated "working
codename, renameable".

---

## 2. A broad research assumption

When the project's positioning is not settled, write **one broad assumption** to bound this
round of searching.

**Three hard requirements**:

1. **It MUST carry its status**: "used only to bound this round of research; does not
   represent user confirmation"
2. **Err wide, not narrow**: too narrow misses an entire class of options, too wide only
   costs a few extra reads
3. **It MUST NOT introduce dimensions the user never mentioned**: no platform, no audience,
   no business model

**Example**:

> The user said: "I want to build a tool to help people manage reading notes"
>
> A good broad assumption:
> "A tool for **capturing, organising and revisiting text produced while reading**.
> The delivery form, the target users and the usage context are **all undetermined**, so this
> round of research must cover several possibilities.
> — Used only to bound this round of research; does not represent user confirmation."
>
> A bad narrow assumption:
> "A web application for managing reading notes, aimed at deep readers."
> — This invents two unconfirmed dimensions, audience and platform, and would make the search
> miss CLI tools, browser extensions and mobile applications entirely.

**Self-check**: circle every qualifier in the assumption and ask of each, "did the user say
this?" Any qualifier they did not say **MUST be deleted or marked as pending**.

---

## 3. Extracting search keywords

### 3.1 Iron rule: a placeholder is never a search term

Never search for `<PROJECT_NAME>`, `<TARGET_USERS>` or the working codename directly.

The working codename is **a word we invented** and will find nothing; a placeholder is just a
meaningless string.

### 3.2 The correct approach: neutral keywords from the user's own words

```
What the user said
   -> extract nouns and verbs, drop the modifiers
Core concept words (2-4)
   -> find one or two synonyms or broader terms for each
Search term combinations
   -> from wide to narrow
Record how it converged
```

**Example**:

| Step | Content |
|---|---|
| The user's words | "a tool to help people manage reading notes" |
| Core concepts | reading notes / manage / tool |
| Synonyms and broader terms | reading notes, excerpts, annotation, highlights, knowledge management |
| Wide to narrow | 1. `reading notes app` -> 2. `highlight management tool` -> 3. `book annotation organizer` |

### 3.3 Record how it converged

Searching does not land in one shot. **Keep the record of how it went from wide to narrow**,
because:

- Downstream can see which directions were already explored and avoid repeating them
- The convergence path is itself evidence — it explains why only these few product classes
  were examined in the end

Record it like this (in the research output, not in the ledger):

> The first pass searched `reading notes app` and returned mostly general note-taking
> applications with only a weak connection to reading; narrowing to `highlight management`
> raised the hit rate noticeably, so that term was used going forward.

---

## 4. Quick reference: how to start with unconfirmed variables

| Variable | What to do when it is unconfirmed |
|---|---|
| Project name | Generate a working codename, labelled renameable |
| Project positioning | Write a broad assumption, labelled as bounding the search only |
| Target users | **Do not lock it in.** Make "identify candidate audiences" a research task |
| Target platform | **Do not lock it in.** Make "candidate delivery forms" a research task |
| Core capabilities | **Do not lock it in.** Make "candidate capability sets" a research task |
| Key resources | Actively discover candidate constraints during research |
| Budget constraints | Record as pending; ask only when it is already affecting an irreversible decision |

**What they share**: **none of them blocks.** No missing variable should ever produce "come
back once you have filled this in".
