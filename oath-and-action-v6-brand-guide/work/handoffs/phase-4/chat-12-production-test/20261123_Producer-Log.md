# The simulated producer's log (chat 12, production reader)

A staffer at a partner organization who builds one web page a month, working only from chapters 16, 20 and 21, chapter 18 and the kit's own file headers. Every step, every place looked and every guess is logged here, in order. Simulated; no real producer was tested.

## Task 1: a new atlas reform page from chapter 21 alone

### The selection rule, written at 17:15 UTC, before looking at any reform

1. Read the four views' domains from chapter 21's words alone (the home question, Reform R-23, the Register's sheet D04, Loop R18 with Reform R-11).
2. List every reform in the atlas model in ID order (R-01, R-02, ...).
3. Take the first reform whose domain is none of the domains found in step 1. Do not read any reform's title, summary or remedy before taking it. Do not skip a reform for its subject, its side or its grade (DR-55 as DR-94 restates it; DR-93: no counterweight, no choice made to even a score).
4. If chapter 21 does not say what a reform's domain is, or how to find it, log that as a gap and use the model's own field for a reform's domain.

### Applying the rule (17:17 UTC)

- Step 1 from chapter 21's words: the views are the atlas home (the question "Why can the same care produce different bills?"), Reform R-23, the Register with sheet D04 open, and Loop R18 with Reform R-11 chosen. Chapter 21 names the domains only in Rule 21.8 ("Domains D01 to D10"), and gives no way to find a reform's domain. **Gap 1:** chapter 21 never says which domain a reform belongs to; a reform has targets, and Rule 21.9 files a target's connection "by the variable the connection moves; ... one with two domains on the first". **Guess 1:** a reform's domains are the first domains of its targets' variables (a connection target counts by the variable it moves), read from the model, `work/extract/atlas-v7-data.json`.
- Domains the four views show, read from the model with that guess: the home question (pathway PW06's variables) reaches D04, D05, D06, D08, D09, D10 and the economy layer; Reform R-23 acts in the economy layer and D08; the Register shows D04; Loop R18 runs through D04 and D05, and Reform R-11 targets D04 and D05. Shown: D04, D05, D06, D08, D09, D10 and the economy layer. Not shown: D01, D02, D03, D07 and the technology layer.
- Step 2 and 3: in ID order, Reform R-01's targets all file on D02. **Chosen: Reform R-01**, taken by the rule before reading its title, summary or grades. (DR-223: R-01 is handled like every other reform.)
