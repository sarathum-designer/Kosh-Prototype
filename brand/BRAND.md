Kosh is the neutral record of India's GCC ecosystem. *Kosh* is Sanskrit for a treasury, the place where valuables are kept safe and counted. The brand has to look like that: calm, exact, a little archival, and never like a sales brochure.

## The idea: the Source Dot

Every fact in Kosh carries a dot. The dot says *this came from somewhere, and you can check it.* The same dot sits inside the **o** of the wordmark. It is the one piece of the identity people should remember.

- A filled `vermilion` dot (`radius-full`, 6–8px) after a number means it is sourced. Click or hover shows the source, date and confidence.
- A `verified` dot means two or more independent sources agree.
- A split dot in `conflict` means sources disagree. Kosh shows both values rather than picking one.
- A hollow `stale` dot means a single source or data older than 12 months.
- Status never rides on colour alone: every dot has a word next to it (Verified, Conflict, Single source, Dated) or a tooltip with the source.

## Why it looks like this

Every other player in this market (Big 4, GCC advisors, research houses, state investment portals) uses corporate blue, stock photos of glass towers and handshake imagery. Kosh is paper, ink and one warm red. It reads like a ledger or a well-kept archive, which is the promise: a record, not a pitch.

## Logo

- `kosh-wordmark.svg` is the primary logo: ink letters, vermilion dot. Use it on `paper` and `paper-raised`.
- `kosh-wordmark-reversed.svg` is for dark grounds (`paper` in the Ink theme, photos, video).
- `kosh-wordmark-mono.svg` is for one-colour print, embossing, fax-grade documents and legal letterheads.
- `kosh-mark.svg` (ring and dot) is the short form for favicons, avatars, the loading state and the Source Dot itself at large sizes.
- `kosh-app-icon.svg` is the vermilion tile for app stores and social profiles.
- Clear space around the logo equals the height of the **o**. Minimum width: 64px digital, 18mm print.
- Never recolour the letters vermilion, never put the wordmark on a vermilion field (use the app icon instead), never add effects, never retype the wordmark in a font. It is drawn, not set.

## Colour

Paper and ink do 90% of the work. Vermilion is spent like money.

- Ground every page with `paper`; put cards on `paper-raised`; set text in `ink` and `ink-muted`.
- Use `vermilion` for one thing per screen or slide: the primary action, the highlighted number, or the Source Dot. If two things are vermilion, one of them is wrong.
- `vermilion` on light is a fill or mark only (3.2:1). For red text use `vermilion-text`. Text on a vermilion fill is `on-vermilion` (ink), never white.
- `verified`, `conflict` and `stale` are statuses, not decoration. Do not use them for brand moments.
- In charts, the first series is `vermilion`, the second `indigo`, everything else `ink-muted` and `line-strong` greys.
- No gradients, no shadows, no glass. Separate with `line` hairlines.

## Type

- **Instrument Serif** (`statement-xl`, `statement`) for the one big claim on a slide or hero. Regular weight only, sentence case, no full stop on single-line headlines unless it is a full sentence.
- **Geist** (`display`, `heading`, `body`, `label`) for the product and all running text.
- **Geist Mono** (`figure`, `source`) for numbers, dates and sources. Numbers are the hero of this brand, so they get their own face.
- All three are free Google Fonts. Load them from fonts.googleapis.com; fall back to Inter / Georgia / Menlo.

## Voice

Kosh talks like a careful analyst who has nothing to sell you.

- Lead with the number, then the source. "Karnataka reimburses 50% of rent for three years. Source: Karnataka GCC Policy 2024–29."
- Say when we don't know. "We have no verified figure for Indore rents yet" beats a guess.
- Show disagreement plainly. "Nasscom-Zinnov counts 2,117 GCCs; EY counts 1,700. The gap is mostly definition: companies versus centres."
- Short sentences, plain words, second person ("you"), sentence case everywhere. No exclamation marks, no emoji, no "unlock", "seamless", "revolutionise" or "game-changer".
- Never rank, recommend or praise a provider in our own voice. Kosh reports what they delivered and what clients said.

## Layout and spacing

- 8px base grid: `space-1` to `space-12`. Card padding `space-6` desktop, `space-4` phone.
- Generous margins, left-aligned text, one idea per slide.
- `radius-md` for buttons and cards, `radius-sm` for chips and inputs. The only round things are dots.
- Focus ring: a solid 2px `focus` outline, offset 2px.

## Iconography and imagery

- Line icons at 1.5px stroke (Lucide), drawn in `ink` or `ink-muted`. Never filled, never coloured except the Source Dot.
- Imagery is maps, floor plates, filings and charts drawn in the palette. No stock photography of people, skylines or handshakes.
- Maps: land in `paper-sunk`, borders in `line`, the city in focus as a vermilion dot.

## Applying it

- **Product:** `paper` ground, `paper-raised` cards, one vermilion primary button per view, Source Dots on every number.
- **Deck:** one statement per slide in `statement-xl`, figures in `figure`, source line in `source` at the foot of every slide that shows data.
- **Documents and legal:** mono wordmark top-left, Geist body, Geist Mono for clause numbers and dates.
