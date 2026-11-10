# Stage C research notes: WCAG 2.2, ARIA patterns, browser support and theme storage

Research lead, round 0 of stage C, November 10, 2026. Brief: `work/handoffs/phase-2/20261110_Stage-C-Brief.md`, "Round 0 tasks, Research lead".

Status: complete. In short: WCAG 2.2 has 31 Level A and 24 Level AA criteria, quoted below from the W3C Recommendation of 12 December 2024. Six of them are new in 2.2, and 4.1.1 Parsing is removed. Eleven of the brief's fourteen components map to an APG pattern, fully, in part or as the nearest fit. The bill tracker's polite live region, the forms' error pattern and the typed ID chip have none; the chip takes the Link pattern if it links. By MDN's data, every listed platform feature has full support in current Chrome, Edge, Firefox and Safari, except `text-wrap: pretty` in Firefox and `forced-color-adjust` in Safari. MDN gives no first version for `CanvasText`, and it does not track whether screen readers announce `aria-live` changes. A theme choice can live in `localStorage`, which may be missing or throw, so the page falls back to the device setting; a classic inline script in the head applies the stored choice before the first paint. One question for Dustin: whether the dark mode control has two states or three.

## 1. WCAG 2.2 success criteria at levels A and AA

**Source.** Web Content Accessibility Guidelines (WCAG) 2.2, "W3C Recommendation 12 December 2024", https://www.w3.org/TR/WCAG22/ (this version: https://www.w3.org/TR/2024/REC-WCAG22-20241212/; SHA-256 of the copy read `6e3c5fe3...e4cf7057`). Read November 10, 2026. I took each criterion's number, name, level and words from the Recommendation itself, by script, and each Understanding page link from the link the Recommendation prints beside the criterion. All 56 Understanding pages and the quick reference (https://www.w3.org/WAI/WCAG22/quickref/) answered 200 on November 10, 2026.

**Count.** 31 criteria at Level A and 24 at Level AA, 55 in all, plus 4.1.1, which WCAG 2.2 keeps as a numbered heading with no level.

**What counts as the rule.** Section 5.1 of the Recommendation: "The main content of WCAG 2.2 is normative and defines requirements that impact conformance claims. Introductory material, appendices, sections marked as "non-normative", diagrams, examples, and notes are informative (non-normative)." So each criterion's own words sit in the quote block, and its notes follow as separate lines marked informative.

**New in 2.2.** The Recommendation's "New Features in WCAG 2.2" section: "The following success criteria are new in WCAG 2.2: 2.4.11 Focus Not Obscured (Minimum) (AA) 2.4.12 Focus Not Obscured (Enhanced) (AAA) 2.4.13 Focus Appearance (AAA) 2.5.7 Dragging Movements (AA) 2.5.8 Target Size (Minimum) (AA) 3.2.6 Consistent Help (A) 3.3.7 Redundant Entry (A) 3.3.8 Accessible Authentication (Minimum) (AA) 3.3.9 Accessible Authentication (Enhanced) (AAA)". Six of these are at A or AA, and each carries a "New" mark in the Recommendation: 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7 and 3.3.8. They are marked **New in 2.2** below.

**4.1.1 Parsing's status.** Removed. The Recommendation names it "4.1.1 Parsing (Obsolete and removed)", gives it no level, and says in the comparison with WCAG 2.1: "WCAG 2.2 has removed one success criterion, 4.1.1 Parsing. Authors that are required by policy to conform with WCAG 2.0 or 2.1 will be able to update content to WCAG 2.2, but may need to continue to test and report 4.1.1." Its Understanding page, https://www.w3.org/WAI/WCAG22/Understanding/parsing.html (SHA-256 `54919a17...eeec56c5`): "This criterion has been removed from WCAG 2.2. ... Many issues that would have failed this criterion will fail Info and Relationships or Name, Role, Value." Chapter 19 lists it as removed, with no rule tied to it.

**Numbering.** The numbers below skip because the missing ones are the 31 Level AAA criteria, which this list leaves out: 1.2.6 to 1.2.9, 1.3.6, 1.4.6 to 1.4.9, 2.1.3, 2.2.3 to 2.2.6, 2.3.2, 2.3.3, 2.4.8 to 2.4.10, 2.4.12, 2.4.13, 2.5.5, 2.5.6, 3.1.3 to 3.1.6, 3.2.5, 3.3.5, 3.3.6 and 3.3.9. The Recommendation says new criteria "have been appended to the end of the set of success criteria within their guideline", which is why 2.4.11 follows 2.4.7 and 3.2.6 follows 3.2.4.

### Principle 1, Perceivable

**1.1.1 Non-text Content** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html

> All non-text content that is presented to the user has a text alternative that serves the equivalent purpose, except for the situations listed below.
> - **Controls, Input:** If non-text content is a control or accepts user input, then it has a name that describes its purpose. (Refer to Success Criterion 4.1.2 for additional requirements for controls and content that accepts user input.)
> - **Time-Based Media:** If non-text content is time-based media, then text alternatives at least provide descriptive identification of the non-text content. (Refer to Guideline 1.2 for additional requirements for media.)
> - **Test:** If non-text content is a test or exercise that would be invalid if presented in text, then text alternatives at least provide descriptive identification of the non-text content.
> - **Sensory:** If non-text content is primarily intended to create a specific sensory experience, then text alternatives at least provide descriptive identification of the non-text content.
> - **CAPTCHA:** If the purpose of non-text content is to confirm that content is being accessed by a person rather than a computer, then text alternatives that identify and describe the purpose of the non-text content are provided, and alternative forms of CAPTCHA using output modes for different types of sensory perception are provided to accommodate different disabilities.
> - **Decoration, Formatting, Invisible:** If non-text content is pure decoration, is used only for visual formatting, or is not presented to users, then it is implemented in a way that it can be ignored by assistive technology.

**1.2.1 Audio-only and Video-only (Prerecorded)** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html

> For prerecorded audio-only and prerecorded video-only media, the following are true, except when the audio or video is a media alternative for text and is clearly labeled as such:
> - **Prerecorded Audio-only:** An alternative for time-based media is provided that presents equivalent information for prerecorded audio-only content.
> - **Prerecorded Video-only:** Either an alternative for time-based media or an audio track is provided that presents equivalent information for prerecorded video-only content.

**1.2.2 Captions (Prerecorded)** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html

> Captions are provided for all prerecorded audio content in synchronized media, except when the media is a media alternative for text and is clearly labeled as such.

**1.2.3 Audio Description or Media Alternative (Prerecorded)** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/audio-description-or-media-alternative-prerecorded.html

> An alternative for time-based media or audio description of the prerecorded video content is provided for synchronized media, except when the media is a media alternative for text and is clearly labeled as such.

**1.2.4 Captions (Live)** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/captions-live.html

> Captions are provided for all live audio content in synchronized media.

**1.2.5 Audio Description (Prerecorded)** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html

> Audio description is provided for all prerecorded video content in synchronized media.

**1.3.1 Info and Relationships** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html

> Information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text.

**1.3.2 Meaningful Sequence** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html

> When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined.

**1.3.3 Sensory Characteristics** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html

> Instructions provided for understanding and operating content do not rely solely on sensory characteristics of components such as shape, color, size, visual location, orientation, or sound.

- *Note, informative:* "For requirements related to color, refer to Guideline 1.4."

**1.3.4 Orientation** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/orientation.html

> Content does not restrict its view and operation to a single display orientation, such as portrait or landscape, unless a specific display orientation is essential.

- *Note, informative:* "Examples where a particular display orientation may be essential are a bank check, a piano application, slides for a projector or television, or virtual reality content where content is not necessarily restricted to landscape or portrait display orientation."

**1.3.5 Identify Input Purpose** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html

> The purpose of each input field collecting information about the user can be programmatically determined when:
> - The input field serves a purpose identified in the Input Purposes for user interface components section; and
> - The content is implemented using technologies with support for identifying the expected meaning for form input data.

**1.4.1 Use of Color** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html

> Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.

- *Note, informative:* "This success criterion addresses color perception specifically. Other forms of perception are covered in Guideline 1.3 including programmatic access to color and other visual presentation coding."

**1.4.2 Audio Control** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html

> If any audio on a web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level.

- *Note, informative:* "Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether or not it is used to meet other success criteria) must meet this success criterion. See Conformance Requirement 5: Non-Interference."

**1.4.3 Contrast (Minimum)** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

> The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following:
> - **Large Text:** Large-scale text and images of large-scale text have a contrast ratio of at least 3:1;
> - **Incidental:** Text or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement.
> - **Logotypes:** Text that is part of a logo or brand name has no contrast requirement.

**1.4.4 Resize Text** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html

> Except for captions and images of text, text can be resized without assistive technology up to 200 percent without loss of content or functionality.

**1.4.5 Images of Text** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html

> If the technologies being used can achieve the visual presentation, text is used to convey information rather than images of text except for the following:
> - **Customizable:** The image of text can be visually customized to the user's requirements;
> - **Essential:** A particular presentation of text is essential to the information being conveyed.

- *Note, informative:* "Logotypes (text that is part of a logo or brand name) are considered essential."

**1.4.10 Reflow** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

> Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions for:
> - Vertical scrolling content at a width equivalent to 320 CSS pixels;
> - Horizontal scrolling content at a height equivalent to 256 CSS pixels.
> Except for parts of the content which require two-dimensional layout for usage or meaning.

- *Note 1, informative:* "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom. For web content which is designed to scroll horizontally (e.g., with vertical text), 256 CSS pixels is equivalent to a starting viewport height of 1024 CSS pixels at 400% zoom."
- *Note 2, informative:* "Examples of content which requires two-dimensional layout are images required for understanding (such as maps and diagrams), video, games, presentations, data tables (not individual cells), and interfaces where it is necessary to keep toolbars in view while manipulating content. It is acceptable to provide two-dimensional scrolling for such parts of the content."

**1.4.11 Non-text Contrast** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

> The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s):
> - **User Interface Components:** Visual information required to identify user interface components and states, except for inactive components or where the appearance of the component is determined by the user agent and not modified by the author;
> - **Graphical Objects:** Parts of graphics required to understand the content, except when a particular presentation of graphics is essential to the information being conveyed.

