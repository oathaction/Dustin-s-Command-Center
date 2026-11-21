# Platform specifications for Phase 4

Research lead, chat 10, November 21, 2026. These are the sizes and limits Phase 4 builds to, read from each platform's own help or developer pages on November 21, 2026 (DR-292). The same rows sit in `work/research/20261121_Platform-Specifications.json` for scripts. Handles print with the Illustrative label until Dustin names them (DR-298, DR-302).

How to read the Status column:

- **read**: the page's own text was downloaded from the official domain on November 21, 2026 and read.
- **search-result**: the official page refused an automated reader or draws its text by script, so the figure comes from what a search showed for that official address. A figure from a third-party site is never the source; where one pointed to an official page, the official page is named.
- **not-found**: no official page stated the figure. Where the studio sets it, the row says "Studio choice".

Byte limits a page writes in MB or KB are stored here as decimal bytes (1 MB = 1,000,000), the smaller reading, so a file that passes passes either way.

Smallest shown: of the pages read, only YouTube states the size at which it shows an avatar ("Image that renders at 98 X 98 px"). No other page states the smallest size it shows an avatar, favicon or thumbnail at, so those cells read "Not stated". Chapters 20 and 23 measure each one by capture at desktop and phone widths and record the measurement as the studio's.

## What differs from the Gate 3 report's starting sizes

- YouTube thumbnail: YouTube now recommends 3840 x 2160 px, at least 640 px wide (the report had 1280 x 720, which still passes). Shorts thumbnails: 2160 x 3840 px.
- YouTube avatar: no 800 x 800 figure on YouTube's page, which says only that the picture renders at 98 x 98 px; 800 x 800 stays as the studio's upload size. The banner's safe area is now set: 1235 x 338 px at 2048 x 1152, scaled to 1,544 x 423 px at 2560 x 1440.
- LinkedIn company page cover: 1512 x 256 px on LinkedIn's page today (the report left it to the help page; search results still show the older 1128 x 191 and 4200 x 700). LinkedIn's 400 x 400 avatar is a minimum.
- Instagram: the portrait post may now run to 3:4 (1080 x 1440) if the newer help text is current; the studio keeps 1080 x 1350, which every version accepts. The profile grid's crop has no official source; the studio keeps a post's words inside its center 3:4 crop. The avatar's "320 x 320 shown" has no Instagram source.
- X: the post image's 1600 x 900 has no X source; X shows a single image whole from 2:1 to 3:4. The link card's 1200 x 628 comes from X's ads pages; the organic card is 2:1 (search result).
- Substack: every size is now set from Substack's own pages, with the share image cropped by Substack to portrait, square and landscape around a focal point.
- Gmail's clipping size: no Google page states it; the 102 KB figure is Substack's statement about Gmail.
- Unchanged: the website's 1200 x 630 share preview, X's 400 x 400 avatar and 1500 x 500 header (both by search result), Instagram's 1080 x 1080, 1080 x 1350 and 1080 x 1920, YouTube's 2560 x 1440 banner and 1920 x 1080 video, LinkedIn's 1584 x 396 personal banner, the 1920 x 1080 slide, US Letter.

## 1. The Oath & Action website (chapter 20)

