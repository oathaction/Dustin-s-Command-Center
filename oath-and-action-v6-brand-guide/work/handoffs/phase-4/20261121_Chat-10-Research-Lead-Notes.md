# Chat 10, research lead notes

Research lead, Phase 4, chat 10, November 21, 2026. Brief: `work/handoffs/phase-4/20261121_Chat-10-Brief.md`, section 5. Every page below was read on November 21, 2026 (UTC) unless a row says otherwise. "Read" means the page's own text was downloaded from the official domain and read in full. "Search-result" means the official page refused an automated reader or draws its text by script, so the fact comes from what a search showed for that official address. "Not-found" means no official page gave the fact.

## Facts for chapter 16

Written between 01:36 and 01:41 UTC. The creative director plans from this section.

### A. WCAG 2.2's media criteria, quoted from the W3C

Source: Web Content Accessibility Guidelines (WCAG) 2.2, "W3C Recommendation 12 December 2024", https://www.w3.org/TR/WCAG22/. Read November 21, 2026 (the whole page downloaded and the five criteria taken from their own sections). Status: read.

| Number | Name | Level | Exact text |
|---|---|---|---|
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | "For prerecorded audio-only and prerecorded video-only media, the following are true, except when the audio or video is a media alternative for text and is clearly labeled as such: Prerecorded Audio-only: An alternative for time-based media is provided that presents equivalent information for prerecorded audio-only content. Prerecorded Video-only: Either an alternative for time-based media or an audio track is provided that presents equivalent information for prerecorded video-only content." |
| 1.2.2 | Captions (Prerecorded) | A | "Captions are provided for all prerecorded audio content in synchronized media, except when the media is a media alternative for text and is clearly labeled as such." |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | "An alternative for time-based media or audio description of the prerecorded video content is provided for synchronized media, except when the media is a media alternative for text and is clearly labeled as such." |
| 1.2.4 | Captions (Live) | AA | "Captions are provided for all live audio content in synchronized media." |
| 1.2.5 | Audio Description (Prerecorded) | AA | "Audio description is provided for all prerecorded video content in synchronized media." |

Terms from the same page, quoted, for the chapter's first use of each word:

- Captions: "synchronized visual and/or text alternative for both speech and non-speech audio information needed to understand the media content". Its notes: "Closed Captions are equivalents that can be turned on and off with some players." "Open Captions are any captions that cannot be turned off. For example, if the captions are visual equivalent images of text embedded in video." "Captions should not obscure or obstruct relevant information in the video."
- Alternative for time-based media: "document including correctly sequenced text descriptions of time-based visual and auditory information and providing a means for achieving the outcomes of any time-based interaction". Its note says a screenplay meets this only "if it was corrected to accurately represent the final synchronized media after editing." This is the W3C's word for what the brief calls a transcript.
- Synchronized media: "audio or video synchronized with another format for presenting information and/or with time-based interactive components, unless the media is a media alternative for text that is clearly labeled as such".

One more criterion bears on the settled rule of no autoplay with sound: 1.4.2 Audio Control (Level A), "If any audio on a web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level."

What this means for Oath & Action's two video forms (DR-301), as the criteria read: Dustin on camera as host and a voiceover over charts are both prerecorded synchronized media, so each needs captions (1.2.2) and, at AA, audio description of anything shown and not said (1.2.5). A voiceover that reads every chart value aloud carries its own description; a chart shown with music alone does not. A live stream needs live captions (1.2.4). A full transcript that also describes what is shown meets 1.2.3 at Level A and does not meet 1.2.5 at AA on its own.

### B. Captions and transcripts on each video platform