**1.4.12 Text Spacing** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html

> In content implemented using markup languages that support the following text style properties, no loss of content or functionality occurs by setting all of the following and by changing no other style property:
> - Line height (line spacing) to at least 1.5 times the font size;
> - Spacing following paragraphs to at least 2 times the font size;
> - Letter spacing (tracking) to at least 0.12 times the font size;
> - Word spacing to at least 0.16 times the font size.
> Exception: Human languages and scripts that do not make use of one or more of these text style properties in written text can conform using only the properties that exist for that combination of language and script.

- *Note 1, informative:* "Content is not required to use these text spacing values. The requirement is to ensure that when a user overrides the authored text spacing, content or functionality is not lost."
- *Note 2, informative:* "Writing systems for some languages use different text spacing settings, such as paragraph start indent. Authors are encouraged to follow locally available guidance for improving readability and legibility of text in their writing system."

**1.4.13 Content on Hover or Focus** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html

> Where receiving and then removing pointer hover or keyboard focus triggers additional content to become visible and then hidden, the following are true:
> - **Dismissible:** A mechanism is available to dismiss the additional content without moving pointer hover or keyboard focus, unless the additional content communicates an input error or does not obscure or replace other content;
> - **Hoverable:** If pointer hover can trigger the additional content, then the pointer can be moved over the additional content without the additional content disappearing;
> - **Persistent:** The additional content remains visible until the hover or focus trigger is removed, the user dismisses it, or its information is no longer valid.
> Exception: The visual presentation of the additional content is controlled by the user agent and is not modified by the author.

- *Note 1, informative:* "Examples of additional content controlled by the user agent include browser tooltips created through use of the HTML title attribute [HTML]."
- *Note 2, informative:* "Custom tooltips, sub-menus, and other nonmodal popups that display on hover and focus are examples of additional content covered by this criterion."
- *Note 3, informative:* "This criterion applies to content that appears in addition to the triggering component itself. Since hidden components that are made visible on keyboard focus (such as links used to skip to another part of a page) do not present additional content they are not covered by this criterion."

### Principle 2, Operable

**2.1.1 Keyboard** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html

> All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes, except where the underlying function requires input that depends on the path of the user's movement and not just the endpoints.

- *Note 1, informative:* "This exception relates to the underlying function, not the input technique. For example, if using handwriting to enter text, the input technique (handwriting) requires path-dependent input but the underlying function (text input) does not."
- *Note 2, informative:* "This does not forbid and should not discourage providing mouse input or other input methods in addition to keyboard operation."

**2.1.2 No Keyboard Trap** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html

> If keyboard focus can be moved to a component of the page using a keyboard interface, then focus can be moved away from that component using only a keyboard interface, and, if it requires more than unmodified arrow or tab keys or other standard exit methods, the user is advised of the method for moving focus away.

- *Note, informative:* "Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference."

**2.1.4 Character Key Shortcuts** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html

> If a keyboard shortcut is implemented in content using only letter (including upper- and lower-case letters), punctuation, number, or symbol characters, then at least one of the following is true:
> - **Turn off:** A mechanism is available to turn the shortcut off;
> - **Remap:** A mechanism is available to remap the shortcut to include one or more non-printable keyboard keys (e.g., Ctrl, Alt);
> - **Active only on focus:** The keyboard shortcut for a user interface component is only active when that component has focus.

**2.2.1 Timing Adjustable** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html

> For each time limit that is set by the content, at least one of the following is true:
> - **Turn off:** The user is allowed to turn off the time limit before encountering it; or
> - **Adjust:** The user is allowed to adjust the time limit before encountering it over a wide range that is at least ten times the length of the default setting; or
> - **Extend:** The user is warned before time expires and given at least 20 seconds to extend the time limit with a simple action (for example, "press the space bar"), and the user is allowed to extend the time limit at least ten times; or
> - **Real-time Exception:** The time limit is a required part of a real-time event (for example, an auction), and no alternative to the time limit is possible; or
> - **Essential Exception:** The time limit is essential and extending it would invalidate the activity; or
> - **20 Hour Exception:** The time limit is longer than 20 hours.

- *Note, informative:* "This success criterion helps ensure that users can complete tasks without unexpected changes in content or context that are a result of a time limit. This success criterion should be considered in conjunction with Success Criterion 3.2.1, which puts limits on changes of content or context as a result of user action."

**2.2.2 Pause, Stop, Hide** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html

> For moving, blinking, scrolling, or auto-updating information, all of the following are true:
> - **Moving, blinking, scrolling:** For any moving, blinking or scrolling information that (1) starts automatically, (2) lasts more than five seconds, and (3) is presented in parallel with other content, there is a mechanism for the user to pause, stop, or hide it unless the movement, blinking, or scrolling is part of an activity where it is essential; and
> - **Auto-updating:** For any auto-updating information that (1) starts automatically and (2) is presented in parallel with other content, there is a mechanism for the user to pause, stop, or hide it or to control the frequency of the update unless the auto-updating is part of an activity where it is essential.

- *Note 1, informative:* "For requirements related to flickering or flashing content, refer to Guideline 2.3."
- *Note 2, informative:* "Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference."
- *Note 3, informative:* "Content that is updated periodically by software or that is streamed to the user agent is not required to preserve or present information that is generated or received between the initiation of the pause and resuming presentation, as this may not be technically possible, and in many situations could be misleading to do so."
- *Note 4, informative:* "An animation that occurs as part of a preload phase or similar situation can be considered essential if interaction cannot occur during that phase for all users and if not indicating progress could confuse users or cause them to think that content was frozen or broken."

**2.3.1 Three Flashes or Below Threshold** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html

> Web pages do not contain anything that flashes more than three times in any one second period, or the flash is below the general flash and red flash thresholds.

- *Note, informative:* "Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference."

**2.4.1 Bypass Blocks** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html

> A mechanism is available to bypass blocks of content that are repeated on multiple web pages.

**2.4.2 Page Titled** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html

> Web pages have titles that describe topic or purpose.

**2.4.3 Focus Order** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html

> If a web page can be navigated sequentially and the navigation sequences affect meaning or operation, focusable components receive focus in an order that preserves meaning and operability.

**2.4.4 Link Purpose (In Context)** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html

> The purpose of each link can be determined from the link text alone or from the link text together with its programmatically determined link context, except where the purpose of the link would be ambiguous to users in general.

**2.4.5 Multiple Ways** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html

> More than one way is available to locate a web page within a set of web pages except where the web page is the result of, or a step in, a process.

**2.4.6 Headings and Labels** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html

> Headings and labels describe topic or purpose.

**2.4.7 Focus Visible** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html

> Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.

**2.4.11 Focus Not Obscured (Minimum)** (Level AA). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html

> When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content.

- *Note 1, informative:* "Where content in a configurable interface can be repositioned by the user, then only the initial positions of user-movable content are considered for testing and conformance of this success criterion."
- *Note 2, informative:* "Content opened by the user may obscure the component receiving focus. If the user can reveal the focused component without advancing the keyboard focus, the component with focus is not considered visually hidden due to author-created content."

**2.5.1 Pointer Gestures** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html

> All functionality that uses multipoint or path-based gestures for operation can be operated with a single pointer without a path-based gesture, unless a multipoint or path-based gesture is essential.

- *Note, informative:* "This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology)."

**2.5.2 Pointer Cancellation** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation.html

> For functionality that can be operated using a single pointer, at least one of the following is true:
> - **No Down-Event:** The down-event of the pointer is not used to execute any part of the function;
> - **Abort or Undo:** Completion of the function is on the up-event, and a mechanism is available to abort the function before completion or to undo the function after completion;
> - **Up Reversal:** The up-event reverses any outcome of the preceding down-event;
> - **Essential:** Completing the function on the down-event is essential.

- *Note 1, informative:* "Functions that emulate a keyboard or numeric keypad key press are considered essential."
- *Note 2, informative:* "This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology)."

**2.5.3 Label in Name** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html

> For user interface components with labels that include text or images of text, the name contains the text that is presented visually.

- *Note, informative:* "A best practice is to have the text of the label at the start of the name."

**2.5.4 Motion Actuation** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html

> Functionality that can be operated by device motion or user motion can also be operated by user interface components and responding to the motion can be disabled to prevent accidental actuation, except when:
> - **Supported Interface:** The motion is used to operate functionality through an accessibility supported interface;
> - **Essential:** The motion is essential for the function and doing so would invalidate the activity.

**2.5.7 Dragging Movements** (Level AA). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html

> All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging, unless dragging is essential or the functionality is determined by the user agent and not modified by the author.

- *Note, informative:* "This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology)."

**2.5.8 Target Size (Minimum)** (Level AA). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

> The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:
> - **Spacing:** Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target;
> - **Equivalent:** The function can be achieved through a different control on the same page that meets this criterion;
> - **Inline:** The target is in a sentence or its size is otherwise constrained by the line-height of non-target text;
> - **User Agent Control:** The size of the target is determined by the user agent and is not modified by the author;
> - **Essential:** A particular presentation of the target is essential or is legally required for the information being conveyed.

- *Note 1, informative:* "Targets that allow for values to be selected spatially based on position within the target are considered one target for the purpose of the success criterion. Examples include sliders, color pickers displaying a gradient of colors, or editable areas where you position the cursor."
- *Note 2, informative:* "For inline targets the line-height should be interpreted as perpendicular to the flow of text. For example, in a language displayed vertically, the line-height would be horizontal."

### Principle 3, Understandable

**3.1.1 Language of Page** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html

> The default human language of each web page can be programmatically determined.

**3.1.2 Language of Parts** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html

> The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text.

**3.2.1 On Focus** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/on-focus.html

> When any user interface component receives focus, it does not initiate a change of context.

**3.2.2 On Input** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/on-input.html

> Changing the setting of any user interface component does not automatically cause a change of context unless the user has been advised of the behavior before using the component.

**3.2.3 Consistent Navigation** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html

> Navigational mechanisms that are repeated on multiple web pages within a set of web pages occur in the same relative order each time they are repeated, unless a change is initiated by the user.