The share preview is the picture a link shows when someone posts it. The Open Graph protocol names the tags and sets no size; Meta's developer page and X's card documentation set the sizes. The favicon set follows the HTML standard, Google Search, Apple and web.dev. The four page widths are the studio's own test widths, so they carry "Studio choice".

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Share preview, Open Graph image (`og:image`) | 1,200 x 630 px or larger | 1.91:1 | Not stated | 8,000,000 bytes | Keep words and marks off the top and bottom 15 px at 1200 wide, since X's card is 2:1 | Not stated | https://developers.facebook.com/docs/sharing/webmasters/images/ ; https://ogp.me/ | 2026-11-21 | read |
| X card, `summary_large_image` | 300 x 157 px or larger, 4096 x 4096 px at most | 2:1 | jpg, png, webp, gif | 5,000,000 bytes | Not stated | Not stated | https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image (now redirects to https://docs.x.com/overview) | 2026-11-21 | search-result |
| Favicon in Google Search results | 8 x 8 px at least; larger than 48 x 48 px recommended | 1:1 | bmp, gif, ico, png, jpeg, ppm, tiff | Not stated | Not stated | Not stated | https://developers.google.com/search/docs/appearance/favicon-in-search | 2026-11-21 | read |
| favicon.ico at the site's root (browser tab fallback) | 16, 32 and 48 px in one file (studio choice) | 1:1 | ico | Not stated | Not stated | Not stated | https://html.spec.whatwg.org/multipage/links.html#rel-icon | 2026-11-21 | not-found |
| SVG favicon (`sizes="any"`) | Any (vector) (studio choice) | 1:1 | svg | Not stated | Not stated | Not stated | https://html.spec.whatwg.org/multipage/links.html#rel-icon | 2026-11-21 | read |
| Apple touch icon (`apple-touch-icon`), iPhone | 180 x 180 px (also 167 and 152) | 1:1 | png | Not stated | Not stated | Not stated | https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html | 2026-11-21 | read |
| Web app manifest icon, 192 | 192 x 192 px | 1:1 | png | Not stated | Not stated | Not stated | https://web.dev/articles/add-manifest | 2026-11-21 | read |
| Web app manifest icon, 512, maskable | 512 x 512 px | 1:1 | png | Not stated | Centered circle, radius 40 percent of the width (a circle 410 px across at 512) | Not stated | https://web.dev/articles/add-manifest ; https://web.dev/articles/maskable-icon | 2026-11-21 | read |
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
| Reel cover | 1,080 x 1,920 px (studio choice); the help page recommends 420 x 654 px (1:1.55) | 9:16 | jpg | 8,000,000 bytes | Center 1,080 x 1,676 px (the 1:1.55 crop), and the reel's safe zone | Not stated | https://help.instagram.com/1038071743007909 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media | 2026-11-21 | search-result |

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

## 5. X (chapter 23)

X's help center (help.x.com) and its business pages answer an automated reader with HTTP 403, so every help-center figure below is a search result for X's own address. X's developer documentation (docs.x.com) was read, and it gives the upload limits for images and video.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Profile photo (ampersand B on the Charcoal tile) | 400 x 400 px or larger | 1:1 | jpg, gif, png | 2,000,000 bytes | Inscribed circle | Not stated | https://help.x.com/en/managing-your-account/how-to-customize-your-profile ; https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo | 2026-11-21 | search-result |
| Header | 1,500 x 500 px | 3:1 | jpg, gif, png | Not stated | Top and bottom 60 px may crop; profile photo overlaps the lower left (footprint not stated) | Not stated | https://help.x.com/en/managing-your-account/how-to-customize-your-profile | 2026-11-21 | search-result |
| Single image post | 1,600 x 900 px (studio choice; shown whole from 2:1 to 3:4) | 16:9 | jpg, png, gif, webp | 5,000,000 bytes | Not stated | Not stated | https://help.x.com/en/using-x/posting-gifs-and-pictures ; https://docs.x.com/x-api/media/quickstart/best-practices | 2026-11-21 | search-result |
| Four-image post | Not stated | Not stated | Not stated | Not stated | Not stated | Not stated | https://help.x.com/en/using-x/posting-gifs-and-pictures | 2026-11-21 | not-found |
| Link card | The website's 1,200 x 630 px share image (studio choice) | 1.91:1 (shown at 2:1) | Not stated | Not stated | Not stated | Not stated | https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image | 2026-11-21 | search-result |

Notes:

- Profile, from "How to customize your profile" and "Help with uploading a profile photo" (search-result): profile photo 400 x 400 px recommended, header 1500 x 500 px recommended, JPG, GIF or PNG with no animated GIFs, profile photo up to 2 MB. Parts of the header may be cropped by screen and browser, with about 60 px at the top and bottom at risk.
- Posts, from "How to post photos or GIFs on X" (search-result): photos up to 5 MB, GIF, JPEG or PNG, 1 to 4 photos a post, and "A single photo with an aspect ratio between 2:1 and 3:4 will display in full". How four photos crop in the grid is not stated on any page found.
- X's developer page "Best practices" for media upload (read): images JPG, PNG, GIF or WEBP, "<= 5 MB"; "You may attach up to 4 photos, 1 animated GIF or 1 video in a Post." Video recommended at 1280 x 720 landscape, 720 x 1280 portrait or 720 x 720 square, "Subscribed users can upload a 1080p video and get 1080p playback"; ratio between 1:3 and 3:1; 0.5 seconds to 20 minutes and up to 8 GB for default accounts.
- Link card: the website's share image serves through the `summary_large_image` card (section 1, search-result). X's ads documentation (docs.x.com/x-ads-api/creatives, read) gives a separate rule for website cards in ads: at least 800 px wide, 1:1 or 1.91:1, 3 MB or less, BMP, JPEG or PNG. Oath & Action's posts are not ads, so the ads rule is recorded and not built to.
- Captions: .srt upload on the web composer (search-result; see the notes file's chapter 16 facts).
- Differences from the Gate 3 report: the report's "post image 1600 x 900" has no X source; X shows a single image whole anywhere from 2:1 to 3:4, so 1600 x 900 stays as the studio's choice and a 4:5 post also shows whole. The report's link card at 1200 x 628 comes from X's ads pages; the organic card is 2:1 by search result.

## 6. YouTube (chapter 23)

YouTube's help center was read in full for every row below (support.google.com/youtube, November 21, 2026).

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Channel profile picture | 800 x 800 px upload (studio choice); renders at 98 x 98 px | 1:1 | jpg, gif, bmp, png | 15,000,000 bytes | Inscribed circle | Renders at 98 x 98 px (the page's only figure) | https://support.google.com/youtube/answer/10456525 | 2026-11-21 | read |
| Channel banner | 2,560 x 1,440 px | 16:9 | Not stated | 6,000,000 bytes | Centered 1,544 x 423 px at 2560 x 1440 (1235 x 338 at 2048 x 1152) | Not stated | https://support.google.com/youtube/answer/10456525 | 2026-11-21 | read |
| Video thumbnail | 3,840 x 2,160 px recommended; 640 px wide at least | 16:9 | jpg, png | 2,000,000 bytes | Not stated | Not stated | https://support.google.com/youtube/answer/72431 | 2026-11-21 | read |
| Shorts thumbnail | 2,160 x 3,840 px recommended; 640 px high at least | 9:16 | jpg, png | 2,000,000 bytes | Not stated | Not stated | https://support.google.com/youtube/answer/72431 | 2026-11-21 | read |
| Video | 1,920 x 1,080 px | 16:9 | Not stated | Not stated | Not stated | Not stated | https://support.google.com/youtube/answer/6375112 | 2026-11-21 | read |
| Short | 1,080 x 1,920 px (studio choice); square or vertical | 9:16 | Not stated | Not stated | Not stated | Not stated | https://support.google.com/youtube/answer/12779649 | 2026-11-21 | read |
| Video watermark | 150 x 150 px or larger | 1:1 | Not stated | 1,000,000 bytes | Not stated | Not stated | https://support.google.com/youtube/answer/10456525 | 2026-11-21 | read |
| End screen (last 5 to 20 seconds) | 1,920 x 1,080 px (studio choice) | 16:9 | Not stated | Not stated | Not stated; elements placed in YouTube Studio | Not stated | https://support.google.com/youtube/answer/6388789 | 2026-11-21 | read |

Notes:

- "Manage your channel branding" (read): profile picture "JPG, GIF, BMP, or PNG file (no animated GIFs)", "should not exceed 15 MB", "Image that renders at 98 X 98 px." Banner: "Minimum dimension for upload: 2048 x 1152 px with an aspect ratio of 16:9. At the minimum dimension, the safe area for text and logos: 1235 x 338 px. Recommended dimension (especially for TV): 2560 x 1440 px." "File size: 6 MB or smaller." Watermark: "Minimum 150x150 pixels. Square image less than 1 MB in size."
- The page gives the banner's safe area at 2048 x 1152 only. Scaled by the same 1.25 to the recommended 2560 x 1440, it is 1,544 x 423 px; that scaling is the studio's arithmetic.
- "Add custom thumbnails on YouTube" (read): "a resolution of 3840 x 2160 pixels for videos and 2160 x 3840 for Shorts, with a minimum width of 640 pixels for videos and a minimum height of 640 pixels for Shorts", JPG or PNG, "Mobile: 2 MB for video thumbnails", "Desktop: 50MB". 16:9 for videos, 9:16 for Shorts. "Vertical videos with 16:9 custom thumbnails will be replaced by an auto-generated 4:5 thumbnail on the home, explore, and subscription pages."
- "Video resolution & aspect ratios" (read): "The standard aspect ratio for YouTube on a computer is 16:9", with 1080p at 1920 x 1080. "Upload YouTube Shorts" (read): "Up to 3 minutes. With a square or vertical aspect ratio." The pixel size of a Short is not stated; 1080 x 1920 is the studio's.
- "Add end screens to videos" (read): end screens fill "the last 5–20 seconds of a video", take "up to four elements" at 16:9, need a video "at least 25 seconds long", and suppress the watermark. Viewers can hide them. Where the elements sit is set in YouTube Studio; no fixed zone is stated, so the end frame (chapter 23) keeps its own words clear of the elements the editor places.
- Differences from the Gate 3 report: the thumbnail's recommended size is now 3840 x 2160 (the report had 1280 x 720, which still passes the 640 px minimum); the avatar's upload size of 800 x 800 has no YouTube source (the page states only that it renders at 98 x 98 px); the banner's central safe area is now set at 1235 x 338 at 2048 x 1152, or 1,544 x 423 at 2560 x 1440.

## 7. TikTok (chapter 23)

TikTok's support center draws its text by script and showed nothing to the reader. TikTok's ads help center and its developer documentation were read, and TikTok's own downloadable safe-zone template was opened and measured. The ads pages are written for ads; their safe zone is the only one TikTok publishes, so the studio uses it for organic video and says so.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Profile photo | 1,080 x 1,080 px (studio choice) | 1:1 | Not stated | Not stated | Center 727 x 727 px (66 of 98, after the ads page) | Not stated | https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads (ads profile photo only) | 2026-11-21 | not-found |
| Video | 1,080 x 1,920 px (studio choice inside TikTok's limits) | 9:16 | mp4, webm, mov | 500,000,000 bytes | Top 240, sides 120, bottom 660 px clear; the right button column x 780 to 960 from y 840 down also clear | Not stated | https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads ; https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide | 2026-11-21 | read |
| Photo post (up to 35 photos) | Up to 1080p; 1,080 x 1,920 px (studio choice) | 9:16 | jpg, webp | 20,000,000 bytes | As the video | Not stated | https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide ; https://developers.tiktok.com/doc/content-posting-api-reference-photo-post | 2026-11-21 | read |
| Video cover | A frame of the video (studio choice) | 9:16 | Not stated | Not stated | As the video | Not stated | No TikTok page found | 2026-11-21 | not-found |

Notes:

- "TikTok Auction In-Feed Ads" (ads help center, "Last updated: June 2026", read): vertical "9:16, more than or equal to 540*960px"; "Less than or equal to 500 MB"; the safe zone "is determined by the dimension (vertical, horizontal, or square), ad caption length, and any additional formats used", with downloadable files. Ad profile photo "98x98px, Square 1:1", ".jpg, .jpeg, .png", "less than 50 KB", and "The key element should be in the center of the 66px*66px-sized image".
- TikTok's standard in-feed safe-zone file (In-Feed-Standard Version LTR.zip, from the page above, opened November 21, 2026): a 720 x 1280 frame marked with 80 px clear at each side, 160 px at the top, 440 px at the bottom, and a 120 px column at the right running up 720 px from the bottom for the app's buttons. At 1080 x 1920 that is 120 px at each side, 240 px at the top, 660 px at the bottom, and the button column covers x 780 to 960 from y 840 down. The file is a reference only; it is not stored in the project and never ships.
- TikTok for Developers, media transfer guide (read): video MP4 (recommended), WebM or MOV, H.264 recommended, 23 to 60 frames a second, "Minimum of 360 pixels for both height and width", "Maximum of 4096 pixels", "Maximum of 4GB", and "All TikTok creators can post 3-minute videos". Photos "WebP" or "JPEG", "Maximum 1080p", "Maximum of 20MB for each image". The photo post reference (read) takes "up to 35 photo content URLs" and a `photo_cover_index` that picks one of the photos as the cover.
- The organic profile photo's size and the video cover's size are not stated on any page read. The studio uploads the avatar at 1080 x 1080 and keeps the mark inside the center 66 percent, after the ads page's 66-in-98 rule.
- Difference from the Gate 3 report: none in size; the report left cover and carousel to TikTok's pages, and they are now set (photo posts up to 1080p, up to 35 photos, cover picked from the photos).

## 8. LinkedIn (chapter 23)

LinkedIn's help center was read in full for every row but video. Each article shows its own "Last updated" line, given below. Both a personal profile and a company page are built, each with its own banner (P4-1).

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Personal profile photo | 400 x 400 px or larger | 1:1 | png, jpg | 8,000,000 bytes | Inscribed circle | Not stated | https://www.linkedin.com/help/linkedin/answer/a549049 | 2026-11-21 | read |
| Personal profile cover image | 1,584 x 396 px | 4:1 | jpg, png | 8,000,000 bytes | Profile photo overlaps the lower left (footprint not stated) | Not stated | https://www.linkedin.com/help/linkedin/answer/a568217 | 2026-11-21 | read |
| Company page logo | 400 x 400 px | 1:1 | png, jpg | 3,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a563309 | 2026-11-21 | read |
| Company page cover | 1,512 x 256 px | 189:32 | png, jpg | 3,000,000 bytes | Key details central and clear of the lower right (no figure stated) | Not stated | https://www.linkedin.com/help/linkedin/answer/a563309 | 2026-11-21 | read |
| Single image post, landscape | 1,200 x 627 px (studio choice) | 1.91:1 | jpg, png | 5,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a527229 ; https://www.linkedin.com/help/linkedin/answer/a563309 | 2026-11-21 | read |
| Single image post, square | 1,080 x 1,080 px (studio choice) | 1:1 | jpg, png | 5,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a527229 | 2026-11-21 | read |
| Single image post, portrait | 1,080 x 1,350 px (studio choice) | 4:5 | jpg, png | 5,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a527229 | 2026-11-21 | read |
| Document post (PDF carousel) | 1,080 x 1,350 px pages (studio choice); 300 pages at most | 4:5 | pdf | 100,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a518909 ; https://www.linkedin.com/help/linkedin/answer/a523054 | 2026-11-21 | read |
| Link preview | 1,200 x 627 px or larger | 1.91:1 | Not stated | 5,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a521928 | 2026-11-21 | read |
| Video post | The shared frames, 1,920 x 1,080 or 1,080 x 1,920 px (studio choice) | 16:9 or 9:16 | Not stated | 5,000,000,000 bytes | Not stated | Not stated | https://www.linkedin.com/help/linkedin/answer/a527229 | 2026-11-21 | search-result |

Notes:

- "Photo won't upload to your profile" (last updated 2 years ago): "Maximum file size is 8MB." Profile photo "between 400 (w) x 400 (h) pixels and 7680 (w) x 4320 (h) pixels". "File type must be PNG or JPG." "Add or change the cover image on your profile" (last updated 2 weeks ago; LinkedIn now calls the personal banner the "cover image"): "JPG or PNG file", "Lesser than 8MB", "1584 (w) x 396 (h) pixels (recommended)". "Your cover image appears behind your profile photo in the introduction section".
- "Image specifications for your LinkedIn Pages and Career Pages" (last updated 3 months ago): "All images must be PNG or JPEG files and have a maximum size of 3MB." Page logo: minimum 268 x 268, recommended 400 x 400. Page cover: 1512 x 256, both minimum and recommended. "You should place key details away from the edges of your cover photo, especially in the lower-right corner." "Your logo image will be displayed on both light and dark backgrounds. If your logo is transparent, it will be shown on a white background." A page post's link image: "Use a 1.91:1 ratio (1200 x 627 pixels)."
- "Share photos on LinkedIn": "The size limit for an upload is 5 MB." At least 552 x 276, "we recommend 1080 (w) pixels". "The photo's aspect ratio can range from 3:1 to 4:5 (width:height). If the ratio is larger, the image will be centered and cropped to fit the max ratio." Up to 20 photos; multi-photo posts "render a max ratio of 4:5". Each photo takes alt text.
- "Make your website shareable on LinkedIn": the link preview needs Open Graph tags, "Max file size: 5 MB", "Minimum image dimensions: 1200 (w) x 627 (h) pixels", "Recommended ratio: 1.91:1". The website's 1200 x 630 image meets it.
- "Upload and share documents on LinkedIn" (last updated 3 years ago): "The file size cannot exceed 100MB and 300 pages." PPT, PPTX, DOC, DOCX and PDF; "Convert files to PDFs whenever possible"; "PDFs with multiple layers must be flattened or merged"; "PDFs with multiple sized pages must be fit to the same page size." Members "will be able to download your document as a PDF". The page size of a document post is not stated; 1080 x 1350 px pages (4:5, the feed's tallest ratio) is the studio's choice.
- Video (search-result for "Share photos or videos", a527229): up to 5 GB, 3 seconds to 15 minutes from a computer and 10 minutes from the app. Captions: SRT upload on desktop for personal profiles and Pages, and auto captions (read; chapter 16 facts).
- Differences from the Gate 3 report: the company page cover is 1512 x 256 px, read today on LinkedIn's own page (search results still show older figures, 1128 x 191 and 4200 x 700, which LinkedIn's page no longer gives); the avatar's 400 x 400 is LinkedIn's minimum, with any larger square up to 7680 x 4320 accepted; the personal banner holds at 1584 x 396.

## 9. Print (chapters 24 and 25)

No platform governs print. The page sizes are the ones the Gate 3 report names, and the bleed is the studio's choice. Each piece states its trim size, its bleed and its margins; the printer named for a job may ask for a different bleed, and that printer's figure then governs.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Report page and one-page explainer, US Letter (the studio sample) | 8.5 x 11 in trim; 8.75 x 11.25 in with 0.125 in bleed (studio choice) | 17:22 | pdf | Not stated | Bleed 0.125 in each side, trimmed off (studio choice); margins set in each chapter | Not stated | Gate 3 report, section 9 (chapters 24 and 25) | 2026-11-21 | not-found |
| Letterhead, US Letter | 8.5 x 11 in trim; 0.125 in bleed (studio choice) | 17:22 | pdf | Not stated | Bleed 0.125 in each side (studio choice); margins set in each chapter | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |
| Event poster | 24 x 36 in trim; 0.125 in bleed (studio choice) | 2:3 | pdf | Not stated | Bleed 0.125 in each side (studio choice); margins set in each chapter | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |
| Table sign | 11 x 17 in trim; 0.125 in bleed (studio choice) | 11:17 | pdf | Not stated | Bleed 0.125 in each side (studio choice); margins set in each chapter | Not stated | Gate 3 report, section 9 (chapter 25) | 2026-11-21 | not-found |

Notes:

- Bleed: 0.125 in on every side, the studio's choice, so a Letter page with bleed measures 8.75 x 11.25 in. A PDF export carries the trim size as its TrimBox and the bleed size as its BleedBox.
- Margins are set in each chapter's own layout rules; this file records only the page.
- Difference from the Gate 3 report: none. Microsoft's slide-size page (read) names "Letter Paper (8.5x11 in)" among PowerPoint's page options, the one official page read today that states the Letter size.

## 10. Slides (chapter 25)

Slide layouts export as PDF and PNG at 1920 x 1080 with a PowerPoint file beside them (P4-2). The pixel size is the studio's.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Slide (cover, content, data) | 1,920 x 1,080 px (studio choice) | 16:9 | pdf, png, pptx | Not stated | Not stated | Not stated | Gate 3 report, section 10, P4-2 (G3-08) | 2026-11-21 | not-found |
| PowerPoint widescreen page | 13.333 x 7.5 in | 16:9 | pptx | Not stated | Not stated | Not stated | https://support.microsoft.com/en-us/office/change-the-size-of-your-slides-040a811c-be43-40b9-8d04-0de5ed79987e | 2026-11-21 | read |

## 11. Shared video frames (chapters 16 and 23)

The video frames serve YouTube, TikTok, Instagram Reels and LinkedIn video at 1920 x 1080 and 1080 x 1920. Their caption-safe areas combine the platform figures above, taking the larger margin on each side; the combination is the studio's.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| Video frame, landscape (title, end, chart and host frames) | 1,920 x 1,080 px (studio choice) | 16:9 | Not stated | Not stated | Not stated by any platform; chapter 23 sets it | Not stated | https://support.google.com/youtube/answer/6375112 | 2026-11-21 | read |
| Video frame, vertical | 1,080 x 1,920 px (studio choice) | 9:16 | Not stated | Not stated | Top 269, sides 120, bottom 672 px clear, and x 780 to 960 from y 840 down | Not stated | https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads ; https://www.facebook.com/business/ads-guide/update/image/instagram-reels | 2026-11-21 | read |

Notes:

- Vertical: top 269 px (Instagram's 14 percent), sides 120 px (TikTok), bottom 672 px (Instagram's 35 percent), and TikTok's button column, x 780 to 960 from y 840 down. A burned-in caption line sits inside this area; the closed caption file stays the primary caption (chapter 16 facts, WCAG 2.2's 1.2.2).
- Landscape: no platform page read states a caption-safe area for 16:9. YouTube's player draws its controls and end-screen elements over the frame and states no fixed zone, so chapter 23 sets the landscape margins as the studio's and tests them by capture.

## 12. Email (chapter 22)

No mail program publishes a body width, and no Google page found states Gmail's clipping size. The rows say where each figure comes from.

| Application | Size | Ratio | Type | Limit | Safe area or crop | Smallest shown | Source page | Checked | Status |
|---|---|---|---|---|---|---|---|---|---|
| HTML email body | 600 px wide at most (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | https://mailchimp.com/help/about-template-widths/ ; https://mailchimp.com/help/about-html-email/ | 2026-11-21 | read |
| Email phone check | 375 px wide (studio choice) | Not stated | Not stated | Not stated | Not stated | Not stated | Gate 3 report, section 9 | 2026-11-21 | not-found |
| Gmail's clipping size for one message | Not a size | Not stated | Not stated | About 102 KB (Substack's figure; no Google page) | Not stated | Not stated | No Google page found; figure from https://support.substack.com/hc/en-us/articles/360038866571 (read) | 2026-11-21 | not-found |

Notes:

- Body width: Mailchimp's help page "About Email Template Widths" (read): "Mailchimp templates are designed to be no greater than 600px wide to fit the display capabilities of most email clients." Its page "About HTML Email" (read): "Set email width to 600px or less." This is an email service's guidance and the common norm; no standard governs it.
- Gmail's clipping size: no Google help page found states it (searched support.google.com and Google's developer pages). Substack's help page "Why does it say 'Your post may be truncated'" (edited 2026-09-29, read) says "Gmail clips emails larger than about 102KB" and that "Links, images, and any text your publication adds to the top or bottom of every email all count toward the size." The figure is Substack's statement about Gmail, recorded as such. The studio keeps the working email's HTML well under it and reads 102 KB as 102,000 bytes.
- Check widths: the working email is checked at 600 and 375 px (Gate 3 report), the second being the studio's phone width.
- Difference from the Gate 3 report: none; the report asked the research lead to confirm Gmail's limit, and no Google page confirms it.

## Could not verify

Every row not marked read, with what stands in for the official page.

- `website.x_card` (search-result): Largest 4096 x 4096. X's stated minimum, 300 x 157, is not exactly 2:1; it is recorded as stated. Only the first frame of an animated GIF shows, per the search result. Not an export target: the website's 1200 x 630 image serves, and X crops it to 2:1. Source: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image (now redirects to https://docs.x.com/overview)
- `website.favicon_ico` (not-found, studio choice): Studio choice: 16, 32 and 48 px inside one ICO. The HTML standard says a browser may request /favicon.ico when no icon is named, and sets no size. Source: https://html.spec.whatwg.org/multipage/links.html#rel-icon
- `website.page_1440` (not-found, studio choice): The guide's own test width. No platform governs. Source: Gate 3 report, section 9 (work/ledger/20261120_Gate-3-Report.md)
- `website.page_1024` (not-found, studio choice): The guide's own test width. Source: Gate 3 report, section 9
- `website.page_390` (not-found, studio choice): The guide's own test width. Source: Gate 3 report, section 9
- `website.page_360` (not-found, studio choice): The guide's own test width. Source: Gate 3 report, section 9
- `substack.body_width` (not-found): Measure on a published post in chat 13 and record as the studio's measurement. Source: No Substack help page states it (searched support.substack.com, November 21, 2026)
- `instagram.avatar` (not-found, studio choice): Upload size is the studio's. The app shows it in a circle; keep the mark inside the inscribed circle. Source: No Instagram page found; https://www.facebook.com/help/125379114252045 gives 320 x 320 for Facebook Pages only
- `instagram.square` (search-result): Width 1080 from the help page (search-result). The publishing page (read) allows JPEG up to 8 MB, 320 to 1440 px wide. Source: https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
- `instagram.portrait` (search-result): 4:5 is inside every version of the help page and the publishing page's 4:5 to 1.91:1 range (read). The safe box is the studio's: the center 3:4 crop the grid may take. Source: https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-feed
- `instagram.portrait_3x4` (search-result): One version of the help page allows 3:4; the publishing page (read) does not. Do not build to it until it is confirmed. Source: https://help.instagram.com/1631821640426723
- `instagram.landscape` (search-result): 1.91:1 is the wide limit in the help page and the publishing page. Source: https://help.instagram.com/1631821640426723 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
- `instagram.carousel` (search-result): Every item in a post takes the one orientation chosen for it (help page "Crop your photo on Instagram", search-result). The studio builds carousels at 4:5. Source: https://help.instagram.com/1631821640426723 ; https://help.instagram.com/117838865078314/
- `instagram.grid` (not-found): Reported as 3:4 by Kapwing and 4:5 by the Inquirer; Substack's page says 4:5. Unconfirmed. Source: No Instagram or Meta page found; leads: press reports of January 2025
- `instagram.story` (search-result): 9:16 recommended by the publishing page (read); 1080 x 1920 from an older Instagram creator page (search-result). Safe zones from Meta's ads guide (read): 14 percent top, 35 percent bottom, 6 percent each side. Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-story
- `instagram.reel` (search-result): Help page (search-result): 1.91:1 to 9:16, at least 720 px and 30 fps. Publishing page (read): up to 1920 px across, 300 MB, 3 seconds to 15 minutes. Safe zones from the ads guide (read). Source: https://help.instagram.com/1038071743007909 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media ; https://www.facebook.com/business/ads-guide/update/image/instagram-reels
- `instagram.reel_cover` (search-result, studio choice): The help page recommends 420 x 654 (1:1.55) (search-result). The publishing page (read) recommends 9:16 and crops "the middle most 9:16 rectangle". The studio builds the cover at 1080 x 1920 with its words inside the center 1080 x 1676 (the 1:1.55 crop) and inside the reel's safe zone. Source: https://help.instagram.com/1038071743007909 ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
- `threads.avatar` (not-found, studio choice): Shared with Instagram's avatar. Source: No Threads page found
- `threads.link_preview` (not-found, studio choice): Uses the website's Open Graph image. Source: No Threads page found
- `x.avatar` (search-result): No animated GIF. Shown in a circle. Source: https://help.x.com/en/managing-your-account/how-to-customize-your-profile ; https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo
- `x.header` (search-result): About 60 px at the top and bottom may be cropped by screen and browser (search-result). The profile photo sits over the lower left of the header; its exact footprint is not stated and is measured by capture in chapter 23. Source: https://help.x.com/en/managing-your-account/how-to-customize-your-profile
- `x.post_image` (search-result, studio choice): X shows a single photo whole between 2:1 and 3:4 (search-result); 1600 x 900 is the studio's starting size inside that range. 5 MB and the four formats are read on docs.x.com. Source: https://help.x.com/en/using-x/posting-gifs-and-pictures ; https://docs.x.com/x-api/media/quickstart/best-practices
- `x.post_four` (not-found): Up to four photos a post (read on docs.x.com). How the grid crops them is not stated. Source: https://help.x.com/en/using-x/posting-gifs-and-pictures
- `x.link_card` (search-result, studio choice): The website's share image (website.share_preview) through the summary_large_image card. Source: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image
- `tiktok.avatar` (not-found, studio choice): No organic size found. Ads profile photo: 98 x 98 px, key element in the center 66 x 66. The studio's safe box keeps that proportion at 1080. Source: https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads (ads profile photo only)
- `tiktok.cover` (not-found, studio choice): Chosen in the app from the video; size not stated. Build it as a frame of the video, inside the video's safe zone. Source: No TikTok page found
- `linkedin.video` (search-result, studio choice): 5 GB; 3 seconds to 15 minutes from a computer (search-result). The shared video frames serve (section 11). Source: https://www.linkedin.com/help/linkedin/answer/a527229
- `print.letter` (not-found, studio choice): Trim 8.5 x 11 in; bleed 0.125 in each side (studio choice), so the bleed box is 8.75 x 11.25 in. Source: Gate 3 report, section 9 (chapters 24 and 25)
- `print.letterhead` (not-found, studio choice): As print.letter. Source: Gate 3 report, section 9 (chapter 25)
- `print.poster` (not-found, studio choice): Trim 24 x 36 in; 0.125 in bleed (studio choice). Source: Gate 3 report, section 9 (chapter 25)
- `print.table_sign` (not-found, studio choice): Trim 11 x 17 in; 0.125 in bleed (studio choice). Source: Gate 3 report, section 9 (chapter 25)
- `slides.layout` (not-found, studio choice): The studio's export size. PowerPoint's own widescreen page is the row below. Source: Gate 3 report, section 10, P4-2 (G3-08)
- `email.phone_check` (not-found, studio choice): The studio's phone width for the check. Source: Gate 3 report, section 9
- `email.gmail_clip` (not-found): "Gmail clips emails larger than about 102KB" (Substack). The whole message's HTML counts. Source: No Google page found; figure from https://support.substack.com/hc/en-us/articles/360038866571 (read)
