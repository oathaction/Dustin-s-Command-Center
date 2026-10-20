# How to run the V6 prompt pack in Claude Code

This pack commissions Edition 06 of the Oath & Action brand guide. It runs in six phases. Each phase stops at a gate so you can review the work before anything changes.

## What is in the pack

```
oath-and-action-v6-brand-guide-prompt/
  20261020_How-To-Run-The-V6-Prompt-Pack.md        this guide
  20261020_Oath-And-Action-V6-Prompt-Revision-Notes.md   what changed from your draft prompt, and why
  project-kit/                                     copy this whole folder to start the project
    CLAUDE.md                                      operating rules Claude Code loads every session
    .claude/agents/                                seven studio agents
    brief/20261020_Oath-And-Action-V6-Master-Brief_V1.md
    brief/20261020_Research-Verification-Ledger.md   award and reference checks the research agent starts from
    brief/phase-prompts/                           six prompts, Phase 0 to Phase 5
    source/icon-studies/                           three icon study sheets you pasted in chat
```

`CLAUDE.md` and the agent files keep the names Claude Code requires, so they sit outside the date-prefix convention.

## Set up once

1. Make a project folder under your Cowork folder, for example `oath-and-action-v6-brand-guide/`.
2. Copy everything inside `project-kit/` into it, including the hidden `.claude` folder.
3. Put these files into `source/` with these exact names:
   - `20261018_Oath-And-Action-Brand-Guide_V5-Polished.html`
   - `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html`
   - `20261018_Oath-And-Action-Atlas-Visual-System.html`
   - `20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html`
   - `20261019_Oath-And-Action-Atlas-Design-Concepts_V1.html`
   - `20261018_Oath-And-Action-Brand-Guide_V5.html`
   - `20261018_Oath-And-Action-Brand-Guide_V4.2.html`
   - `data_viz.zip`
   - `Design_I_like.zip`

   The `source/icon-studies/` folder is already filled.
4. Open a terminal in the project folder and run `claude`.
5. Type `/agents` and confirm you see the seven agents whose names start with `oa-`.

The builder will ask permission to install test tools (Playwright, axe-core and an SVG or PNG tool) and to search the web. Approve those. If you have Canva, Figma or Adobe connected in Claude Code, the builder can use them for image generation. Without one, it writes the image prompts and leaves labeled placeholders.

## Run each phase

1. Start a fresh session for each phase. The ledgers in `work/ledger/` carry everything forward.
2. Open the phase prompt in `brief/phase-prompts/`, copy everything below its line, and paste it in.
3. For Phases 1 to 5, fill in the "Gate decisions" line with what you approved or changed at the previous gate.
4. The builder stops at the gate. Open the gate report in `work/ledger/` and the board it names in `work/boards/`.
5. Reply with "Approved," or with the changes you want. The builder revises and asks again when your changes are substantial.

Phases 3 and 4 are the heaviest. A phase that runs long can continue in a new session. Tell it to read the ledgers and pick up where it stopped.

## What to look for at each gate

| Gate | Check before you approve |
|---|---|
| 0 Review and plan | The review names the right strengths and problems. The reconciliation table shows how the guide matches Atlas V7. The plan shows what you will see at each gate. Your open questions are answerable. |
| 1 Direction | The strategy sounds like Oath & Action. You like one of the two pillar-mark directions. Accept or decline each identity refinement one at a time. Every V5 chapter has a home in the architecture map. |
| 2 Foundations and symbols | The marks look right at 16 px. Similar icons are easy to tell apart. Small text is readable. The loading and disabled states make sense to you. |
| 3 Data and systems | You can read each worked example without help. R1's weakest step is obvious. Reform R-01 shows no total score. Every statistic shows a source and period. |
| 4 Applications | Each application looks finished at real size. The email works with images off. Illustrative labels sit beside the realistic quotes and figures. |
| 5 Final | Every download opens. The validation report lists what was tested and what was not. The open questions are ones you can resolve. |

## If something goes wrong

- If the builder starts a later phase without your approval, stop it and point it to the gate rules in `CLAUDE.md`.
- If it reads a large HTML file whole and runs out of context, tell it to use the extraction scripts in `work/extract/`.
- If a download or test fails at the end, the validation report should say so plainly. Ask for the fix before you accept.
