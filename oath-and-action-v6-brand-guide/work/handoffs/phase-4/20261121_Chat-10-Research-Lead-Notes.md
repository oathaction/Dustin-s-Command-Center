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

Burned-in captions, which WCAG calls open captions, are words drawn into the video's own pixels. Every platform shows them because they are part of the picture, and none can switch them off or hand them to a screen reader. That makes them a second layer at most: the closed caption file stays the one a reader can turn on, resize or read aloud. Where a burned-in line runs, it must clear each app's button and caption zones, which the specifications file records per channel (section "Safe areas" of `work/research/20261121_Platform-Specifications.md`, as each channel lands).

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
- The ids the three samples need: `instagram.portrait` (the social post), `website.page_1440`, `website.page_1024`, `website.page_390`, `website.page_360` (the web page) and `print.letter` (the report page). The Instagram and print rows land next; until they do, the ids are fixed here.

## Routine calls

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