**3.2.4 Consistent Identification** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html

> Components that have the same functionality within a set of web pages are identified consistently.

**3.2.6 Consistent Help** (Level A). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html

> If a web page contains any of the following help mechanisms, and those mechanisms are repeated on multiple web pages within a set of web pages, they occur in the same order relative to other page content, unless a change is initiated by the user:
> - Human contact details;
> - Human contact mechanism;
> - Self-help option;
> - A fully automated contact mechanism.

- *Note 1, informative:* "Help mechanisms may be provided directly on the page, or may be provided via a direct link to a different page containing the information."
- *Note 2, informative:* "For this success criterion, "the same order relative to other page content" can be thought of as how the content is ordered when the page is serialized. The visual position of a help mechanism is likely to be consistent across pages for the same page variation (e.g., CSS break-point). The user can initiate a change, such as changing the page's zoom or orientation, which may trigger a different page variation. This criterion is concerned with relative order across pages displayed in the same page variation (e.g., same zoom level and orientation)."

**3.3.1 Error Identification** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html

> If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text.

**3.3.2 Labels or Instructions** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html

> Labels or instructions are provided when content requires user input.

**3.3.3 Error Suggestion** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html

> If an input error is automatically detected and suggestions for correction are known, then the suggestions are provided to the user, unless it would jeopardize the security or purpose of the content.

**3.3.4 Error Prevention (Legal, Financial, Data)** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html

> For web pages that cause legal commitments or financial transactions for the user to occur, that modify or delete user-controllable data in data storage systems, or that submit user test responses, at least one of the following is true:
> - **Reversible:** Submissions are reversible.
> - **Checked:** Data entered by the user is checked for input errors and the user is provided an opportunity to correct them.
> - **Confirmed:** A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission.

**3.3.7 Redundant Entry** (Level A). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html

> Information previously entered by or provided to the user that is required to be entered again in the same process is either:
> - auto-populated, or
> - available for the user to select.
> Except when:
> - re-entering the information is essential,
> - the information is required to ensure the security of the content, or
> - previously entered information is no longer valid.

**3.3.8 Accessible Authentication (Minimum)** (Level AA). **New in 2.2.**

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html

> A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following:
> - **Alternative:** Another authentication method that does not rely on a cognitive function test.
> - **Mechanism:** A mechanism is available to assist the user in completing the cognitive function test.
> - **Object Recognition:** The cognitive function test is to recognize objects.
> - **Personal Content:** The cognitive function test is to identify non-text content the user provided to the website.

- *Note 1, informative:* ""Object recognition" and "Personal content" may be represented by images, video, or audio."
- *Note 2, informative:* "Examples of mechanisms that satisfy this criterion include: support for password entry by password managers to reduce memory need, and copy and paste to reduce the cognitive burden of re-typing."

### Principle 4, Robust

**4.1.1 Parsing (Obsolete and removed)**. No level: removed in WCAG 2.2.

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/parsing.html

- *Note, informative:* "This criterion was originally adopted to address problems that assistive technology had directly parsing HTML. Assistive technology no longer has any need to directly parse HTML. Consequently, these problems either no longer exist or are addressed by other criteria. This criterion no longer has utility and is removed."

**4.1.2 Name, Role, Value** (Level A)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html

> For all user interface components (including but not limited to: form elements, links and components generated by scripts), the name and role can be programmatically determined; states, properties, and values that can be set by the user can be programmatically set; and notification of changes to these items is available to user agents, including assistive technologies.

- *Note, informative:* "This success criterion is primarily for web authors who develop or script their own user interface components. For example, standard HTML controls already meet this success criterion when used according to specification."

**4.1.3 Status Messages** (Level AA)

Understanding page: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

> In content implemented using markup languages, status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus.


## 2. WAI-ARIA Authoring Practices patterns for chapter 18's draft list

**Source.** The ARIA Authoring Practices Guide (APG), W3C Web Accessibility Initiative, patterns index https://www.w3.org/WAI/ARIA/apg/patterns/ (SHA-256 `f65c5018...11d9362b`), and 22 pattern pages under it, each saved and hashed (`SHA256SUMS` in the scratch folder `apg-patterns`). Read November 10, 2026. The pages carry no date of their own. The polite live region has no APG pattern, so its wording comes from the WAI-ARIA 1.2 specification, "W3C Recommendation 06 June 2023", https://www.w3.org/TR/wai-aria-1.2/ (SHA-256 `c0fea16f...ebc73a4849`).

**What APG is.** APG is guidance, not a standard: WCAG sets what must hold, and APG shows one tested way to build each widget. The pattern pages ask for the native HTML element where one exists (for example, the Link pattern: "Authors are strongly encouraged to use a native host language link element"; the Table pattern: "authors are strongly encouraged to use a native HTML `table` element whenever possible"). Chapter 18's code follows that: a `<button>`, an `<a href>`, a `<table>`, an `<input type="checkbox">` first, and ARIA only where HTML has no element.

### Component by component

