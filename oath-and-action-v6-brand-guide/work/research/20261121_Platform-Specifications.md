# Platform specifications for Phase 4

Research lead, chat 10, November 21, 2026. These are the sizes and limits Phase 4 builds to, read from each platform's own help or developer pages on November 21, 2026 (DR-292). The same rows sit in `work/research/20261121_Platform-Specifications.json` for scripts. Handles print with the Illustrative label until Dustin names them (DR-298, DR-302).

How to read the Status column:

- **read**: the page's own text was downloaded from the official domain on November 21, 2026 and read.
- **search-result**: the official page refused an automated reader or draws its text by script, so the figure comes from what a search showed for that official address. A figure from a third-party site is never the source; where one pointed to an official page, the official page is named.
- **not-found**: no official page stated the figure. Where the studio sets it, the row says "Studio choice".

Byte limits a page writes in MB or KB are stored here as decimal bytes (1 MB = 1,000,000), the smaller reading, so a file that passes passes either way.

## 1. The Oath & Action website (chapter 20)

The share preview is the picture a link shows when someone posts it. The Open Graph protocol names the tags and sets no size; Meta's developer page and X's card documentation set the sizes. The favicon set follows the HTML standard, Google Search, Apple and web.dev. The four page widths are the studio's own test widths, so they carry "Studio choice".

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Share preview, Open Graph image (`og:image`) | 1,200 x 630 px or larger | 1.91:1 | Not stated | 8,000,000 bytes | Keep words and marks off the top and bottom 15 px at 1200 wide, since X's card is 2:1 | Not stated | https://developers.facebook.com/docs/sharing/webmasters/images/ ; https://ogp.me/ | 2026-11-21 | read |
| X card, `summary_large_image` | 300 x 157 px or larger, 4096 x 4096 px at most | 2:1 | jpg, png, webp, gif | 5,000,000 bytes | Not stated | Not stated | https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image (now redirects to https://docs.x.com/overview) | 2026-11-21 | search-result |
| Favicon in Google Search results | 8 x 8 px at least; larger than 48 x 48 px recommended | 1:1 | bmp, gif, ico, png, jpeg, ppm, tiff | Not stated | Not stated | Not stated | https://developers.google.com/search/docs/appearance/favicon-in-search | 2026-11-21 | read |
| favicon.ico at the site's root (browser tab fallback) | 16, 32 and 48 px in one file (studio choice) | 1:1 | ico | Not stated | Not stated | Not stated | https://html.spec.whatwg.org/multipage/links.html#rel-icon | 2026-11-21 | not-found |
| SVG favicon (`sizes="any"`) | Any (vector) | 1:1 | svg | Not stated | Not stated | Not stated | https://html.spec.whatwg.org/multipage/links.html#rel-icon | 2026-11-21 | read |
| Apple touch icon (`apple-touch-icon`), iPhone | 180 x 180 px (also 167 and 152) | 1:1 | png | Not stated | Not stated | Not stated | https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html | 2026-11-21 | read |
| Web app manifest icon, 192 | 192 x 192 px | 1:1 | png | Not stated | Not stated | Not stated | https://web.dev/articles/add-manifest | 2026-11-21 | read |
| Web app manifest icon, 512, maskable | 512 x 512 px | 1:1 | png | Not stated | Centered circle, radius 40 percent of the width (a 410 px circle at 512) | Not stated | https://web.dev/articles/add-manifest ; https://web.dev/articles/maskable-icon | 2026-11-21 | read |
| Web page, desktop | 1,440 px wide (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | Gate 3 report, section 9 (work/ledger/20261120_Gate-3-Report.md) | 2026-11-21 | not-found |
| Web page, tablet | 1,024 px wide (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | Gate 3 report, section 9 | 2026-11-21 | not-found |
| Web page, phone | 390 px wide (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | Gate 3 report, section 9 | 2026-11-21 | not-found |
| Web page, small phone | 360 px wide (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | Gate 3 report, section 9 | 2026-11-21 | not-found |

Notes:

- Open Graph protocol, https://ogp.me/, read: `og:image` takes optional `og:image:width`, `og:image:height`, `og:image:type` and `og:image:alt`, which it defines as "A description of what is in the image (not a caption). If the page specifies an og:image it should specify og:image:alt." The protocol sets no pixel size.
- Meta for Developers, "Images in Link Shares", read through a fetch reader (the page refuses a plain download): "Use images that are at least 1200 x 630 pixels for the best display on high resolution devices." "The minimum allowed image dimension is 200 x 200 pixels." Larger link images need "600 x 315 pixels". "Try to keep your images as close to 1.91:1 aspect ratio as possible." "The size of the image file must not exceed 8 MB." No date on the page.
- X's card page for `summary_large_image` sat at developer.twitter.com and now redirects to the general overview of docs.x.com, so X's current documentation no longer carries it. A search of the old address shows a 2:1 ratio, at least 300 x 157 and at most 4096 x 4096 px, under 5 MB, in JPG, PNG, WEBP or GIF. The search result is the only source; it is marked so. Substack's own help page (section 2) also gives X's ratio as 2:1. If X crops a 1.91:1 image to 2:1 from the center, a 1200 x 630 share image loses 15 px at the top and 15 px at the bottom, so the share image keeps its words and marks off those edges.
- Google Search's favicon page (last updated 2026-10-27) lists BMP, GIF, ICO, PNG, JPEG, PPM and TIFF and does not list SVG, so an SVG favicon needs an ICO or PNG beside it for search results.
- Apple's page is its archived Safari Web Content Guide, which still documents `apple-touch-icon` with 152, 167 and 180 px sizes and points to its design guidelines for current sizes. The guidelines page draws its text by script and was not read.
- The HTML standard (WHATWG, links section, read) says a browser may fetch `/favicon.ico` when a page names no icon, and shows `sizes="any"` for an SVG icon. It sets no pixel size, so the ICO's inner sizes are the studio's choice.
- Difference from the Gate 3 report: none in size. The report's 1200 x 630 share preview matches Meta's page; the report's "favicons from the standard set" becomes the seven rows above.

## 2. Substack (chapter 22)

Substack's help center (support.substack.com) answers an automated reader through its public article interface, so every Substack row is read from Substack's own text, with each article's last edit date. Substack sends every post in its own email template; the list after the table names the parts a publisher sets.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Publication logo | 256 x 256 px or larger | 1:1 | Not stated; transparent background asked for | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 | 2026-11-21 | read |
| Wordmark | 1,344 x 256 px or larger | 21:4 | Not stated | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 | 2026-11-21 | read |
| Header cover photo (Classic theme only) | 1,600 px wide or wider | Not stated | Not stated | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 | 2026-11-21 | read |
| Welcome page image | 600 x 600 px or larger | 1:1 | Not stated | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 | 2026-11-21 | read |
| Email header banner | 1,100 x 220 px | 5:1 | png | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 ; https://support.substack.com/hc/en-us/articles/360056142311 | 2026-11-21 | read |
| Social and post preview image | 1,200 x 630 px or larger | 1.91:1 | avif, gif, jpg, jpeg, png, webp | Not stated | Cropped by Substack to portrait, square and 3:2 landscape around a focal point the publisher sets | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 ; https://support.substack.com/hc/en-us/articles/360039016992 ; https://support.substack.com/hc/en-us/articles/55331495866772 | 2026-11-21 | read |
| Post thumbnail | Ratio only | 3:2 | Not stated | Not stated | Not stated | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 | 2026-11-21 | read |
| Full-width image in a post | Width not stated | 1:1 at most | avif, gif, jpg, jpeg, png, webp | Not stated | Taller than square is cropped to 1:1 | Not stated | https://support.substack.com/hc/en-us/articles/4408381685268 ; https://support.substack.com/hc/en-us/articles/360037832971 | 2026-11-21 | read |
| Post body width (for a chart image) | Not stated | Not stated | Not stated | Not stated | Not stated | Not stated | No Substack help page states it (searched support.substack.com, November 21, 2026) | 2026-11-21 | not-found |

Notes:

- "What are the optimal image dimensions for my Substack publication?" (edited 2026-11-12): "Logo: 256×256 px or larger, transparent background"; "Wordmark: 1344×256 px or larger (a wide, horizontal image)"; "Header cover photo: 1600 px wide or wider ... (Classic theme only)"; "Welcome image: 600×600 px or larger"; "Email banner: 1100×220 px PNG, transparent background"; "Social / post preview image: 1200×630 px or larger"; "Full-width post image: Up to 1:1; taller images are cropped to 1:1". Its ratio table gives post thumbnails 3:2, and gives "Instagram profile grid 4:5", "LinkedIn 1.91:1" and "X 2:1" as Substack's own reading of those platforms.
- "How do I crop my post thumbnail on Substack?" (edited 2026-11-05): the crop tool shows Portrait ("image assets in your Share Center"), Square ("Top Posts" and the app's Posts tab) and Landscape (Notes, desktop dashboard, home page layouts). "If you don’t adjust the crop, Substack uses a smart crop where it picks the area of the image with the most detail or highest contrast." Cropping works on the web only.
- "How do I embed media in my post" (edited 2024-12-10): "Image files that are supported are avif, gif, jpg, jpeg, png, webp." The banner "must be in PNG format." "We do not currently support custom CSS or HTML in the post editor. However, we support Datawrapper charts". Embedded YouTube and TikTok videos reach email as "a static image" that links out.
- "How can I edit images on a Substack post?" (edited 2024-08-22): each image takes alt text ("Edit alt text"), a caption, a link, a watermark of the publication's logo, crop and filters, on the web editor.
- What a publisher sets, from the articles above and "How do I edit email headers and footers" (edited 2026-06-05), "How do I change my email sender name?" (edited 2026-09-15), "How do I set up welcome emails" (edited 2026-09-16), "How do I set a custom theme" and "Can I use custom fonts" (both edited 2026-11-12): the sender name ("but not the sender email address", which is "[subdomain]@substack.com"); header and footer content for free and paid subscribers; the optional email banner; four welcome emails (free, paid, imported, founding); the social preview's text, image and crop; the logo, wordmark and welcome image; the site's colors (on Classic: Background, Accent, Welcome, Header, Footer, Secondary footer, Subscribe) and fonts (on Classic: Wordmark, Post titles, Body, Section titles, from Substack's list; "Font size is set automatically"); post image corners and cropping; each image's alt text and caption. "A mailing address is shown at the bottom of all emails." None of the pages says whether the site's colors and fonts carry into the emails; chapter 22 checks this with a test email ("Send test emails").
- Substack's post body width is not stated on any help page read. Chapter 22 measures it on a published post before it sizes a chart image, and records the measurement as the studio's.
- Difference from the Gate 3 report: the report left Substack's sizes to its help center; they are now set. The share preview is a minimum (1200 x 630 or larger) and takes Substack's own crop to portrait, square and landscape, so the image needs a focal point that survives all three.

## 3. Instagram (chapter 23)

Instagram's help center refuses an automated reader (HTTP 400, and a fetch reader sees only the words "Help Center"), so its own sizes come from search results for its pages. Meta's developer page for publishing to Instagram and Meta's ads guide were read, and they back the help center's figures where they overlap. The ads guide is written for ads; its safe zones are the only ones Meta publishes for Stories and Reels, so the studio uses them for organic posts and says so.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Profile photo (ampersand B on the Charcoal tile) | 1,080 x 1,080 px (studio choice) | 1:1 | Not stated | Not stated | Inscribed circle | Not stated | No Instagram page found; https://www.facebook.com/help/125379114252045 gives 320 x 320 for Facebook Pages only | 2026-11-21 | not-found |
| Square post | 1,080 x 1,080 px | 1:1 | JPEG through the publishing interface; JPG or PNG in the ads guide | 8,000,000 bytes | Not stated | Not stated | https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media | 2026-11-21 | search-result |
| Portrait post (the studio sample) | 1,080 x 1,350 px | 4:5 | JPEG through the publishing interface; JPG or PNG in the ads guide | 8,000,000 bytes | Words and marks inside the center 1,012 x 1,350 px (a 3:4 grid crop; studio choice) | Not stated | https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-feed | 2026-11-21 | search-result |
| Taller portrait post, if 3:4 is current | 1,080 x 1,440 px | 3:4 | Not stated | Not stated | Not stated | Not stated | https://help.instagram.com/1631821640426723 | 2026-11-21 | search-result |
| Landscape post | 1,080 x 566 px | 1.91:1 | Not stated | Not stated | Not stated | Not stated | https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media | 2026-11-21 | search-result |
| Carousel post | 1,080 x 1,350 px | 4:5 | Not stated | Not stated | As the portrait post | Not stated | https://help.instagram.com/1631821640426723 ; https://help.instagram.com/117838865078314/ | 2026-11-21 | search-result |
| Profile grid crop | Not stated | 3:4 (reported) | Not stated | Not stated | Center crop, reported | Not stated | No Instagram or Meta page found; leads: press reports of January 2025 | 2026-11-21 | not-found |
| Story | 1,080 x 1,920 px | 9:16 | jpg, png | 8,000,000 bytes | Top 269 px, bottom 672 px, sides 65 px kept clear (Meta's ads guide) | Not stated | https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-story | 2026-11-21 | search-result |
| Reel (video) | 1,080 x 1,920 px | 9:16 | mp4, mov | 300,000,000 bytes | Top 269 px, bottom 672 px, sides 65 px kept clear (Meta's ads guide) | Not stated | https://help.instagram.com/1038071743007909 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-reels | 2026-11-21 | search-result |
| Reel cover | 420 x 654 px or larger | 1:1.55 | jpg | 8,000,000 bytes | Center 1,080 x 1,676 px at 1080 x 1920 (the 1:1.55 crop) | Not stated | https://help.instagram.com/1038071743007909 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media | 2026-11-21 | search-result |

Notes:

- Instagram help, "Image resolution of photos you share on Instagram" (search-result): photos at least 1080 px wide keep their resolution at 1080 wide when the ratio lies between 1.91:1 and a tall limit, and smaller photos are enlarged to 320 wide. Two versions of the page show in search results with different tall limits: "between 1.91:1 and 4:5" (height 566 to 1350 at 1080 wide) and "between 1.91:1 and 3:4" (height 566 to 1440). The studio cannot tell which is current. Meta's publishing page (read) still says "Must be within a 4:5 to 1.91:1 range", JPEG, "8 MB maximum", width 320 to 1440 px, sRGB.
- The profile grid's crop: no Instagram or Meta page found states it. Press coverage from January 2025 (PetaPixel, Engadget, Kapwing) reports that the grid changed from squares to taller rectangles, with Kapwing giving 3:4 and the Philippine Daily Inquirer 4:5; Substack's help page (read) gives 4:5. These are leads, not sources. The studio's call: keep every word and mark of a 1080 x 1350 post inside its center 1012 x 1350 px, the 3:4 crop, so it holds under either reading.
- Reels: Instagram's help page "Reel size & aspect ratios on Instagram" (search-result) says "You can upload a reel with an aspect ratio between 1.91:1 and 9:16", with at least 30 frames a second and 720 px, and recommends a cover of "420px by 654px (or 1:1.55 ratio)". Meta's publishing page (read): reels up to 1920 px across, 9:16 recommended, "300MB maximum", 3 seconds to 15 minutes; the cover is JPEG, 8 MB at most, and "we crop the image and use the middle most 9:16 rectangle as the cover photo for the reel."
- Safe zones, from Meta's ads guide for the Reels and Stories placements (read through a fetch reader): keep "roughly 14% of the top, 35% of the bottom, and 6% on each side" free of text, logos and key elements. At 1080 x 1920 that is 269 px at the top, 672 px at the bottom and 65 px at each side, rounded up.
- The profile photo: no Instagram page found states its size. Facebook's help page for Facebook Pages gives 320 x 320, which is Facebook's, not Instagram's. The studio uploads the avatar (ampersand B on the Charcoal tile, DR-116) at 1080 x 1080 and keeps the mark inside the circle the app draws. Smallest shown: not stated on any page found.
- Differences from the Gate 3 report: the portrait post may now run to 3:4 (1080 x 1440) if the newer help text is current; the studio keeps 1080 x 1350, which every version accepts. The grid's crop is unconfirmed; the report asked for it from the help page, and no help page states it. The avatar's "320 x 320 shown" has no Instagram source.

## 4. Threads (chapter 23)

Threads has no size page of its own in Instagram's help center that a search found. Meta's developer page for publishing to Threads was read and gives the limits a post must meet. The avatar and link preview are not stated anywhere found.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Profile photo | 1,080 x 1,080 px (studio choice) | 1:1 | Not stated | Not stated | Inscribed circle | Not stated | No Threads page found | 2026-11-21 | not-found |
| Single image post | 1,080 x 1,350 px (studio choice inside Threads' limits) | 4:5 | jpg, png | 8,000,000 bytes | Not stated | Not stated | https://developers.facebook.com/docs/threads/overview | 2026-11-21 | read |
| Carousel post (2 to 20 items) | 1,080 x 1,350 px each (studio choice) | 4:5 | jpg, png | 8,000,000 bytes | Not stated | Not stated | https://developers.facebook.com/docs/threads/overview | 2026-11-21 | read |
| Video post | 1,080 x 1,920 px at most | 9:16 | mp4, mov | 1,000,000,000 bytes | Not stated | Not stated | https://developers.facebook.com/docs/threads/overview | 2026-11-21 | read |
| Link preview | The website's 1,200 x 630 px share image (studio choice) | 1.91:1 | Not stated | Not stated | Not stated | Not stated | No Threads page found | 2026-11-21 | not-found |

Notes:

- Meta for Developers, Threads API overview (read through a fetch reader): images "JPEG and PNG", "8 MB maximum", "Aspect Ratio Limit: 10:1", "Minimum Width: 320", and "Images larger than 4096 x 4096 pixels are scaled down to fit." Video "MOV or MP4", up to 1920 px across, "we recommend 9:16", "300 seconds (5 minutes) maximum", "1 GB maximum". "Text posts are limited to 500 characters." Carousels take 2 to 20 items.
- How the Threads feed crops a tall image is not stated on any page found. Meta's Threads ads page, by search result only, says ad images taller than 4:5 are cropped and centered to 4:5. The studio posts Threads images at Instagram's 4:5, which avoids that crop.
- The Threads profile photo and the link preview's image size are not stated on any page found. The studio uses the Instagram avatar and the website's 1200 x 630 share image, as the Gate 3 report planned.
- Difference from the Gate 3 report: none; the report's plan (Instagram's sizes and the website's share image) stands, now with Threads' own limits beside it.

## 9. Print (chapters 24 and 25)

No platform governs print. The page sizes are the ones the Gate 3 report names, and the bleed is the studio's choice. Each piece states its trim size, its bleed and its margins; the printer named for a job may ask for a different bleed, and that printer's figure then governs.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Report page and one-page explainer, US Letter (the studio sample) | 8.5 x 11 in trim; 8.75 x 11.25 in with 0.125 in bleed | 17:22 | pdf | Not stated | 0.125 in bleed on each side, trimmed off (studio choice) | Not stated | Gate 3 report, section 9 (chapters 24 and 25) | 2026-11-21 | not-found |
| Letterhead, US Letter | 8.5 x 11 in trim; 0.125 in bleed | 17:22 | pdf | Not stated | 0.125 in bleed (studio choice) | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |
| Event poster | 24 x 36 in trim; 0.125 in bleed | 2:3 | pdf | Not stated | 0.125 in bleed (studio choice) | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |
| Table sign | 11 x 17 in trim; 0.125 in bleed | 11:17 | pdf | Not stated | 0.125 in bleed (studio choice) | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |

Notes:

- Bleed: 0.125 in on every side, the studio's choice, so a Letter page with bleed measures 8.75 x 11.25 in. A PDF export carries the trim size as its TrimBox and the bleed size as its BleedBox.
- Margins are set in each chapter's own layout rules; this file records only the page.
- Difference from the Gate 3 report: none.

## 10. Slides (chapter 25)

Slide layouts export as PDF and PNG at 1920 x 1080 with a PowerPoint file beside them (P4-2). The pixel size is the studio's.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Slide (cover, content, data) | 1,920 x 1,080 px (studio choice) | 16:9 | pdf, png, pptx | Not stated | Not stated | Not stated | Gate 3 report, section 10, P4-2 (G3-08) | 2026-11-21 | not-found |

## Could not verify

Every row marked search-result or not-found above, gathered here.

(Filled as channels land.)