| Platform | Upload a caption file | Formats | Auto captions | Transcript | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|
| YouTube | Yes. YouTube Studio, Subtitles, Add language, then "Upload file", "With timing" or "Without timing". Captions can also be added during upload | Basic: SubRip .srt, SubViewer .sbv or .sub, MPsub .mpsub, LRC .lrc, Videotron Lambda .cap. Advanced: SAMI .smi or .sami, RealText .rt, WebVTT .vtt, TTML .ttml, DFXP .ttml or .dfxp. Broadcast: Scenarist .scc ("our preferred file format"), EBU-STL .stl, .tds, .cin, .asc, .cap. ".srt and .sbv: Only basic versions of these files are supported. No style info (markup) is recognized. The file must be in plain UTF-8." | Yes, in English and many other languages. "You should always review automatic captions and edit any parts that haven't been properly transcribed." English automatic captions now show "expressive captions" (intensity in capitals, sighs, environmental noise). Live automatic captions are English only, normal latency only | "Auto-sync": paste or upload a transcript and YouTube sets the timing; "Transcripts are not recommended for videos that are over an hour long or have poor audio quality." | https://support.google.com/youtube/answer/2734796 ; https://support.google.com/youtube/answer/2734698 ; https://support.google.com/youtube/answer/6373554 | 2026-11-21 | read |
| TikTok | No official page found that offers a caption file upload | Not found | Yes. TikTok's newsroom describes creators selecting auto captions on the editing page after uploading or recording, editing the text, and viewers turning captions off | Not found | https://newsroom.tiktok.com/auto-captions-on-tiktok ; support.tiktok.com pages draw their text by script and showed only "TikTok Support" to the reader | 2026-11-21 | search-result (auto captions); not-found (file upload, transcript) |
| Instagram Reels | No official page found that offers a caption file upload | Not found | Yes. Instagram's help page "Manage closed captions for your reels on Instagram" says Instagram uses speech recognition to create closed captions automatically, which the maker can turn on or off | Not found. On-screen text is a separate tool, "Add text and text-to-speech to your reel" | https://help.instagram.com/7487270478066359/ (refused the automated reader, HTTP 400) | 2026-11-21 | search-result |
| LinkedIn video | Yes, on desktop: "You must have an associated SRT (SubRip Subtitle) file attached to the video before it can be posted." "Closed captions can be added to videos posted either by personal accounts or LinkedIn Pages." Page marked "Last updated: 5 years ago" | SRT only, per the page | Yes. "Add auto captions" toggle, with "Review captions before viewers can see them"; captions can be edited or removed after posting. Page marked "Last updated: 2 years ago" | Not offered on the pages read | https://www.linkedin.com/help/linkedin/answer/a552177 ; https://www.linkedin.com/help/linkedin/answer/a1327025 | 2026-11-21 | read |
| X video | Yes. In the post composer, "Upload caption file (.srt)", then "Upload captions"; verified subscribers can also upload in Media Studio. Captions show "toward the bottom of the video" for viewers who turn captions on | .srt | X's help text is reported to say captions generate automatically; a hearing-loss charity (RNID) reports it could not make that work. Not confirmed | Not found | https://help.x.com/en/using-x/upload-caption-srt-file (HTTP 403 to the automated reader) | 2026-11-21 | search-result |

Burned-in captions, which WCAG calls open captions, are words drawn into the video's own pixels. Every platform shows them because they are part of the picture, and none can switch them off or hand them to a screen reader. That makes them a second layer at most: the closed caption file stays the one a reader can turn on, resize or read aloud. Where a burned-in line runs, it must clear each app's button and caption zones, which the specifications file records per channel in its "Safe area or crop" column (`work/research/20261121_Platform-Specifications.md`; the shared video frames are its section 11).

### C. Each platform's own label for AI-generated or altered content