| Chapter 18 component (brief's draft list) | APG pattern | Fit | Notes |
|---|---|---|---|
| Buttons: primary, ask and quiet | Button, https://www.w3.org/WAI/ARIA/apg/patterns/button/ | Fits | One pattern for all three looks. A button that turns something on and off is a toggle button with `aria-pressed`. A button whose action is unavailable keeps focus and carries `aria-disabled="true"` |
| Links in text and to other sites (Rule 11.13) | Link, https://www.w3.org/WAI/ARIA/apg/patterns/link/ | Fits the behavior | APG says nothing about marking a link to another site. That cue comes from Rule 11.13 and WCAG 2.4.4, Link Purpose (In Context) |
| Copy control | Button | Fits the control, not the result | APG has no copy pattern. The result ("Copied") goes to a status line, which WCAG 4.1.3, Status Messages, covers; see the live region row |
| Download control | Link, or Button | Fits | An `<a href download>` when it fetches a file; a button when a script builds the file. Either keeps its visible word as its name |
| Disclosures | Disclosure (Show/Hide), https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/ | Fits | A stack of disclosures under headings, opened one section at a time, is the Accordion pattern, https://www.w3.org/WAI/ARIA/apg/patterns/accordion/ |
| Tabs | Tabs, https://www.w3.org/WAI/ARIA/apg/patterns/tabs/ | Fits | APG recommends that tabs activate on focus when their panels show without delay. Arrow keys move between tabs; Tab leaves the tab list |
| Tables | Table, https://www.w3.org/WAI/ARIA/apg/patterns/table/ | Fits | A static table, read by a screen reader cell by cell, with no keys of its own. A sortable column sets `aria-sort` on its header ("Sortable Table Example"). The Grid pattern, https://www.w3.org/WAI/ARIA/apg/patterns/grid/, applies only if the cells become controls a reader moves among with arrow keys |
| Bill tracker as a component (Rule 11.5's polite live region) | None | No pattern fits | APG has an Alert pattern, https://www.w3.org/WAI/ARIA/apg/patterns/alert/, which is assertive and suits errors, not a tracker's updates. The tracker itself is a list, with no keys. Its updates use the `status` role or `aria-live="polite"`, quoted from WAI-ARIA 1.2 below |
| Symbol library's search and filters | Several: Landmarks (search), Disclosure, Checkbox or Radio Group, Button | No single pattern | The search field sits in a search landmark, https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/. The funnel that opens the filters is a disclosure (Rule 11.12's caption: "The funnel opens the filters, the chevron shows they are open"). Filters a reader can combine are checkboxes, https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/; filters where one replaces another are a radio group, https://www.w3.org/WAI/ARIA/apg/patterns/radio/. The clear control is a button. The result count goes to a status line. The Combobox pattern applies only if the search offers suggestions as the reader types |
| Report reader | Toolbar for the control row, Button for each control | Partial | APG has no pager or document reader pattern. The Toolbar pattern, https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/, groups three or more controls into one Tab stop with arrow keys between them; APG: "Use toolbar as a grouping element only if the group contains 3 or more controls." The new page's number goes to a status line |
| Loop stepper and other chart and diagram controls | Nearest: Carousel; also Button, Radio Group, Slider, Toolbar | No stepper pattern | The Carousel pattern, https://www.w3.org/WAI/ARIA/apg/patterns/carousel/, is the nearest: previous and next controls, a play control that stops, slides announced politely when nothing plays on its own, and "Activating the rotation control, next slide, and previous slide do not move focus". A chart control that switches between views is a radio group or a set of toggle buttons; a value along a range is a slider, https://www.w3.org/WAI/ARIA/apg/patterns/slider/ |
| Forms with the approved error pattern (DR-199) | None | No pattern fits | APG has no form pattern. The form sits in a form landmark (Landmarks pattern). An error that appears uses the Alert pattern or a status line the field points to, as chapter 11's builders line already says; the field carries `aria-invalid` and `aria-describedby` |
| Typed ID chip | None, or Link | No pattern fits a label | A chip that only names a record is text, with no role. A chip that opens the record in the atlas is a link and follows the Link pattern |
| Masthead menu with its part navigation | Disclosure, as in APG's "Disclosure (Show/Hide) Navigation Menu" example | Fits | APG's example page: "Although this example uses the word "menu" in the colloquial sense to refer to a set of navigation links, it does not use the WAI-ARIA menu role." "Typical site navigation does not need all the keyboard interactions specified by the menu and menubar pattern." The Menu Button pattern is for menus of actions, not links to parts of a page. Keyboard and attributes below |
| Dark mode switch (DR-204) | Switch, https://www.w3.org/WAI/ARIA/apg/patterns/switch/; or Radio Group | Fits, with one choice to make | A switch has two states, on and off, and APG says "it is critical the label on a switch does not change when its state changes." DR-204 makes the device setting the starting point, and a two-state switch gives a reader no way back to it once pressed. A radio group with three choices (light, dark, the device's setting) keeps that way back. See the question at the end |

### The masthead menu: APG's disclosure navigation example

Source: "Example Disclosure Navigation Menu", https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/ (SHA-256 `52a3f537...cd9704e7b`), read November 10, 2026. In its words:

> If a dropdown is open and focus is inside the navigation region, pressing Esc will close the dropdown. Moving focus out of the navigation region also closes an open dropdown. Implementing this Esc behavior is necessary to meet the WCAG 2.1 1.4.13: Content on Hover or Focus criterion.

Keyboard support table, as printed:

> - **Tab, Shift + Tab:** Move keyboard focus among top-level buttons, and if a dropdown is open, into and through links in the dropdown.
> - **Space or Enter:** If focus is on a disclosure button, activates the button, which toggles the visibility of the dropdown. If focus is on a link: If any link has aria-current set, removes it. Sets aria-current="page" on the focused link. Activates the focused link.
> - **Escape:** If a dropdown is open, closes it and sets focus on the button that controls that dropdown.
> - **Down Arrow or Right Arrow (Optional):** If focus is on a button and its dropdown is collapsed, and it is not the last button, moves focus to the next button. if focus is on a button and its dropdown is expanded, moves focus to the first link in the dropdown. If focus is on a link, and it is not the last link, moves focus to the next link.
> - **Up Arrow or Left Arrow (Optional):** If focus is on a button, and it is not the first button, moves focus to the previous button. If focus is on a link, and it is not the first link, moves focus to the previous link.
> - **Home (Optional), End (Optional):** move focus to the first or last button, or the first or last link.

Attributes: `aria-controls="IDREF"` and `aria-expanded="false"` or `"true"` on each button; `aria-current="page"` on the link to the page shown. The list sits in a navigation landmark.

### The polite live region: WAI-ARIA 1.2

Source: WAI-ARIA 1.2, "W3C Recommendation 06 June 2023", https://www.w3.org/TR/wai-aria-1.2/, read November 10, 2026.

> **status role:** "A type of live region whose content is advisory information for the user but is not important enough to justify an alert, often but not necessarily presented as a status bar." "Authors SHOULD ensure an element with role status does not receive focus as a result of change in status." "Elements with the role status have an implicit aria-live value of polite and an implicit aria-atomic value of true."

> **aria-live property, polite:** "Indicates that updates to the region should be presented at the next graceful opportunity, such as at the end of speaking the current sentence or when the user pauses typing." On assertive: "Because an interruption may disorient users or cause them to not complete their current task, authors SHOULD NOT use the assertive value unless the interruption is imperative."

> **alert role:** "A type of live region with important, and usually time-sensitive, information." "Alerts are assertive live regions, which means they cause immediate notification for assistive technology users."

The Alert pattern adds: "screen readers do not inform users of alerts that are present on the page before page load completes", and "it is crucial they do not affect keyboard focus."

### Each pattern in APG's words

#### Button Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/button/

*Keyboard Interaction*, in APG's words:

> When the button has focus:
> - Space: Activates the button.
> - Enter: Activates the button.
> - Following button activation, focus is set depending on the type of action the button performs. For example:
>   - If activating the button opens a dialog, the focus moves inside the dialog. (see dialog pattern)
>   - If activating the button closes a dialog, focus typically returns to the button that opened the dialog unless the function performed in the dialog context logically leads to a different element. For example, activating a cancel button in a dialog returns focus to the button that opened the dialog. However, if the dialog were confirming the action of deleting the page from which it was opened, the focus would logically move to a new context.
>   - If activating the button does not dismiss the current context, then focus typically remains on the button after activation, e.g., an Apply or Recalculate button.
>   - If the button action indicates a context change, such as move to next step in a wizard or add another search criteria, then it is often appropriate to move focus to the starting point for that action.
>   - If the button is activated with a shortcut key, the focus usually remains in the context from which the shortcut key was activated. For example, if Alt + U were assigned to an "Up" button that moves the currently focused item in a list one position higher in the list, pressing Alt + U when the focus is in the list would not move the focus from the list.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The button has role of button.
> - The `button` has an accessible label. By default, the accessible name is computed from any text content inside the button element. However, it can also be provided with aria-labelledby or aria-label.
> - If a description of the button's function is present, the button element has aria-describedby set to the ID of the element containing the description.
> - When the action associated with a button is unavailable, the button has aria-disabled set to `true`.
> - If the button is a toggle button, it has an aria-pressed state. When the button is toggled on, the value of this state is `true`, and when toggled off, the state is `false`.

#### Link Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/link/

*Keyboard Interaction*, in APG's words:

> - Enter: Executes the link and moves focus to the link target.
> - Shift + F10 (Optional): Opens a context menu for the link.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> The element containing the link text or graphic has role of link.

#### Disclosure (Show/Hide) Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

*Keyboard Interaction*, in APG's words:

> When the disclosure control has focus:
> - Enter: activates the disclosure control and toggles the visibility of the disclosure content.
> - Space: activates the disclosure control and toggles the visibility of the disclosure content.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The element that shows and hides the content has role button.
> - When the content is visible, the element with role `button` has aria-expanded set to `true`. When the content area is hidden, it is set to `false`.
> - Optionally, the element with role `button` has a value specified for aria-controls that refers to the element that contains all the content that is shown or hidden.

#### Accordion Pattern (Sections With Show/Hide Functionality)

URL: https://www.w3.org/WAI/ARIA/apg/patterns/accordion/

*Keyboard Interaction*, in APG's words:

> - Enter or Space:
>   - When focus is on the accordion header for a collapsed panel, expands the associated panel. If the implementation allows only one panel to be expanded, and if another panel is expanded, collapses that panel.
>   - When focus is on the accordion header for an expanded panel, collapses the panel if the implementation supports collapsing. Some implementations require one panel to be expanded at all times and allow only one panel to be expanded; so, they do not support a collapse function.
> - Tab: Moves focus to the next focusable element; all focusable elements in the accordion are included in the page Tab sequence.
> - Shift + Tab: Moves focus to the previous focusable element; all focusable elements in the accordion are included in the page Tab sequence.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The title of each accordion header is contained in an element with role button.
> - Each accordion header `button` is wrapped in an element with role heading that has a value set for aria-level that is appropriate for the information architecture of the page.
>   - If the native host language has an element with an implicit `heading` and `aria-level`, such as an HTML heading tag, a native host language element may be used.
>   - The `button` element is the only element inside the `heading` element. That is, if there are other visually persistent elements, they are not included inside the `heading` element.
> - If the accordion panel associated with an accordion header is visible, the header `button` element has aria-expanded set to `true`. If the panel is not visible, aria-expanded is set to `false`.
> - The accordion header `button` element has aria-controls set to the ID of the element containing the accordion panel content.
> - If the accordion panel associated with an accordion header is visible, and if the accordion does not permit the panel to be collapsed, the header `button` element has aria-disabled set to `true`.
> - Optionally, each element that serves as a container for panel content has role region and aria-labelledby with a value that refers to the button that controls display of the panel.
>   - Avoid using the `region` role in circumstances that create landmark region proliferation, e.g., in an accordion that contains more than approximately 6 panels that can be expanded at the same time.
>   - Role `region` is especially helpful to the perception of structure by screen reader users when panels contain heading elements or a nested accordion.

#### Tabs Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

*Keyboard Interaction*, in APG's words:

> For the tab list:
> - Tab:
>   - When focus moves into the tab list, places focus on the active `tab` element.
>   - When the tab list contains the focus, moves focus to the next element in the page tab sequence outside the tablist, which is the tabpanel unless the first element containing meaningful content inside the tabpanel is focusable.
> - When focus is on a tab element in a horizontal tab list:
>   - Left Arrow: moves focus to the previous tab. If focus is on the first tab, moves focus to the last tab. Optionally, activates the newly focused tab (See note below).
>   - Right Arrow: Moves focus to the next tab. If focus is on the last tab element, moves focus to the first tab. Optionally, activates the newly focused tab (See note below).
> - When focus is on a tab in a tablist with either horizontal or vertical orientation:
>   - Space or Enter: Activates the tab if it was not activated automatically on focus.
>   - Home (Optional): Moves focus to the first tab. Optionally, activates the newly focused tab (See note below).
>   - End (Optional): Moves focus to the last tab. Optionally, activates the newly focused tab (See note below).
>   - Shift + F10: If the tab has an associated popup menu, opens the menu.
>   - Delete (Optional): If deletion is allowed, deletes (closes) the current tab element and its associated tab panel, sets focus on the tab following the tab that was closed, and optionally activates the newly focused tab. If there is not a tab that followed the tab that was deleted, e.g., the deleted tab was the right-most tab in a left-to-right horizontal tab list, sets focus on and optionally activates the tab that preceded the deleted tab. If the application allows all tabs to be deleted, and the user deletes the last remaining tab in the tab list, the application moves focus to another element that provides a logical work flow. As an alternative to Delete, or in addition to supporting Delete, the delete function is available in a context menu.
> **Note**
> - It is recommended that tabs activate automatically when they receive focus as long as their associated tab panels are displayed without noticeable latency. This typically requires tab panel content to be preloaded. Otherwise, automatic activation slows focus movement, which significantly hampers users' ability to navigate efficiently across the tab list. For additional guidance, see Deciding When to Make Selection Automatically Follow Focus.
> - When a tab list has its aria-orientation set to `vertical`:
>   - Down Arrow performs as Right Arrow is described above.
>   - Up Arrow performs as Left Arrow is described above.
> - If the tab list is horizontal, it does not listen for Down Arrow or Up Arrow so those keys can provide their normal browser scrolling functions even when focus is inside the tab list.
> - When the tabpanel does not contain any focusable elements or the first element with content is not focusable, the tabpanel should set `tabindex="0"` to include it in the tab sequence of the page.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The element that serves as the container for the set of tabs has role tablist.
> - Each element that serves as a tab has role tab and is contained within the element with role `tablist`.
> - Each element that contains the content panel for a `tab` has role tabpanel.
> - If the tab list has a visible label, the element with role `tablist` has aria-labelledby set to a value that refers to the labelling element. Otherwise, the `tablist` element has a label provided by aria-label.
> - Each element with role `tab` has the property aria-controls referring to its associated `tabpanel` element.
> - The active `tab` element has the state aria-selected set to `true` and all other `tab` elements have it set to `false`.
> - Each element with role `tabpanel` has the property aria-labelledby referring to its associated `tab` element.
> - If a `tab` element has a popup menu, it has the property aria-haspopup set to either `menu` or `true`.
> - If the `tablist` element is vertically oriented, it has the property aria-orientation set to `vertical`. The default value of `aria-orientation` for a `tablist` element is `horizontal`.

#### Table Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/table/

*Keyboard Interaction*, in APG's words:

> Not applicable.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The table container has role table.
> - Each row container has role row and is either a DOM descendant of or owned by the `table` element or an element with role rowgroup.
> - Each cell is either a DOM descendant of or owned by a `row` element and has one of the following roles:
>   - columnheader if the cell contains a title or header information for the column.
>   - rowheader if the cell contains title or header information for the row.
>   - cell if the cell does not contain column or row header information.
> - If there is an element in the user interface that serves as a label for the table, aria-labelledby is set on the table element with a value that refers to the labelling element. Otherwise, a label is specified for the table element using aria-label.
> - If the table has a caption or description, aria-describedby is set on the table element with a value referring to the element containing the description.
> - If the table contains sortable columns or rows, aria-sort is set to an appropriate value on the header cell element for the sorted column or row as described in the Grid and Table Properties Practice.
> - If there are conditions where some rows or columns are hidden or not present in the DOM, e.g., there are widgets on the page for hiding rows or columns, the following properties are applied as described in the Grid and Table Properties Practice.
>   - aria-colcount or aria-rowcount is set to the total number of columns or rows, respectively.
>   - aria-colindex or aria-rowindex is set to the position of a cell within a row or column, respectively.
> - If the table includes cells that span multiple rows or multiple columns, then aria-rowspan or aria-colspan is applied as described in the Grid and Table Properties Practice.
> **Note**
> If rows or cells are included in a table via aria-owns, they will be presented to assistive technologies after the DOM descendants of the `table` element unless the DOM descendants are also included in the `aria-owns` attribute.

#### Alert Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/alert/

*Keyboard Interaction*, in APG's words:

> Not applicable.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> The widget has a role of alert.

#### Checkbox Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/

*Keyboard Interaction*, in APG's words:

> When the checkbox has focus, pressing the Space key changes the state of the checkbox.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The checkbox has role checkbox.
> - The checkbox has an accessible label provided by one of the following:
>   - Visible text content contained within the element with role `checkbox`.
>   - A visible label referenced by the value of aria-labelledby set on the element with role `checkbox`.
>   - aria-label set on the element with role `checkbox`.
> - When checked, the checkbox element has state aria-checked set to `true`.
> - When not checked, it has state aria-checked set to `false`.
> - When partially checked, it has state aria-checked set to `mixed`.
> - If a set of checkboxes is presented as a logical group with a visible label, the checkboxes are included in an element with role group that has the property aria-labelledby set to the ID of the element containing the label.
> - If the presentation includes additional descriptive static text relevant to a checkbox or checkbox group, the checkbox or checkbox group has the property aria-describedby set to the ID of the element containing the description.

#### Radio Group Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/radio/

*Keyboard Interaction*, in APG's words:

> **For Radio Groups Not Contained in a Toolbar**
> This section describes the keyboard interaction implemented for most radio groups. For the special case of a radio group nested inside a toolbar, use the keyboard interaction described in the following section.
> - Tab and Shift + Tab: Move focus into and out of the radio group. When focus moves into a radio group:
>   - If a radio button is checked, focus is set on the checked button.
>   - If none of the radio buttons are checked, focus is set on the first radio button in the group.
> - Space: checks the focused radio button if it is not already checked.
> - Right Arrow and Down Arrow: move focus to the next radio button in the group, uncheck the previously focused button, and check the newly focused button. If focus is on the last button, focus moves to the first button.
> - Left Arrow and Up Arrow: move focus to the previous radio button in the group, uncheck the previously focused button, and check the newly focused button. If focus is on the first button, focus moves to the last button.
> **Note**
> The initial focus behavior described above differs slightly from the behavior provided by some browsers for native HTML radio groups. In some browsers, if none of the radio buttons are selected, moving focus into the radio group with Shift + Tab will place focus on the last radio button instead of the first radio button.
> **For Radio Group Contained in a Toolbar**
> Because arrow keys are used to navigate among elements of a toolbar and the Tab key moves focus in and out of a toolbar, when a radio group is nested inside a toolbar, the keyboard interaction of the radio group is slightly different from that of a radio group that is not inside of a toolbar. For instance, users need to be able to navigate among all toolbar elements, including the radio buttons, without changing which radio button is checked. So, when navigating through a radio group in a toolbar with arrow keys, the button that is checked does not change. The keyboard interaction of a radio group nested in a toolbar is as follows.
> - Space: If the focused radio button is not checked, unchecks the currently checked radio button and checks the focused radio button. Otherwise, does nothing.
> - Enter (optional): If the focused radio button is not checked, unchecks the currently checked radio button and checks the focused radio button. Otherwise, does nothing.
> - Right Arrow:
>   - When focus is on a radio button and that radio button is **not** the last radio button in the radio group, moves focus to the next radio button.
>   - When focus is on the last radio button in the radio group and that radio button is **not** the last element in the toolbar, moves focus to the next element in the toolbar.
>   - When focus is on the last radio button in the radio group and that radio button is also the last element in the toolbar, moves focus to the first element in the toolbar.
> - Left Arrow:
>   - When focus is on a radio button and that radio button is **not** the first radio button in the radio group, moves focus to the previous radio button.
>   - When focus is on the first radio button in the radio group and that radio button is **not** the first element in the toolbar, moves focus to the previous element in the toolbar.
>   - When focus is on the first radio button in the radio group and that radio button is also the first element in the toolbar, moves focus to the last element in the toolbar.
> - Down Arrow (optional): Moves focus to the next radio button in the radio group. If focus is on the last radio button in the radio group, moves focus to the first radio button in the group.
> - Up Arrow (optional): Moves focus to the previous radio button in the radio group. If focus is on the first radio button in the radio group, moves focus to the last radio button in the group.
> **Note**
> Radio buttons in a toolbar are frequently styled in a manner that appears more like toggle buttons. For an example, See the Simple Editor Toolbar Example.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The radio buttons are contained in or owned by an element with role radiogroup.
> - Each radio button element has role radio.
> - If a radio button is checked, the `radio` element has aria-checked set to `true`. If it is not checked, it has aria-checked set to `false`.
> - Each `radio` element is labelled by its content, has a visible label referenced by aria-labelledby, or has a label specified with aria-label.
> - The `radiogroup` element has a visible label referenced by aria-labelledby or has a label specified with aria-label.
> - If elements providing additional information about either the radio group or each radio button are present, those elements are referenced by the `radiogroup` element or `radio` elements with the aria-describedby property.

#### Switch Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/switch/

*Keyboard Interaction*, in APG's words:

> - Space: When focus is on the switch, changes the state of the switch.
> - Enter (Optional): When focus is on the switch, changes the state of the switch.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The switch has role switch.
> - The switch has an accessible label provided by one of the following:
>   - Visible text content contained within the element with role `switch`.
>   - A visible label referenced by the value of aria-labelledby set on the element with role `switch`.
>   - aria-label set on the element with role `switch`.
> - When `on`, the switch element has state aria-checked set to `true`.
> - When `off`, the switch element has state aria-checked set to `false`.
> - If the switch element is an HTML `input[type="checkbox"]`, it uses the HTML `checked` attribute instead of the `aria-checked` property.
> - If a set of switches is presented as a logical group with a visible label, either:
>   - The switches are included in an element with role group that has the property aria-labelledby set to the ID of the element containing the group label.
>   - The set is contained in an HTML `fieldset` and the label for the set is contained in an HTML `legend` element.
> - If the presentation includes additional descriptive static text relevant to a switch or switch group, the switch or switch group has the property aria-describedby set to the ID of the element containing the description.

#### Toolbar Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/

*Keyboard Interaction*, in APG's words:

> - Tab and Shift + Tab: Move focus into and out of the toolbar. When focus moves into a toolbar:
>   - If focus is moving into the toolbar for the first time, focus is set on the first control that is not disabled.
>   - If the toolbar has previously contained focus, focus is optionally set on the control that last had focus. Otherwise, it is set on the first control that is not disabled.
> - For a horizontal toolbar (the default):
>   - Left Arrow: Moves focus to the previous control. Optionally, focus movement may wrap from the first element to the last element.
>   - Right Arrow: Moves focus to the next control. Optionally, focus movement may wrap from the last element to the first element.
> - Home (Optional): Moves focus to first element.
> - End (Optional): Moves focus to last element.
> **Note**
> - If the items in a toolbar are arranged vertically:
>   - Down Arrow performs as Right Arrow is described above.
>   - Up Arrow performs as Left Arrow is described above.
> - Typically, disabled elements are not focusable when navigating with a keyboard. However, in circumstances where discoverability of a function is crucial, it may be helpful if disabled controls are focusable so screen reader users are more likely to be aware of their presence. For additional guidance, see Focusability of disabled controls.
> - In applications where quick access to a toolbar is important, such as accessing an editor's toolbar from its text area, a documented shortcut key for moving focus from the relevant context to its corresponding toolbar is recommended.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The element that serves as the toolbar container has role toolbar.
> - If the toolbar has a visible label, it is referenced by aria-labelledby on the toolbar element. Otherwise, the toolbar element has a label provided by aria-label.
> - If the controls are arranged vertically, the toolbar element has aria-orientation set to `vertical`. The default orientation is horizontal.

#### Carousel (Slide Show or Image Rotator) Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/carousel/

*Keyboard Interaction*, in APG's words:

> - If the carousel has an auto-rotate feature, automatic slide rotation stops when any element in the carousel receives keyboard focus. It does not resume unless the user activates the rotation control.
> - Tab and Shift + Tab: Move focus through the interactive elements of the carousel as specified by the page tab sequence -- scripting for Tab is not necessary.
> - Button elements implement the keyboard interaction defined in the button pattern. Note: Activating the rotation control, next slide, and previous slide do not move focus, so users may easily repetitively activate them as many times as desired.
> - If present, the rotation control is the first element in the Tab sequence inside the carousel. It is essential that it precede the rotating content so it can be easily located.
> - If tab elements are used for slide picker controls, they implement the keyboard interaction defined in the Tabs Pattern.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> This section describes the element composition for three styles of carousels:
> - Basic: Has rotation, previous slide, and next slide controls but no slide picker controls.
> - Tabbed: Has basic controls plus a single tab stop for slide picker controls implemented using the tabs pattern.
> - Grouped: Has basic controls plus a series of tab stops in a group of slide picker controls where each control implements the button pattern. Because each slide selector button adds an element to the page tab sequence, this style is the least friendly for keyboard users.
> **Basic carousel elements**
> - A carousel container element that encompasses all components of the carousel, including both carousel controls and slides, has either role region or role group. The most appropriate role for the carousel container depends on the information architecture of the page. See the Landmark Regions Practice to determine whether the carousel warrants being designated as a landmark region.
> - The carousel container has the aria-roledescription property set to `carousel`.
> - If the carousel has a visible label, its accessible label is provided by the property aria-labelledby on the carousel container set to the ID of the element containing the visible label. Otherwise, an accessible label is provided by the property aria-label set on the carousel container. Note that since the `aria-roledescription` is set to "carousel", the label does not contain the word "carousel".
> - The rotation control, next slide control, and previous slide control are either native button elements (recommended) or implement the button pattern.
> - The rotation control has an accessible label provided by either its inner text or aria-label. The label changes to match the action the button will perform, e.g., "Stop slide rotation" or "Start slide rotation". A label that changes when the button is activated clearly communicates both that slide content can change automatically and when it is doing so. Note that since the label changes, the rotation control does not have any states, e.g., `aria-pressed`, specified.
> - Each slide container has role group with the property aria-roledescription set to `slide`.
> - Each slide has an accessible name:
>   - If a slide has a visible label, its accessible label is provided by the property aria-labelledby on the slide container set to the ID of the element containing the visible label.
>   - Otherwise, an accessible label is provided by the property aria-label set on the slide container.
>   - If unique names that identify the slide content are not available, a number and set size can serve as a meaningful alternative, e.g., "3 of 10". Note: Normally, including set position and size information in an accessible name is not appropriate. An exception is helpful in this implementation because group elements do not support aria-setsize or aria-posinset. The tabbed carousel implementation pattern does not have this limitation.
>   - Note that since the `aria-roledescription` is set to "slide", the label does not contain the word "slide."
> - Optionally, an element wrapping the set of slide elements has aria-atomic set to `false` and aria-live set to:
>   - `off`: if the carousel is automatically rotating.
>   - `polite`: if the carousel is **NOT** automatically rotating.
> **Tabbed Carousel Elements**
> The structure of a tabbed carousel is the same as a basic carousel except that:
> - Each slide container has role tabpanel in lieu of `group`, and it does not have the `aria-roledescription` property.
> - It has slide picker controls implemented using the tabs pattern where:
>   - Each control is a `tab` element, so activating a tab displays the slide associated with that tab.
>   - The accessible name of each `tab` indicates which slide it will display by including the name or number of the slide, e.g., "Slide 3". Slide names are preferable if each slide has a unique name.
>   - The set of controls is grouped in a `tablist` element with an accessible name provided by the value of aria-label that identifies the purpose of the tabs, e.g., "Choose slide to display."
>   - The `tab`, `tablist`, and `tabpanel` implement the properties specified in the tabs pattern.
> **Grouped Carousel Elements**
> A grouped carousel has the same structure as a basic carousel, but it also includes slide picker controls where:
> - The set of slide picker controls is contained in an element with role group.
> - The group containing the picker controls has an accessible label provided by the value of aria-label that identifies the purpose of the controls, e.g., "Choose slide to display."
> - Each picker control is a native button element (recommended) or implements the button pattern.
> - The accessible name of each picker button matches the name of the slide it displays. One technique for accomplishing this is to set aria-labelledby to a value that references the slide `group` element.
> - The picker button representing the currently displayed slide has the property aria-disabled set to `true`. Note: `aria-disabled` is preferable to the HTML `disabled` attribute because this is a circumstance where screen reader users benefit from the disabled button being included in the page Tab sequence.

#### Slider Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/slider/

*Keyboard Interaction*, in APG's words:

> - Right Arrow: Increase the value of the slider by one step.
> - Up Arrow: Increase the value of the slider by one step.
> - Left Arrow: Decrease the value of the slider by one step.
> - Down Arrow: Decrease the value of the slider by one step.
> - Home: Set the slider to the first allowed value in its range.
> - End: Set the slider to the last allowed value in its range.
> - Page Up (Optional): Increase the slider value by an amount larger than the step change made by Up Arrow.
> - Page Down (Optional): Decrease the slider value by an amount larger than the step change made by Down Arrow.
> **Note**
> - Focus is placed on the slider (the visual object that the mouse user would move, also known as the thumb.
> - In some circumstances, reversing the direction of the value change for the keys specified above, e.g., having Up Arrow decrease the value, could create a more intuitive experience.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The element serving as the focusable slider control has role slider.
> - The slider element has the aria-valuenow property set to a decimal value representing the current value of the slider.
> - The slider element has the aria-valuemin property set to a decimal value representing the minimum allowed value of the slider.
> - The slider element has the aria-valuemax property set to a decimal value representing the maximum allowed value of the slider.
> - If the value of `aria-valuenow` is not user-friendly, e.g., the day of the week is represented by a number, the aria-valuetext property is set to a string that makes the slider value understandable, e.g., "Monday".
> - If the slider has a visible label, it is referenced by aria-labelledby on the slider element. Otherwise, the slider element has a label provided by aria-label.
> - If the slider is vertically oriented, it has aria-orientation set to `vertical`. The default value of `aria-orientation` for a slider is `horizontal`.

#### Landmarks Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/

*Keyboard Interaction*, in APG's words:

> Not applicable.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> The Landmark Regions Practice describes the HTML elements, roles, properties, and usage guidelines for each of the landmark region roles.

#### Menu Button Pattern

URL: https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/

*Keyboard Interaction*, in APG's words:

> - With focus on the button:
>   - Enter: opens the menu and places focus on the first menu item.
>   - Space: Opens the menu and places focus on the first menu item.
>   - (Optional) Down Arrow: opens the menu and moves focus to the first menu item.
>   - (Optional) Up Arrow: opens the menu and moves focus to the last menu item.
> - The keyboard behaviors needed after the menu is open are described in the Menu and Menubar Pattern.

*WAI-ARIA Roles, States, and Properties*, in APG's words:

> - The element that opens the menu has role button.
> - The element with role `button` has aria-haspopup set to either `menu` or `true`.
> - When the menu is displayed, the element with role `button` has aria-expanded set to `true`. When the menu is hidden, `aria-expanded` is set to `false`.
> - The element that contains the menu items displayed by activating the button has role menu.
> - Optionally, the element with role `button` has a value specified for aria-controls that refers to the element with role `menu`.
> - Additional roles, states, and properties needed for the menu element are described in the Menu and Menubar Pattern.


## 3. Browser support for the platform features the rules depend on

**Source.** MDN's own compatibility data, the `@mdn/browser-compat-data` package, version 8.1.8, built "2026-11-02T14:19:59.386Z" (its `__meta` field), downloaded from the npm registry, https://registry.npmjs.org/@mdn/browser-compat-data/-/browser-compat-data-8.1.8.tgz, whose SHA-1 matches the registry's (`5604db35...98772209`). Checked November 10, 2026. This is the data MDN's pages draw their compatibility tables from; the pages themselves build the tables by script, so I read the data. Release dates come from the same package's browser release list.

**How to read the table.** Each cell gives the first version with full support, with no flag, no prefix, no other name and no partial mark, and that version's release date. "No" means MDN records no full support in any version. Edge before 79 is the older EdgeHTML engine; where a cell reads 79, the older Edge had none. Safari moved from version 18 to version 26 in 2025, so 26 follows 18.

| Feature | Chrome | Edge | Firefox | Safari | Safari on iOS | MDN page |
|---|---|---|---|---|---|---|
| `prefers-reduced-motion` media feature | 74 (2019-04-23) | 79 (2020-01-15) | 63 (2018-10-23) | 10.1 (2017-03-27) | 10.3 (2017-03-27) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion |
| `prefers-color-scheme` media feature | 76 (2019-07-30) | 79 (2020-01-15) | 67 (2019-05-21) | 12.1 (2019-03-25) | 13 (2019-09-19) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme |
| `color-scheme` property | 81 (2020-04-07) | 81 (2020-04-13) | 96 (2022-01-11) | 13 (2019-09-19) | 13 (2019-09-19) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme |
| `<meta name="color-scheme">` | 81 (2020-04-07) | 81 (2020-04-13) | 96 (2022-01-11) | 12.1 (2019-03-25) | 12.2 (2019-03-25) | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/color-scheme |
| `forced-colors` media feature | 89 (2021-03-02) | 79 (2020-01-15) | 89 (2021-06-01) | 16 (2022-09-12) | 16 (2022-09-12) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors |
| `forced-color-adjust` property | 89 (2021-03-02) | 79 (2020-01-15) | 113 (2023-05-09) | No | No | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/forced-color-adjust |
| System colors (`<system-color>` type, as one row) | 1 (2008-12-11) | 12 (2015-07-29) | 1 (2004-11-09) | 1 (2003-06-23) | 1 (2007-06-29) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/system-color |
| `:focus-visible` | 86 (2020-10-20) | 86 (2020-10-09) | 85 (2021-01-26) | 15.4 (2022-03-14) | 15.4 (2022-03-14) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible |
| Container queries, `@container` | 105 (2022-09-02) | 105 (2022-09-01) | 110 (2023-02-14) | 16 (2022-09-12) | 16 (2022-09-12) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@container |
| Container queries, `container-type` | 105 (2022-09-02) | 105 (2022-09-01) | 110 (2023-02-14) | 16 (2022-09-12) | 16 (2022-09-12) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/container-type |
| `text-wrap: balance` (shorthand) | 114 (2023-05-30) | 114 (2023-06-02) | 121 (2023-12-19) | 17.5 (2024-05-13) | 17.5 (2024-05-13) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap |
| `text-wrap-style: balance` (longhand) | 130 (2024-10-15) | 130 (2024-10-17) | 124 (2024-03-19) | 17.5 (2024-05-13) | 17.5 (2024-05-13) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap-style |
| `text-wrap: pretty` (shorthand) | 117 (2023-09-12) | 117 (2023-09-15) | No | 26 (2025-09-15) | 26 (2025-09-15) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap |
| `text-wrap-style: pretty` (longhand) | 130 (2024-10-15) | 130 (2024-10-17) | No | 26 (2025-09-15) | 26 (2025-09-15) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap-style |
| `inert` attribute | 102 (2022-05-24) | 102 (2022-05-31) | 112 (2023-04-11) | 15.5 (2022-05-16) | 15.5 (2022-05-16) | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert |
| `<dialog>` element | 37 (2014-08-26) | 79 (2020-01-15) | 98 (2022-03-08) | 15.4 (2022-03-14) | 15.4 (2022-03-14) | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog |
| `HTMLDialogElement.showModal()` | 37 (2014-08-26) | 79 (2020-01-15) | 98 (2022-03-08) | 15.4 (2022-03-14) | 15.4 (2022-03-14) | https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal |
| Popover API, `popover` attribute | 114 (2023-05-30) | 114 (2023-06-02) | 125 (2024-04-16) | 17 (2023-09-18) | 17 (2023-09-18) | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover |
| Popover API, `HTMLElement.popover` | 114 (2023-05-30) | 114 (2023-06-02) | 125 (2024-04-16) | 17 (2023-09-18) | 18.3 (2025-01-27) | https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/popover |
| Popover API, `popovertarget` on `<button>` | 114 (2023-05-30) | 114 (2023-06-02) | 125 (2024-04-16) | 17 (2023-09-18) | 17 (2023-09-18) | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button#popovertarget |
| `aria-live`: only the DOM reflection `Element.ariaLive` | 81 (2020-04-07) | 81 (2020-04-13) | 119 (2023-10-24) | 12.1 (2019-03-25) | 12.2 (2019-03-25) | https://developer.mozilla.org/en-US/docs/Web/API/Element/ariaLive |
| Clipboard API, `navigator.clipboard` | 66 (2018-04-17) | 79 (2020-01-15) | 63 (2018-10-23) | 13.1 (2020-03-24) | 13.4 (2020-03-24) | https://developer.mozilla.org/en-US/docs/Web/API/Navigator/clipboard |
| Clipboard API, `Clipboard.writeText()` | 66 (2018-04-17) | 79 (2020-01-15) | 63 (2018-10-23) | 13.1 (2020-03-24) | 13.4 (2020-03-24) | https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText |
| `window.localStorage` (for section 4) | 4 (2010-01-25) | 12 (2015-07-29) | 3.5 (2009-06-30) | 4 (2009-06-08) | 3.2 (2010-04-03) | https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage |
| `window.matchMedia()` (for section 4) | 9 (2011-02-03) | 12 (2015-07-29) | 6 (2011-08-16) | 5.1 (2011-07-20) | 5 (2011-10-12) | https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia |
| `MediaQueryList` `change` event (for section 4) | 39 (2014-11-18) | 79 (2020-01-15) | 55 (2017-08-08) | 14 (2020-09-16) | 14 (2020-09-16) | https://developer.mozilla.org/en-US/docs/Web/API/MediaQueryList/change_event |

### What the table means for the rules

- **Reduced motion, color scheme, focus, container queries, `inert`, `<dialog>` and the clipboard** are in every current engine. Chapter 17's reduced motion rule and chapter 18's `:focus-visible` rings can rely on them.
- **`text-wrap: pretty` has no Firefox support.** MDN records `version_added: false` for Firefox, in both the shorthand and the longhand. Treat it as an extra that some browsers apply, never as the only way a rule is met. `text-wrap: balance` works everywhere listed, through the shorthand from Chrome 114 and through the longhand from Chrome 130. One cross-check: caniuse's page for "css-text-wrap-balance", read through the fetch tool, gives Chrome from 130 and Firefox from 121, which matches MDN's longhand row for Chrome and its shorthand row for Firefox. The guide should write the shorthand, `text-wrap: balance`, which has the earlier support.
- **`forced-color-adjust` has no Safari support**, while the `forced-colors` media feature does from Safari 16. A forced colors drawing that depends on `forced-color-adjust: none` will not hold in Safari; a border, outline or text that stays visible under forced colors works in every engine. Forced colors mode itself is mainly a Windows setting, and this container cannot test it (chapter 19's script covers it).
- **System colors such as `CanvasText`.** MDN's data keeps one row for the `<system-color>` type (version 1 in every browser, which dates from the older CSS 2 keywords) and separate rows only for `AccentColor`, `AccentColorText`, `ButtonBorder`, `Mark` and `MarkText`. It has no row for `Canvas`, `CanvasText`, `LinkText`, `ButtonText` or `GrayText`, so MDN does not give their first versions. MDN's page, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/system-color (read through the fetch tool, last modified Aug 12, 2026), lists `CanvasText` as "Text color in application content or documents" and says: "In forced colors mode, authors should use colors from the `<system-color>` type for all properties that are _not_ in the set of properties whose colors are overridden." The definition is in CSS Color Module Level 4, https://www.w3.org/TR/css-color-4/ ("W3C Candidate Recommendation Draft, 3 November 2026"): "CanvasText Text in application content or documents."
- **Popover on iOS.** MDN records the `popover` attribute from Safari on iOS 17, but marks iOS 17 to 18.2 as partial for `HTMLElement.popover`: "On iOS and iPadOS, popovers are not dismissed when the user taps outside of the popover area". Full support starts at iOS 18.3. A menu built on popover needs its own close control on phones.
- **Clipboard `writeText()` needs a user action and a secure page.** MDN's notes for Firefox, Safari and Safari on iOS: "This method must be called within user gesture event handlers." For Chrome and Edge: "From version 107, this method must be called within user gesture event handlers, or the user must grant the clipboard-write permission." The Clipboard API specification marks `navigator.clipboard` as `[SecureContext]` (https://www.w3.org/TR/clipboard-apis/, "W3C Working Draft, 24 June 2026"), so it is missing on a page served over plain HTTP. Every copy button calls it from its own click and handles a refusal with words in the status line.
- **`aria-live`.** MDN's compatibility data does not track ARIA attributes. Its only row is the DOM reflection `Element.ariaLive` (shown above), which says when a script can read the attribute as a property, not when a screen reader announces a change. MDN's `aria-live` page, https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live (read through the fetch tool, last modified Sep 23, 2025), has no browser compatibility section. It says: "The `aria-live` attribute is set on an **empty** element. When an update to the page occurs, the empty element with that `aria-live` attribute should be updated with a brief announcement informing the user an update has been made." Whether a live region is heard depends on the browser and the screen reader together, which only a real screen reader test settles (chapter 19's script).

**Specifications behind each row**, with the status each showed on w3.org on November 10, 2026:

- `prefers-reduced-motion`, `prefers-color-scheme`, `forced-colors`: Media Queries Level 5, https://www.w3.org/TR/mediaqueries-5/, "W3C Working Draft, 19 February 2026". Its words for `reduce`: "Indicates that user has notified the system that they prefer an interface that removes or replaces the types of motion-based animation that either trigger discomfort for those with vestibular motion sensitivity, or distraction for those with attention deficits."
- `color-scheme`, `forced-color-adjust`: CSS Color Adjustment Module Level 1, https://www.w3.org/TR/css-color-adjust-1/, "W3C Candidate Recommendation Snapshot, 16 December 2025".
- System colors: CSS Color Module Level 4, https://www.w3.org/TR/css-color-4/, "W3C Candidate Recommendation Draft, 3 November 2026".
- `@container` and `container-type`: CSS Conditional Rules Module Level 5, https://www.w3.org/TR/css-conditional-5/, "W3C Working Draft, 30 October 2025" (the specification MDN's data links).
- `text-wrap`: CSS Text Module Level 4, https://www.w3.org/TR/css-text-4/, "W3C Working Draft, 14 August 2026".
- `:focus-visible`: Selectors Level 4, https://www.w3.org/TR/selectors-4/, "W3C Working Draft, 22 January 2026".
- `inert`, `<dialog>`, popover, `<meta name="color-scheme">`, `localStorage`: the WHATWG HTML Living Standard, https://html.spec.whatwg.org/multipage/.
- Clipboard: Clipboard API and events, https://www.w3.org/TR/clipboard-apis/, "W3C Working Draft, 24 June 2026".


## 4. Storing a reader's theme choice without a server, and avoiding a flash of the wrong theme

Sources, all read November 10, 2026: the WHATWG HTML Living Standard's Web storage, scripting, semantics, DOM and browsers sections (https://html.spec.whatwg.org/multipage/webstorage.html, scripting.html, semantics.html, dom.html, browsers.html; each saved and hashed in the scratch folders `whatwg-html-1` and `whatwg-html-2`); MDN's pages on `Window.localStorage`, the Web Storage API, storage quotas and `<meta name="color-scheme">`, read through the fetch tool, which returns its own summary with quotes; and CSS Color Adjustment Module Level 1 on w3.org.

### Where the choice lives: `localStorage`

- **What it keeps.** MDN, `Window.localStorage` (last modified Oct 12, 2026): "the stored data is saved across browser sessions", and "localStorage data has no expiration time". The store belongs to the page's origin (its scheme, host and port), so every page on the same site reads the same choice. MDN's data gives support from Chrome 4, Edge 12, Firefox 3.5, Safari 4 and Safari on iOS 3.2 (section 3's table).
- **Size.** MDN, "Storage quotas and eviction criteria" (last modified Jan 5, 2026): "Browsers can store up to 5 MiB of local storage, and 5 MiB of session storage per origin." A theme choice is a few bytes.
- **When reading it throws.** The WHATWG standard: the `localStorage` getter "Throws a "SecurityError" DOMException if the Document's origin is an opaque origin or if the request violates a policy decision (e.g., if the user agent is configured to not allow the page to persist data)." MDN adds that this "can happen if the origin uses the `file:` or `data:` schemes, for example", and: "Note that if the user blocks cookies, browsers will probably interpret this as an instruction to prevent the page from persisting data." A page shown in a sandboxed frame is one such case. The standard on the sandbox flag: "This flag forces content into an opaque origin ... and blocks access to localStorage."
- **When writing it throws.** The standard, on `setItem`: "Throws a QuotaExceededError if the new value couldn't be set. (Setting could fail if, e.g., the user has disabled storage for the site, or if the quota has been exceeded.)"
- **Private browsing.** MDN, `Window.localStorage`: "localStorage data for a document loaded in a "private browsing" or "incognito" session is cleared when the last "private" tab is closed." MDN, Web Storage API (last modified Feb 22, 2025): "In private mode, `localStorage` is treated like `sessionStorage`. The storage APIs are still available and fully functional, but all data stored in the private window is deleted when the browser or browser tab is closed." So a reader's choice holds for the private session and is gone after it.
- **Safari's clearing.** MDN, storage quotas page: "Safari proactively evicts data when cross-site tracking prevention is turned on. If an origin has no user interaction, such as click or tap, in the last seven days of browser use, its data created from script will be deleted." A reader who stays away more than a week of browsing can lose the choice.

What follows for DR-204: the stored choice is a convenience that can be missing, so the page reads it inside `try` and `catch`, and when it gets nothing it follows the device setting, which is the default DR-204 sets anyway. Writing the choice also sits inside `try`, so a refused write leaves the switch working for the visit. No server, cookie or account is needed.

### Following the device: `prefers-color-scheme`

CSS reads the device setting with `@media (prefers-color-scheme: dark)`. A script reads it with `window.matchMedia('(prefers-color-scheme: dark)')` and hears a change through the `MediaQueryList` `change` event; support for both is in section 3's table (the event from Chrome 39, Edge 79, Firefox 55 and Safari 14).

### Avoiding a flash of the wrong theme

Neither MDN nor the WHATWG standard names the "flash of the wrong theme" as such. The method below rests on what the standard says about three things: the `color-scheme` meta element, scripts in the head, and render blocking.

1. **Let CSS alone get the common case right.** Put the dark values under `@media (prefers-color-scheme: dark)` in the stylesheet, so a reader who never pressed the switch sees the device's theme from the first paint, with no script involved.
2. **Declare the schemes in the head.** The standard: "To aid user agents in rendering the page background with the desired color scheme immediately (rather than waiting for all CSS in the page to load), a 'color-scheme' value can be provided in a meta element." For a screen product that offers both, `<meta name="color-scheme" content="light dark">`.
3. **Apply a stored choice before the body exists.** A small inline script in the `<head>`, before the stylesheet and the body, reads the stored choice and sets the root attribute the engineer names, so the first paint already carries it. The standard on a classic script with neither `async` nor `defer`: "the script is fetched and evaluated immediately, blocking parsing until these are both complete." On render blocking: "A script element el is implicitly potentially render-blocking if el's type is "classic", el is parser-inserted, and el does not have an async or defer attribute", and a document "allows adding render-blocking elements if document's content type is "text/html" and the body element of document is null." The script must be a classic script: for a module script, the standard says it is "evaluated when the page has finished parsing", which is too late.
4. **Keep the head script tiny and safe.** It reads one key inside `try` and `catch`, sets one attribute and stops. Everything else (the switch, saving the choice, listening for device changes) loads with the rest of the page.

A sketch for the engineer, not run in any browser, with `data-theme` standing in for the attribute the engineer names:

```html
<head>
  <meta name="color-scheme" content="light dark">
  <script>
    try {
      var t = localStorage.getItem('oa-theme');
      if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    } catch (e) {}
  </script>
  <link rel="stylesheet" href="tokens.css">
</head>
```

### The guide itself stays light

DR-204 keeps the guide on Newsprint whatever the device asks. CSS Color Adjustment Module Level 1 (https://www.w3.org/TR/css-color-adjust-1/, "W3C Candidate Recommendation Snapshot, 16 December 2025") describes browser modes that darken pages on their own: "for pages that do not explicitly support a dark color scheme, and have not explicitly forbidden this auto-adjustment by specifying color-scheme: only light, this mode triggers auto-adjustment of the page’s colors to force the page to conform to the desired dark color scheme." MDN's `<meta name="color-scheme">` page (last modified August 18, 2026) gives `only light` as the value that "Indicates that the document _only_ supports light mode", and says `only dark` "_is invalid_". So the guide's page declares `color-scheme: only light` on its root, or `<meta name="color-scheme" content="only light">`, besides forcing the light attribute. That stops a browser's own dark mode from recoloring the guide, which the guide check's test with the device set to dark (the brief's risk list) can then confirm.


## Decisions

- D2-xxx | WCAG's words come from the Recommendation of 12 December 2024, with each Understanding page linked | The Recommendation is the normative text; the quick reference and the Understanding pages are W3C's informative companions
- D2-xxx | Each criterion keeps its notes, marked informative and kept apart from the quoted rule | WCAG 2.2 section 5.1 calls notes informative, and chapter 19 may still want them to explain a criterion
- D2-xxx | 4.1.1 Parsing is listed as removed, with no guide rule tied to it | WCAG 2.2 names it "Obsolete and removed" and gives it no level
- D2-xxx | Browser support comes from MDN's compatibility data package, version 8.1.8, not from MDN's rendered pages | The pages draw their tables from this data by script; the package is versioned and dated, and its hash matches the registry's
- D2-xxx | "First stable version" means the first version with full support, without a flag, prefix, other name or partial mark | Counting partial support, such as popover on iOS before 18.3, would overstate what a rule can rely on
- D2-xxx | `text-wrap: pretty` and `forced-color-adjust` count as extras, never as the only way a rule is met | MDN records no Firefox support for `pretty` and no Safari support for `forced-color-adjust`
- D2-xxx | The masthead menu maps to APG's disclosure navigation example, not the Menu pattern | APG's example says site navigation does not use the menu role
- D2-xxx | Status lines and the bill tracker's updates cite WAI-ARIA 1.2's `status` role and `aria-live="polite"` | APG has no pattern for a polite live region
- D2-xxx | The head script in section 4 is a sketch, labeled as not run | I did not run it in any browser

## Questions for Dustin

1. **The dark mode switch: two states or three choices (DR-204).** DR-204 asks for a visible switch that remembers the reader's choice and starts from the device setting. A switch has two states, on and off, so once a reader presses it the page has no way back to following the device. A group of three choices, Light, Dark and Match my device, keeps that way back, and APG's Radio Group pattern covers it with arrow keys between the choices. **Recommendation:** three choices in a radio group labeled "Theme", with Match my device chosen at first. If you prefer the single switch, it works too: it shows the device's theme at first, and a reader who presses it keeps the theme they chose until they clear their browser's storage.

## Tested

- WCAG 2.2: downloaded the Recommendation and parsed every criterion by script (number, name, level, "New" mark, Understanding link, words, notes): 31 at Level A, 24 at Level AA, 4.1.1 with no level, and six A or AA criteria marked new. Checked that all 56 Understanding pages and the quick reference answer 200. Read 4.1.1's Understanding page and the Recommendation's "New Features in WCAG 2.2", comparison and section 5.1 text.
- ARIA patterns: downloaded the APG patterns index, 22 pattern pages and the disclosure navigation example, and extracted each Keyboard Interaction and Roles, States, and Properties section by script. Read WAI-ARIA 1.2's `status`, `alert` and `aria-live` definitions.
- Browser support: downloaded MDN's compatibility data, version 8.1.8, from the npm registry and matched its SHA-1 to the registry's. Looked up 28 entries by script with release dates; printed the raw statements and notes for seven of them; confirmed Safari's and Edge's version numbering in the same data. Read the status line of seven W3C specifications on w3.org and the definitions quoted in section 3.
- Theme storage: read the WHATWG standard's text on `localStorage`, `setItem`, the sandbox flag, the `color-scheme` meta element, classic and module scripts, and render blocking.
- Through the fetch tool, which summarizes: MDN's pages for system colors, `aria-live`, `Window.localStorage`, the Web Storage API, storage quotas and `<meta name="color-scheme">`, and caniuse's page for `text-wrap: balance`.

## Not tested

- Any feature in a real browser. Every version number is MDN's record, not a test of mine.
- First versions for `Canvas`, `CanvasText` and the other CSS Color 4 system color keywords: MDN's data has no rows for them, and I found no other primary record.
- caniuse beyond one page. A plain request to caniuse's search and to a feature page got 406 from its server; I did not retry with other request headers, and read one page through the fetch tool.
- Whether a screen reader announces any live region. MDN does not track it, and this container has no screen reader.
- The quick reference's wording against the Recommendation's: I took the words from the Recommendation and checked only that the quick reference answers.
- APG example pages other than the disclosure navigation example, such as the Sortable Table and the switch built on a button.
- The head script sketch, in any browser, on a `file:` page or in a sandboxed frame.
- The raw text of the MDN pages read through the fetch tool: what I quote from them is the tool's quotation, not text I extracted myself.

## Change log

Files created:

- `work/handoffs/phase-2/20261110_Stage-C-Research-Notes.md` (this file).

Files modified: none. No chapter, specimen, generator, ledger, board or source file was touched.

Scratch only, outside the project, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/`:

- `research/`, one new folder per download or batch: `wcag22-tr`, `wcag22-understanding-parsing`, `apg-index`, `apg-patterns`, `apg-example-disclosure-nav`, `wai-aria-12`, `mdn-bcd-meta`, `mdn-bcd-8.1.8`, `caniuse-query-1`, `caniuse-page-1`, `whatwg-html-1`, `whatwg-html-2`, `w3c-tr-specs`.
- `scripts/`: `wcag_parse.py`, `wcag_md.py`, `apg_parse.py`, `apg_md.py`, `bcd_lookup.py`, `bcd_md.py`, `find_text.py`, each run with `python3 -I`, and their outputs `wcag22.json`, `wcag22.md`, `apg.json`, `apg.md`, `bcd_result.json`, `bcd.md`.