| Platform | The label and when it applies | Source page | Checked | Status |
|---|---|---|---|---|
| YouTube | The "AI use" setting in YouTube Studio, under Attributes at upload. "We require creators to disclose AI-generated or altered content that seems realistic." Disclosure is required for content that "Makes a real person appear to say or do something they didn't do. Alters footage of a real event or place. Generates a realistic scene that didn't actually occur. Creates music that's the main focus of the video." Once a creator answers Yes, "the content will be labeled as AI generated or altered for viewers": in the player for photorealistic content or music, in the expanded description otherwise. YouTube may label automatically "Content that contains C2PA metadata". Not required for "Color adjustment or lighting filters", "Caption creation" and other minor edits | https://support.google.com/youtube/answer/14328491 ("Disclosing use of GenAI content") | 2026-11-21 | read |
| TikTok | Community Guidelines, "Edited Media and AI-Generated Content (AIGC)": "we require creators to label AI-generated or significantly edited content that shows realistic-looking scenes or people. Unlabeled content may be removed, restricted, or labeled by our team, depending on the harm it could cause." The guidelines page reads "Effective September 24, 2026". TikTok's safety page adds that it labels content made with TikTok's own AI effects automatically and reads C2PA Content Credentials from other platforms. The words a viewer sees on the label ("Creator labeled as AI-generated") come from a search result for the support page, which draws its text by script | https://www.tiktok.com/community-guidelines/en/integrity-authenticity (lands on tiktok.com/safety/en/policies-and-engagement/integrity-authenticity) ; https://www.tiktok.com/transparency/en/supporting-responsible-transparent-ai-generated-content/ ; support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content | 2026-11-21 | read (rule); search-result (the label's words) |
| Instagram, Threads, Facebook (Meta) | "AI info". Meta's newsroom post "Our Approach to Labeling AI-Generated Content and Manipulated Media" (April 5, 2024) names Facebook, Instagram and Threads. Its update of July 1, 2024: "we're updating the 'Made with AI' label to 'AI info' across our apps". Its update of September 12, 2024: for content only modified or edited by AI tools, "we are moving the 'AI info' label to the post's menu", and the label stays on the post for content an AI tool generated. Instagram's help page describes a "Label as made with AI" control when sharing, and says Meta requires a label on "photorealistic video or realistic-sounding audio" that was digitally generated or altered | https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/ ; https://help.instagram.com/761121959519495 (HTTP 400 to the automated reader) | 2026-11-21 | read (newsroom); search-result (Instagram help) |
| LinkedIn | No self-disclosure label found. LinkedIn shows the C2PA Content Credentials icon on "all image and video content that has C2PA information attached"; selecting it shows whether AI made or edited the content, the app or device, who created it, and who issued the credential. "We're gradually making this feature available." Page marked "Last updated: 3 weeks ago" | https://www.linkedin.com/help/linkedin/answer/a6282984 ("Content credentials") | 2026-11-21 | read |
| X | "Manipulated media". X's notices page: for posts with media "determined to have been significantly and deceptively altered or fabricated, we may add a 'Manipulated media' label." The X Rules: "You may not deceptively share synthetic or manipulated media that are likely to cause harm." A claim that X now offers a "Made with AI" toggle comes from a reply by the Grok account on x.com, which is no help page; it is unverified and not used | https://help.x.com/en/rules-and-policies/manipulated-media ; https://help.x.com/en/rules-and-policies/notices-on-x (both HTTP 403 to the automated reader) | 2026-11-21 | search-result |

For the plan: these are the platforms' labels and they sit beside the guide's own label. The studio's call for this chat is no generated image, so none of these labels is triggered by chat 10's work. Two of the platforms (YouTube and TikTok) apply a label on their own when a file carries C2PA data, which some generating tools write into the file.

### D. A documentary ethics source on consent, minors and captions

Source: the Society of Professional Journalists (SPJ) Code of Ethics, "Revised October 4, 2026 at SPJ's National Convention in Columbus, Ohio", https://www.spj.org/spj-code-of-ethics/. Read November 21, 2026 in full. Status: read. The code was revised seven weeks ago; any older quotation of the 2014 code in the guide should be checked against this text before it prints.

Lines that bear on chapter 16, quoted exactly:

- "Use heightened sensitivity when dealing with crime victims (especially victims of sex crimes), juveniles, and sources or subjects who are inexperienced or unable to give consent. Consider cultural differences in approach and treatment."
- "Weigh the consequences of reporting or amplifying personal information. Private people have a greater right to control information about themselves than public figures and others who seek power, influence or attention."
- "Recognize that legal access to information differs from the ethical justification for reporting it."
- "Never publish fabricated content that could be confused with reality. Clearly label illustrations and reenactments."
- "Take responsibility for the accuracy of their work before releasing it. Verify the provenance and authenticity of the methods, sources and technology used to produce news."
- "Clearly identify the sources and technology that shape the creation of news."
- "Consider the long-term implications of the extended reach and permanence of publication."
- "Never plagiarize. Always attribute."
- On its own standing: "It is not, nor can it be under the First Amendment, legally enforceable."

The NPPA Code of Ethics for Visual Journalists sits at https://nppa.org/resources/code-ethics, but the page draws its text by script and the reader saw only its title and "Loading...". The copies found by search sit on third-party sites, so none is quoted here. Status: not-found (official text).

Matters of law that vary by state, which the guide names as such and gives no legal advice on: recording audio of a conversation (each state sets its own consent requirements), using a person's likeness to promote something (the right of publicity), and photographing minors and using their images. Source for the first: the Reporters Committee for Freedom of the Press, "Reporter's Recording Guide", which "provides a summary of each state's laws governing the recording of phone calls and in-person conversations" and says "this guide should not take the place of legal advice from a lawyer", https://www.rcfp.org/reporters-recording-guide/, read November 21, 2026. The second and third are named here as state law matters without a source read today. A host's own rules at a public meeting (for example, a council's rules on cameras) also govern, and they differ by body.

### E. The two photographs chapter 16 teaches on

Both confirmed against chapter 01's built specimens, the rights ledger and the sidecars. The Commons license boxes were read again today and say what the rights rows quote.

| | The Capitol Rotunda | The public meeting at Lake Isabella |
|---|---|---|
| File the guide shows | `work/build/assets/photography/20261112_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005-1200-Wide.jpg`, 1,200 x 797 px, 223,719 bytes | `work/build/assets/photography/20261112_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno-1200-Wide.jpg`, 1,200 x 768 px, 143,243 bytes |
| Source file and sidecar | `20261106_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005.jpg` and `.json` (1,920 x 1,275); each rendition has its own `.json` | `20261106_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno.jpg` and `.json` (1,920 x 1,229) |
| Rights rows | pho-01 (source) and pho-01r (rendition), rights ledger lines 535 and 536; T-USGOV; may ship | pho-04 (source) and pho-04r (rendition), lines 539 and 540; T-USGOV; may ship |
| License box, read again November 21, 2026 | "This image is a work of an employee of the Architect of the Capitol, taken or made as part of that person's official duties. As a work of the U.S. federal government, all images created or made by the Architect of the Capitol are in the public domain in the United States." https://commons.wikimedia.org/wiki/File:Rosa_Parks_Lying_in_Honor_(8509693081).jpg | "This image or file is a work of a U.S. Army Corps of Engineers soldier or employee, taken or made as part of that person's official duties. As a work of the U.S. federal government, the image is in the public domain." https://commons.wikimedia.org/wiki/File:A_meeting_between_Corps_and_Lake_Isabella_owners.jpg |
| Credit line chapter 01 prints | "Photograph: Architect of the Capitol." | "Photograph: John Prettyman, U.S. Army." |
| Caption chapter 01 prints (Rule 01.6 and 01.8 correct plates) | "Members of the public file past the casket of Rosa Parks, the civil rights pioneer, as she lies in honor in the Rotunda of the U.S. Capitol, Washington, D.C., October 2005. Photograph: Architect of the Capitol." | "Paul Zianno, chief of civil works acquisition and management for the U.S. Army Corps of Engineers Sacramento District, explains the Isabella Lake Dam safety project's land purchases to residents at a public meeting in Lake Isabella, California, March 27, 2014. Photograph: John Prettyman, U.S. Army." |
| Alt chapter 01 prints | "Mourners file past a casket ringed by velvet ropes in the Capitol Rotunda, under its paintings and statues." | "An official points to a project map while two residents, seen from behind, listen." |
| Date | October 30 or 31, 2005, the two days Rosa Parks lay in honor; the Commons file's "1 October 2005" is a placeholder, so the caption says "October 2005" | March 27, 2014 |
| People | Members of the public and uniformed U.S. Capitol Police officers, none named | Paul Zianno named by role, from the agency's own caption; residents seen from behind and not named |
| Crop notes | The Architect of the Capitol mark sits at the lower right; chapter 01's 5:3 crop keeps it out | The Commons description carries a stray phrase, "Cross border estate planning", that is no part of the agency caption; leave it out |
| Where chapter 01 shows it today | `s-01-6-correct` only | `s-01-8-correct` and `s-01-8-failure`, the second copy the engineer removes under P4-5 |

Two teaching points the records already hold, for the plan: the Rotunda photograph's date is known to two days and the caption gives only the month, which shows how a caption says no more than its evidence holds; the meeting photograph names the official from the agency caption and leaves the residents unnamed, which is chapter 01's rule on people.

## Contracts

- **For the engineer: the specifications JSON is at `work/research/20261121_Platform-Specifications.json`** (first channels in at 01:45 UTC; rows keep landing through the chat, so read it fresh each run). Its human-readable twin is `work/research/20261121_Platform-Specifications.md`.
- Shape: one object with `rows`, an array of one object per application. Each row has the brief's keys `id`, `channel`, `application`, `width`, `height`, `unit` (`px` or `in`), `aspect`, `formats`, `max_bytes`, `safe_area`, `smallest_shown_px`, `source`, `checked` (`2026-11-21`), `status` (`read`, `search-result` or `not-found`), and three more: `match` (`exact`, `min`, `max` or `ratio`, saying how an export's size compares), `basis` (`platform` or `studio-choice`) and `note`. The file's own `contract` key repeats this.
- `width` or `height` is null where the platform states only one side or none; a dimension check skips the null side and checks the ratio where `aspect` is set.
- `safe_area` is null, or `{"type": "insets", "top", "right", "bottom", "left"}` in the row's unit, or `{"type": "box", "width", "height"}` centered, or `{"type": "circle", "radius_pct"}` centered.
- Byte limits are decimal (1 MB = 1,000,000), the smaller reading.
- The ids the three samples need: `instagram.portrait` (the social post, 1080 x 1350), `website.page_1440`, `website.page_1024`, `website.page_390`, `website.page_360` (the web page, width only) and `print.letter` (the report page, 8.5 x 11 in trim). All six are in the file.
- Complete at 01:57 UTC: 74 rows over twelve channels (website, Substack, Instagram, Threads, X, YouTube, TikTok, LinkedIn, print, slides, shared video frames, email). Later additions to the rows, if any, keep these ids and keys.
- Added after the first landing: `safe_area` of type `insets` may carry `exclude`, a list of boxes `{"x", "y", "width", "height"}` measured from the top left that must also stay clear (TikTok's button column, used by `tiktok.*` and `video.vertical`). Print rows carry `bleed` (inches per side); their `width` and `height` are the trim. A Letter PDF passes when its TrimBox is 8.5 x 11 in and its BleedBox or MediaBox is 8.75 x 11.25 in. `bleed` is null elsewhere.
- `aspect` is a string. Parse it only when it reads number:number; some rows say "1:1 at most", "3:4 (reported)" or "16:9 or 9:16" and carry the rule in `note`.
- A row with `basis: studio-choice` holds a size the studio set inside the platform's limits; the dimension check treats it like any other row. The check should print each row's `status` beside its result, so a pass on a `search-result` row reads as such.

## Routine calls

- D4-xxx | The ethics source for chapter 16 is the SPJ Code of Ethics as revised October 4, 2026 | It was read in full on its own site; the NPPA code's official page draws its text by script and could not be read, and copies elsewhere are third-party
- D4-xxx | Sizes the platforms give in MB or KB are stored as decimal bytes (1 MB = 1,000,000) | The smaller reading, so an export that passes passes either way
- D4-xxx | Meta's and TikTok's ads-guide safe zones stand in for organic Stories, Reels and TikTok video, labeled as ads figures | They are the only safe zones either company publishes; both pages were read
- D4-xxx | Instagram posts stay at 1080 x 1350 (4:5), with words inside the center 1012 x 1350 (a 3:4 crop) | Instagram's help text shows two tall limits (4:5 and 3:4) and no page states the profile grid's crop; 4:5 passes every version and the 3:4 box survives either grid
- D4-xxx | The shared vertical video frame takes the larger of TikTok's and Instagram's margins on each side, plus TikTok's button column | One frame then serves both apps and YouTube Shorts
- D4-xxx | YouTube's banner safe area is scaled from 1235 x 338 at 2048 x 1152 to 1,544 x 423 at 2560 x 1440 | YouTube states it only at the minimum size; the scale is 1.25
- D4-xxx | Upload sizes the platforms do not state are the studio's: Instagram, Threads and TikTok avatars at 1080 x 1080, YouTube's at 800 x 800, LinkedIn document pages at 1080 x 1350, the YouTube Short at 1080 x 1920 | Each is inside the platform's stated limits and marked "studio choice"
- D4-xxx | Print bleed is 0.125 in a side on every print piece, stated as the studio's choice | No platform governs print (brief section 5, item 4)
- D4-xxx | The email body width rests on Mailchimp's help pages (600 px), recorded as an email service's guidance; Gmail's clipping size rests on Substack's page (about 102 KB), recorded as Substack's statement | No Google or mail-client page states either (brief section 5, item 2)
- D4-xxx | Platform marks get no rights row until each platform's brand guidelines are read; applications name the platform in words until then (rights row p4-03) | No platform mark is drawn in chat 10

## Done

- `work/handoffs/phase-4/20261121_Chat-10-Research-Lead-Notes.md` (new): chapter 16 facts (WCAG 2.2 media criteria, captions and AI labels on five platforms, the SPJ code, the two photographs), contracts, calls and checks.
- `work/research/20261121_Platform-Specifications.md` (new): one table per channel, twelve channels, 74 rows, each with its source page, date and status; a section on what differs from the Gate 3 report's starting sizes; a closing list of every row not marked read.
- `work/research/20261121_Platform-Specifications.json` (new): the same 74 rows for scripts, with a `contract` key describing every field.
- `work/research/20261020_Rights-Ledger.md` (modified): a new section at the end, "Added November 21, 2026: platform references for Phase 4 (chat 10)", rows p4-01 to p4-05.
- Both specification files are written by a generator in the research lead's scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/127ebfa4-7663-587b-a8ae-9ad439f7784c/scratchpad/c10/research-lead/specs_build.py` with its data in `specs_data.py`), so the Markdown and the JSON cannot disagree. The downloaded pages sit beside it in `dl/`. The scratch folder is not durable; the two project files are the record.

## Requests

- For the main session, to relay to Dustin or to the next chat's research lead: X's help center (help.x.com and business.x.com) and Instagram's (help.instagram.com) refuse automated readers, so 14 rows rest on search results for those official pages. Before chat 13 builds Instagram and X, a person or a browser session should open these pages and confirm the figures: Instagram's "Image resolution of photos you share" (4:5 or 3:4 tall limit), "Reel size & aspect ratios", the profile grid's crop; X's "How to customize your profile" (400 x 400, 1500 x 500, 2 MB) and "How to post photos or GIFs" (2:1 to 3:4 shown whole). The rows to update are named in the specifications file's "Could not verify" list.
- For the engineer (through the main session): `work/research/20261121_Platform-Specifications.json` is complete; please read the `match`, `bleed` and `safe_area.exclude` keys as the Contracts section describes, and print each row's `status` beside each pass or fail.
- For the creative director (through the main session): cite WCAG 2.2 criteria and the SPJ code by number, name and date in Basis lines. Printing a criterion's full text or the code's sentences in the guide waits on rights rows p4-04 and p4-05, since neither body's reuse terms were read today.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| C10-RL-1 | Research lead, chat 10 | Gate 3 report, section 9, "The eight channels" table | Several starting sizes differ from what the platforms state today: YouTube thumbnail (now 3840 x 2160 recommended), LinkedIn company page cover (1512 x 256), X post image (1600 x 900 has no X source), Instagram avatar (320 x 320 has no Instagram source), YouTube avatar (800 x 800 has no YouTube source) | Build to `work/research/20261121_Platform-Specifications.json`; the report's figures were starting points to verify, so the report itself needs no change | The report is approved and closed; the table was written as figures to check | Open, for the main session to note in handoff V30 |

## Tested

- Downloaded and read in full, November 21, 2026: WCAG 2.2 (W3C), the SPJ Code of Ethics, YouTube help (captions, caption formats, automatic captions, AI disclosure, channel branding, banner tips, thumbnails, resolution and aspect ratios, Shorts, end screens, encoding), LinkedIn help (closed captions, auto captions, content credentials, profile photo, cover image, Pages images, photo sharing, website sharing, documents and their FAQ), Substack help through its public article interface (image dimensions, email header and footer, social preview, thumbnail crop, truncation, custom theme, fonts, welcome emails, sender name, image editing, media embeds), TikTok's community guidelines and AIGC safety page, TikTok's in-feed ads help, TikTok's developer media and photo-post pages, Meta's newsroom post on AI labels, docs.x.com media best practices and ads creatives, ogp.me, Google Search's favicon page, Apple's archived web clip page, web.dev's manifest and maskable icon pages, the HTML standard's links section, Mailchimp's two width pages, Microsoft's slide-size page, the Reporters Committee's recording guide page, and the two Commons file pages' license boxes.
- Read through the fetch reader where a plain download was refused: Meta's "Images in Link Shares", Meta's publishing reference for Instagram, Meta's ads guide for Instagram Feed, Stories and Reels, and Meta's Threads API overview.
- Opened TikTok's in-feed safe-zone file and read its marked margins (80, 160, 440 and a 120 px column on a 720 x 1280 frame).
- Matched chapter 01's printed captions, credits and alt text for Rules 01.6 and 01.8 against the built specimens, the sidecars and rights rows pho-01, pho-01r, pho-04 and pho-04r.
- By script: the JSON parses; 74 rows with unique ids; every status is read, search-result or not-found; every row has a source and the date 2026-11-21; every box, inset and exclusion fits inside its row's width and height; every number:number aspect matches its width and height within 2 percent except `website.x_card`, whose 300 x 157 minimum is X's own figure and is noted; the six sample ids are present; no em dash in the Markdown.

## Not tested

- Any page on help.x.com, business.x.com, help.instagram.com, support.tiktok.com, the NPPA's code page, Apple's design guidelines and the W3C document license: each refused the reader or drew its text by script. Their figures are marked search-result or not-found.
- Whether Substack carries the site's colors and fonts into its emails; no page says, and no test email was sent.
- Substack's post body width; no page states it.
- Any platform's real rendering: no upload, post or capture was made on any platform, so no crop, avatar overlap or smallest display size was observed.
- The engineer's dimension script against the JSON; it did not exist when these notes were written.

## Addendum by the main session: Understanding SC 1.2.5 (02:21 UTC)

The creative director's plan leaves `why_understanding_quote` on Rule 16.12 waiting for this page. The main session read it (HTTP 200): W3C, "Understanding Success Criterion 1.2.5: Audio Description (Prerecorded)", https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html, retrieved November 21, 2026. Its "Intent" section:

- "The intent of this success criterion is to provide people who are blind or visually impaired access to the visual information in a synchronized media presentation in the same human language as the video or page on which it appears."
- "During existing pauses in dialogue, audio description provides information about actions, characters, scene changes, and on-screen text that are important and are not described or spoken in the main sound track."
- Its note: "For 1.2.3, 1.2.5, and 1.2.7, if all of the important information in the video track is already conveyed in the audio track, no additional audio description is necessary."

The note is the quote that grounds Rule 16.12: a narrator who says aloud what the screen shows meets 1.2.5 with no separate description track.
