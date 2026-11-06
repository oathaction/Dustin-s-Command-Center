// Oath & Action design tokens, Edition 06: the one source of truth.
//
// work/build/scripts/phase-2/tokens_build.mjs reads this module and writes
//   work/build/tokens/tokens.json   (DTCG Format Module 2025.10)
//   work/build/tokens/tokens.css    (custom properties, surface classes, reduced motion)
// Edit this file, never the outputs. The token tests fail when the outputs and this source disagree.
//
// The source states recipes, not results. A derived color is written as the palette color it starts
// from, the color it mixes toward and the amount (OKLab, D1-04); the generator computes the hex, the
// sRGB components and every contrast ratio. Sizes are written in the units the brand sets them in,
// and the generator writes rem, clamp() and em values. So no computed number is typed here by hand.
//
// Spec: work/ledger/20261021_Token-Architecture.md (T-1 to T-11, approved at Gate 1, G1-03 T5).
// Later decisions that change it are cited beside the token they touch.

// ------------------------------------------------------------------------------------------ helpers
// Tagged recipes. The generator turns each into a DTCG value.
const ref = (path) => ({ $kind: 'ref', path });
const P = (name) => ref(`oa.color.palette.${name}`);
const D = (name) => ref(`oa.color.derived.${name}`);
const T = (name) => ref(`oa.color.tint.${name}`);
const hex = (h) => ({ $kind: 'hex', hex: h });
const mix = (base, toward, amount) => ({ $kind: 'mix', base, toward, amount });
const px = (value) => ({ $kind: 'dim', value, unit: 'px' });
const rem = (value) => ({ $kind: 'dim', value, unit: 'rem' });
const ms = (value) => ({ $kind: 'duration', value, unit: 'ms' });

// One token. `ext` lands in $extensions["org.oathandaction"].
const tok = ($type, $value, $description, ext = {}) => ({ $type, $value, $description, ext });

// A semantic or component color role on several surfaces. `map` names the value per surface;
// surfaces left out get no token (for example, no red token on Prussian).
const SURFACE_KEY = { newsprint: 'onNewsprint', white: 'onWhite', charcoal: 'onCharcoal', prussian: 'onPrussian' };
function onSurfaces(description, ext, map, perSurface = {}) {
  const group = {};
  for (const [surface, value] of Object.entries(map)) {
    group[SURFACE_KEY[surface]] = tok('color', value, description, { ...ext, surface, ...(perSurface[surface] || {}) });
  }
  return group;
}
const semantic = (kind, job, map, perSurface) => onSurfaces(job, { tier: 'semantic', kind }, map, perSurface);
const component = (job, map, perSurface) => onSurfaces(job, { tier: 'component' }, map, perSurface);

// Chart sizes keep a pointer to the build-script key they came from, so the chart kit can map them.
const chartDim = (value, description, source, ext = {}) => tok('dimension', px(value), description, { source, ...ext });
const chartNum = (value, unit, description, source, ext = {}) => tok('number', value, description, { unit, source, ...ext });

// ------------------------------------------------------------------------------------------ metadata
export const meta = {
  title: 'Oath & Action design tokens, Edition 06',
  version: '6.0.0-gate2.1',
  status: 'pre-release',
  statusNote:
    'Built for Gate 2. Version 6.0.0 ships when Dustin approves the token files at Gate 2; until then every value may still change.',
  formatVersion: '2025.10',
  formatReference: 'https://www.designtokens.org/TR/2025.10/format/',
  colorReference: 'https://www.designtokens.org/TR/2025.10/color/',
  namespace: 'org.oathandaction',
  namespaceNote:
    'Reverse-domain key from oathandaction.org as written in V5 (D1-06); ownership is unconfirmed, so the key can change before Phase 5',
  source: 'work/build/tokens/src/oa-tokens.src.mjs',
  generator: 'work/build/scripts/phase-2/tokens_build.mjs',
  spec: 'work/ledger/20261021_Token-Architecture.md',
  surfaces: ['newsprint', 'white', 'charcoal', 'prussian'],
  chartGrounds: ['newsprint', 'charcoal'],
  chartGroundNote:
    'Charts and the atlas sit on Newsprint (DR-53); Charcoal is the dark ground (DR-50). Chart tokens exist for these two grounds only.',
  fluidRange: { minViewportPx: 390, maxViewportPx: 1440 },
  remBasePx: 16,
  fontSizeFloorPx: 13,
  fontSizeExceptions: [],
  cssNaming:
    'Prefix --oa-, path segments in kebab case, the surface last: oa.color.text.secondary.onNewsprint becomes --oa-color-text-secondary-on-newsprint',
};

// The register of measured needs (condition 1 of the rule for adding a token).
export const needs = {
  'N-01':
    'Secondary small text on Newsprint: Stone measures 4.29:1; 49 Stone-on-Newsprint text failures in the V5 census; Concepts V2 already uses #4E535C 1,606 times',
  'N-02': 'Secondary text on Charcoal and Prussian: Stone measures 3.10:1 and 2.20:1; 8 failures in the V5 census',
  'N-03':
    'Error message ground that holds 13 px text: Charcoal on Pillar Red is 4.49:1 and White on Pillar Red 4.17:1',
  'N-05':
    'Chart structure that recedes behind the data (gridlines, tracks, bands, light fills, map land): no palette color sits between a ground and Stone. Measured in the Explainer system (DR-52) and the palette lab (D2-95)',
  'N-06':
    'Context marks on Charcoal one step quieter than secondary text: Dim Newsprint carries secondary text there at 7.26:1, so context lines need their own ink (Explainer dark view, palette lab "Context, quieter" at 5.41:1)',
  'N-07':
    'Diverging pair B (DR-54) needs a light step on each side and a midpoint tinted toward the ground; no palette color supplies them',
  'N-08':
    'One-sided magnitude scales (S16 turnout in the stretch test, approved with Board 4 under DR-62) need five ordered Verdigris steps per ground',
  'N-09':
    'Phone tile maps of shifts draw gray steps by size (DR-64): four ordered Stone steps per ground, each holding a 4.5:1 label',
};

// Values registered at Gate 1 that are not tokens. They stay out of tokens.json and tokens.css.
export const held = {
  verdigrisOnDark: {
    hex: '#59857D',
    derivation: 'Verdigris 10% toward Newsprint in OKLab',
    need: 'N-04',
    needText: 'Verdigris status marks on Prussian measure 2.80:1',
    status: 'held',
    reason: 'Success on Prussian takes Newsprint (section 4), so no token needs this value; it waits for the Signal Grid chapter',
  },
  redInk: { hex: '#AC3339', status: 'rejected', reason: 'T-6: no small red text and no derived red' },
  redGraphic: { hex: '#DA3843', status: 'rejected', reason: 'T-6: a second red that looks like the first' },
  divergingA: {
    status: 'not adopted',
    reason:
      'Explainer drew S06 in diverging A (Stone to Verdigris); DR-54 picked pair B, and the creative director\'s finishing list redraws S06 in pair B',
  },
};

// Rule 05.3, word for word: D2-01 as amended by DR-66.
export const redRule = {
  id: 'Rule 05.3',
  text:
    "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one keeps its red, and that red counts as signature red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.",
  source: 'work/ledger/20261020_Decision-Log.md, D2-01 with the sentence DR-66 approved',
  precedence: { 1: 'an error the reader must fix', 2: 'the step a reader can take now', 3: 'the one point the headline names' },
};

export const chartRules = {
  party: 'Party marks take neutral inks with the party named on the mark. Pillar Red and Prussian never mark a party, and no two parties get a color pair (DR-48, DR-58).',
  diverging: 'The diverging scale is pair B, Prussian through the page color to Verdigris, with a boxed arrow or a printed sign carrying direction (DR-54). No diverging scale pairs red with blue (Master Brief V2 section 13).',
  red: 'Data reaches red only through oa.color.data.emphasisRed, the third claim on the view\'s working red (Rule 05.3).',
};

// ------------------------------------------------------------------------------------------ the token tree
const SURF4 = ['newsprint', 'white', 'charcoal', 'prussian'];
const light = (a, b) => ({ newsprint: a, white: a, charcoal: b, prussian: b });

const palette = {
  newsprint: tok('color', hex('#DCD9D2'), 'Newsprint, the default reading surface and the page color for charts and the atlas (DR-53).',
    { tier: 'primitive', status: 'locked', job: 'Default reading surface', lockedIn: 'Master Brief V2 section 3' }),
  charcoal: tok('color', hex('#121212'), 'Charcoal, primary text on light surfaces and the dark ground.',
    { tier: 'primitive', status: 'locked', job: 'Primary text on light surfaces and the dark ground', lockedIn: 'Master Brief V2 section 3' }),
  pillarRed: tok('color', hex('#E63946'), 'Pillar Red: signature red in identity marks, and the one working red each view may carry (Rule 05.3).',
    { tier: 'primitive', status: 'locked', job: 'Signature red and the one working red per view', lockedIn: 'Master Brief V2 section 3' }),
  prussian: tok('color', hex('#1F2D5A'), 'Prussian, the depth surface for panels and explainers. Red never sits on it.',
    { tier: 'primitive', status: 'locked', job: 'Depth surface for panels and explainers', lockedIn: 'Master Brief V2 section 3' }),
  stone: tok('color', hex('#5D636D'), 'Stone, hairlines, structure and context marks. Too light for small text on Newsprint (4.29:1).',
    { tier: 'primitive', status: 'locked', job: 'Hairlines, structure and context marks', lockedIn: 'Master Brief V2 section 3' }),
  verdigris: tok('color', hex('#4A7C74'), 'Verdigris, success marks and the focus ring on light surfaces.',
    { tier: 'primitive', status: 'locked', job: 'Success marks and focus on light surfaces', lockedIn: 'Master Brief V2 section 3' }),
  white: tok('color', hex('#FFFFFF'), 'White, the bright surface, reversed text and neutral production.',
    { tier: 'primitive', status: 'locked', job: 'Bright surface and reversed text', lockedIn: 'Master Brief V2 section 3' }),
};

// Derived colors adopted at Gate 1 (T-4, T-5).
const derived = {
  deepStone: tok('color', mix('stone', 'charcoal', 0.18),
    'Deep Stone, secondary and disabled text on Newsprint and White. Stone mixed 18% toward Charcoal in OKLab (T-4).',
    { tier: 'primitive', status: 'adopted', job: 'Secondary and disabled text on Newsprint and White', kind: 'text',
      surfaces: ['newsprint', 'white'], need: 'N-01', gate: 'Gate 1, T-4' }),
  dimNewsprint: tok('color', mix('newsprint', 'charcoal', 0.25),
    'Dim Newsprint, secondary and disabled text on Charcoal and Prussian. Newsprint mixed 25% toward Charcoal in OKLab (T-5).',
    { tier: 'primitive', status: 'adopted', job: 'Secondary and disabled text on Charcoal and Prussian', kind: 'text',
      surfaces: ['charcoal', 'prussian'], need: 'N-02', gate: 'Gate 1, T-5' }),
  errorBand: tok('color', mix('pillarRed', 'newsprint', 0.88),
    'Error Band, the ground of an error message on Newsprint and White. Pillar Red mixed 88% toward Newsprint in OKLab (T-5).',
    { tier: 'primitive', status: 'adopted', job: 'Ground of an error message on Newsprint and White', kind: 'background',
      surfaces: ['newsprint', 'white'], need: 'N-03', gate: 'Gate 1, T-5',
      textOnIt: ['{oa.color.palette.charcoal}', '{oa.color.derived.deepStone}'] }),
};

// Chart tints: OKLab mixes from the Explainer system, the stretch test and the palette lab.
// Names give the recipe: stoneN55 is Stone mixed 55% toward Newsprint; stoneC45 is Stone 45% toward
// Charcoal; p stands for a decimal point (verdigrisN52p75 is 52.75%).
function tint(name, base, toward, amount, job, kind, surfaces, need, from) {
  return [name, tok('color', mix(base, toward, amount), `${job}.`, {
    tier: 'primitive', status: 'adopted', job, kind, surfaces, need, from })];
}
const tints = Object.fromEntries([
  tint('stoneN55', 'stone', 'newsprint', 0.55, 'Light Stone fill for a category under the subject, with its value printed', 'dataFill', ['newsprint'], 'N-05', 'Explainer lt; palette lab'),
  tint('stoneN70', 'stone', 'newsprint', 0.70, 'Gridline on Newsprint', 'decorative', ['newsprint'], 'N-05', 'Explainer grid; palette lab'),
  tint('stoneN88', 'stone', 'newsprint', 0.88, 'Track on Newsprint, the whole a share sits in', 'decorative', ['newsprint'], 'N-05', 'Explainer lt2'),
  tint('stoneN90', 'stone', 'newsprint', 0.90, 'Midpoint of diverging pair B on Newsprint', 'dataFill', ['newsprint'], 'N-07', 'Palette lab, diverging B'),
  tint('stoneN35', 'stone', 'newsprint', 0.35, 'Context marks on Charcoal, one step quieter than secondary text', 'graphic', ['charcoal'], 'N-06', 'Explainer dark ctx; palette lab'),
  tint('stoneN85', 'stone', 'newsprint', 0.85, 'Largest gray step of a phone tile map on Charcoal', 'dataFill', ['charcoal'], 'N-09', 'Stretch S12 phone step'),
  tint('stoneC10', 'stone', 'charcoal', 0.10, 'Third gray step of a phone tile map on Newsprint', 'dataFill', ['newsprint'], 'N-09', 'Stretch S12 phone step'),
  tint('stoneC40', 'stone', 'charcoal', 0.40, 'Second gray step of a phone tile map on Charcoal', 'dataFill', ['charcoal'], 'N-09', 'Stretch S12 phone step'),
  tint('stoneC45', 'stone', 'charcoal', 0.45, 'Gridline on Charcoal', 'decorative', ['charcoal'], 'N-05', 'Explainer dark grid; palette lab'),
  tint('stoneC55', 'stone', 'charcoal', 0.55, 'Track on Charcoal, the whole a share sits in', 'decorative', ['charcoal'], 'N-05', 'Explainer dark lt2'),
  tint('stoneC60', 'stone', 'charcoal', 0.60, 'Largest gray step of a phone tile map on Newsprint', 'dataFill', ['newsprint'], 'N-09', 'Stretch S12 phone step'),
  tint('stoneC72', 'stone', 'charcoal', 0.72, 'Band on Charcoal, a stretch of time a note names', 'decorative', ['charcoal'], 'N-05', 'Explainer dark band'),
  tint('stoneC75', 'stone', 'charcoal', 0.75, 'Smallest gray step of a phone tile map on Charcoal', 'dataFill', ['charcoal'], 'N-09', 'Stretch S12 phone step'),
  tint('stoneC80', 'stone', 'charcoal', 0.80, 'Map land on Charcoal', 'decorative', ['charcoal'], 'N-05', 'Stretch land, dark'),
  // Explainer writes "Newsprint 45% toward White"; OKLab mixing is linear, so that is White 55% toward Newsprint, the form D1-04 allows.
  tint('whiteN55', 'white', 'newsprint', 0.55, 'Band and map land on Newsprint, lighter than the page', 'decorative', ['newsprint'], 'N-05', 'Explainer band; stretch land'),
  tint('prussianN62', 'prussian', 'newsprint', 0.62, 'Light Prussian step of diverging pair B on Newsprint', 'dataFill', ['newsprint'], 'N-07', 'Palette lab, diverging B'),
  tint('verdigrisN55', 'verdigris', 'newsprint', 0.55, 'Light Verdigris step: pair B on Newsprint and the top sequential step on Charcoal', 'dataFill', ['newsprint', 'charcoal'], 'N-07', 'Palette lab, diverging B and sequential on Charcoal'),
  tint('verdigrisC25', 'verdigris', 'charcoal', 0.25, 'Strong Verdigris end of diverging pair B on Newsprint', 'dataFill', ['newsprint'], 'N-07', 'Palette lab, diverging B'),
  tint('verdigrisN82', 'verdigris', 'newsprint', 0.82, 'First sequential Verdigris step on Newsprint', 'dataFill', ['newsprint'], 'N-08', 'Palette lab sequential; stretch q1'),
  tint('verdigrisN52p75', 'verdigris', 'newsprint', 0.5275, 'Second sequential Verdigris step on Newsprint', 'dataFill', ['newsprint'], 'N-08', 'Palette lab sequential; stretch q2'),
  tint('verdigrisN23p5', 'verdigris', 'newsprint', 0.235, 'Third sequential Verdigris step on Newsprint', 'dataFill', ['newsprint'], 'N-08', 'Palette lab sequential; stretch q3'),
  tint('verdigrisC5p75', 'verdigris', 'charcoal', 0.0575, 'Fourth sequential Verdigris step on Newsprint', 'dataFill', ['newsprint'], 'N-08', 'Palette lab sequential; stretch q4'),
  tint('verdigrisC35', 'verdigris', 'charcoal', 0.35, 'Fifth sequential Verdigris step and the circle outline on Newsprint', 'dataFill', ['newsprint'], 'N-08', 'Palette lab sequential; stretch q5 and qk'),
  tint('verdigrisC75', 'verdigris', 'charcoal', 0.75, 'First sequential Verdigris step on Charcoal', 'dataFill', ['charcoal'], 'N-08', 'Palette lab sequential on Charcoal'),
  tint('verdigrisC50', 'verdigris', 'charcoal', 0.50, 'Second sequential Verdigris step on Charcoal', 'dataFill', ['charcoal'], 'N-08', 'Palette lab sequential on Charcoal'),
  tint('verdigrisC20', 'verdigris', 'charcoal', 0.20, 'Third sequential Verdigris step on Charcoal', 'dataFill', ['charcoal'], 'N-08', 'Palette lab sequential on Charcoal'),
  tint('verdigrisN25', 'verdigris', 'newsprint', 0.25, 'Fourth sequential Verdigris step on Charcoal', 'dataFill', ['charcoal'], 'N-08', 'Palette lab sequential on Charcoal'),
]);

const color = {
  $description: 'Identity, state and data color. Identity marks use palette colors only; tints serve data scales, state grounds and chart structure.',
  palette,
  derived,
  tint: { $description: 'OKLab mixes of one palette color toward Newsprint or Charcoal, each with a registered need. Chart structure, data scales and dark-ground context.', ...tints },
  surface: Object.fromEntries(SURF4.map((s) => [s, tok('color', P(s), `The ${s[0].toUpperCase() + s.slice(1)} surface: the ground every other ${s} token is measured on.`, { tier: 'semantic', kind: 'surface', surface: s })])),
  text: {
    primary: semantic('text', 'Body text, headings and data values.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') }),
    secondary: semantic('text', 'Captions, metadata, labels, source lines and disabled text.', { ...light(D('deepStone'), D('dimNewsprint')) }),
  },
  graphic: {
    essential: semantic('graphic', 'Marks a reader needs: icons, diagram strokes, lit Signal Grid nodes.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('newsprint') }),
    subtle: semantic('graphic', 'Marks that support: unlit nodes, secondary diagram strokes.', { newsprint: P('stone'), white: P('stone'), charcoal: D('dimNewsprint'), prussian: D('dimNewsprint') }),
  },
  border: {
    strong: semantic('graphic', 'Edges of inputs and controls that a reader must find, and the keyline on a red mark.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('newsprint') }),
    hairline: semantic('decorative', 'Dividers and table rules with no meaning of their own.', { newsprint: P('stone'), white: P('stone'), charcoal: P('stone'), prussian: P('white') }),
  },
  focus: {
    ring: semantic('focus', 'Keyboard focus outline, 2 px with a 2 px offset, shown at once.', { newsprint: P('verdigris'), white: P('verdigris'), charcoal: P('newsprint'), prussian: P('newsprint') }),
  },
  identity: {
    signature: semantic('logotype',
      'Signature red: the wordmark ampersand, the lockmark lever, the ampersands in the hinge diagram and the hinge-circle badge, and a standalone icon\'s accent. It does not count against the view\'s working red (Rule 05.3). White on Prussian, treatment D.',
      { newsprint: P('pillarRed'), white: P('pillarRed'), charcoal: P('pillarRed'), prussian: P('white') },
      { newsprint: { redRole: 'signature' }, white: { redRole: 'signature' }, charcoal: { redRole: 'signature' } }),
    hingeDivider: semantic('graphic', 'The ampersand in the hinge divider takes its surface\'s ink and is never red (Rule 05.3).',
      { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') }),
  },
  action: {
    ask: {
      fill: semantic('graphic', 'Ask button fill: the step a reader can take now, the second claim on the view\'s working red. On Newsprint it takes a 1 px Charcoal keyline.',
        { newsprint: P('pillarRed'), white: P('pillarRed'), charcoal: P('pillarRed'), prussian: P('newsprint') },
        { newsprint: { redRole: 'working', precedence: 2, keyline: '{oa.color.palette.charcoal}' },
          white: { redRole: 'working', precedence: 2 }, charcoal: { redRole: 'working', precedence: 2 } }),
      label: semantic('largeText', 'Ask button label, White on Pillar Red, set in oa.type.ask at 19 px bold or larger (T-7).',
        { newsprint: P('white'), white: P('white'), charcoal: P('white'), prussian: P('charcoal') },
        Object.fromEntries(SURF4.map((s) => [s, { requiresType: '{oa.type.ask}', ground: `{oa.color.action.ask.fill.${SURFACE_KEY[s]}}` }]))),
    },
    primary: {
      fill: semantic('graphic', 'Primary button fill. It also carries the ask when an error holds the view\'s red.',
        { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('newsprint') }),
      fillHover: semantic('graphic', 'Primary button fill on hover: Charcoal steps to Prussian on light surfaces, Newsprint steps to White on dark ones. The label also underlines.',
        { newsprint: P('prussian'), white: P('prussian'), charcoal: P('white'), prussian: P('white') }),
      label: semantic('text', 'Primary button label, on the fill and on the hover fill.',
        { newsprint: P('white'), white: P('white'), charcoal: P('charcoal'), prussian: P('charcoal') },
        Object.fromEntries(SURF4.map((s) => [s, { ground: `{oa.color.action.primary.fill.${SURFACE_KEY[s]}}`, groundsAlso: [`{oa.color.action.primary.fillHover.${SURFACE_KEY[s]}}`] }]))),
    },
  },
  state: {
    $description: 'Every state changes text or shape as well as color, and no state uses opacity (section 4).',
    muted: {
      text: semantic('text', 'Muted text, set in regular weight.', light(D('deepStone'), D('dimNewsprint'))),
      mark: semantic('graphic', 'Muted marks, drawn as outlines.', light(P('stone'), D('dimNewsprint'))),
    },
    disabled: {
      text: semantic('text', 'Disabled text. The control keeps focus with aria-disabled and a reason line says what will make it available.', light(D('deepStone'), D('dimNewsprint'))),
      edge: semantic('graphic', 'Disabled control edge, drawn dashed.', light(D('deepStone'), D('dimNewsprint')),
        Object.fromEntries(SURF4.map((s) => [s, { strokeStyle: 'dashed' }]))),
    },
    loading: {
      text: semantic('text', 'Loading text in a role="status" region, such as "Loading tracker".', light(D('deepStone'), D('dimNewsprint'))),
      mark: semantic('graphic', 'The still outline lever of the loading state. It never moves (T-10).', light(P('stone'), D('dimNewsprint')),
        Object.fromEntries(SURF4.map((s) => [s, { motion: 'none' }]))),
    },
    selected: {
      band: semantic('background', 'Ground of a selected row or option: the paired surface. Pair it with the 4 px bar and a check glyph.',
        { newsprint: P('white'), white: P('newsprint'), charcoal: P('prussian'), prussian: P('charcoal') },
        Object.fromEntries(SURF4.map((s) => [s, { textOnIt: [`{oa.color.text.primary.${SURFACE_KEY[s]}}`, `{oa.color.text.secondary.${SURFACE_KEY[s]}}`] }]))),
      bar: semantic('graphic', 'The 4 px bar beside a selected item, drawn on the selected band.',
        { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') },
        Object.fromEntries(SURF4.map((s) => [s, { ground: `{oa.color.state.selected.band.${SURFACE_KEY[s]}}` }]))),
    },
    warning: {
      mark: semantic('graphic', 'Warning triangle and 4 px bar. Warning has no hue of its own; the word "Warning" carries it.',
        { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('newsprint') }),
      text: semantic('text', 'Warning text, in primary ink.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') }),
    },
    error: {
      band: semantic('background', 'Ground of an error message on light surfaces. Pair it with the word "Error", the glyph and the fix in plain words.',
        { newsprint: D('errorBand'), white: D('errorBand') },
        { newsprint: { textOnIt: ['{oa.color.text.primary.onNewsprint}', '{oa.color.text.secondary.onNewsprint}'] },
          white: { textOnIt: ['{oa.color.text.primary.onWhite}', '{oa.color.text.secondary.onWhite}'] } }),
      mark: semantic('graphic', 'Error glyph and state bar: the first claim on the view\'s working red. Newsprint on Prussian, where red never sits.',
        { newsprint: P('pillarRed'), white: P('pillarRed'), charcoal: P('pillarRed'), prussian: P('newsprint') },
        { newsprint: { redRole: 'working', precedence: 1, keyline: '{oa.color.palette.charcoal}' },
          white: { redRole: 'working', precedence: 1 }, charcoal: { redRole: 'working', precedence: 1 } }),
      text: semantic('text', 'Error message text, in primary ink. Red never sets text.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') }),
    },
    empty: {
      text: semantic('text', 'Empty state text: what is missing and what to do next.', light(D('deepStone'), D('dimNewsprint'))),
      edge: semantic('graphic', 'Dashed edge of an empty region.', light(P('stone'), D('dimNewsprint')),
        Object.fromEntries(SURF4.map((s) => [s, { strokeStyle: 'dashed' }]))),
    },
    success: {
      mark: semantic('graphic', 'Success check glyph. Status never relies on red and Verdigris alone; a word such as "Saved" goes with it.',
        { newsprint: P('verdigris'), white: P('verdigris'), charcoal: P('verdigris'), prussian: P('newsprint') }),
      text: semantic('text', 'Success text, in primary ink.', { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('white') }),
    },
  },
  data: {
    $description: 'Data color on any surface. Data reaches red only through emphasisRed, the third claim on the view\'s working red.',
    emphasis: semantic('graphic', 'The mark the chart title is about, and every mark that stands for a party (neutral ink).',
      { newsprint: P('charcoal'), white: P('charcoal'), charcoal: P('newsprint'), prussian: P('newsprint') }),
    // DR-52 (Explainer, November 6) sets context on Charcoal one step quieter than Dim Newsprint, which carries
    // secondary text there; this replaces section 3's Dim Newsprint for data context on Charcoal.
    context: semantic('graphic', 'Every other data mark in the same chart.',
      { newsprint: P('stone'), white: P('stone'), charcoal: T('stoneN35'), prussian: D('dimNewsprint') },
      { charcoal: { changedBy: 'DR-52, Explainer dark palette; section 3 had Dim Newsprint' } }),
    emphasisRed: semantic('graphic', 'The one point the headline names, in working red at the third rank (Rule 05.3). Only when no error or ask holds the view\'s red. On Newsprint it takes a 1 px Charcoal keyline. Never on Prussian.',
      { newsprint: P('pillarRed'), white: P('pillarRed'), charcoal: P('pillarRed') },
      { newsprint: { redRole: 'working', precedence: 3, keyline: '{oa.color.palette.charcoal}' },
        white: { redRole: 'working', precedence: 3 }, charcoal: { redRole: 'working', precedence: 3 } }),
  },
};

// ------------------------------------------------------------------------------------------ type
const font = {
  family: {
    display: tok('fontFamily', ['Inter Tight', 'Arial', 'sans-serif'], 'Display: titles, headings and big figures.'),
    reading: tok('fontFamily', ['Inter', 'Arial', 'sans-serif'], 'Reading and interface text, chart labels and numbers (DR-47).'),
    quote: tok('fontFamily', ['Lora', 'Georgia', 'serif'], 'Editorial quotation, italic only, and only for quoted words.', { fontStyle: 'italic' }),
    emailSans: tok('fontFamily', ['Helvetica', 'Arial', 'sans-serif'], 'Email display and body, the system stack V5 documents.'),
    emailQuote: tok('fontFamily', ['Georgia', 'serif'], 'Email quotation, set italic.', { fontStyle: 'italic' }),
  },
  weight: {
    regular: tok('fontWeight', 400, 'Inter reading text; Lora Italic quotation.'),
    medium: tok('fontWeight', 500, 'Lora Italic 500 for quote cards.'),
    semibold: tok('fontWeight', 600, 'Inter interface text and data labels.'),
    bold: tok('fontWeight', 700, 'Inter labels, the ask label and strong emphasis.'),
    extrabold: tok('fontWeight', 800, 'Inter Tight display and the wordmark face.'),
  },
};

// name: [family, weight, min px, max px, line height, tracking em, case, numeric, job]
// Sizes run in rem from 390 to 1440 px wide (T-9). The floor is 13 px with no screen exceptions.
const TYPE = [
  ['title', 'display', 'extrabold', 56, 110, 0.95, -0.045, 'none', null, 'Cover and chapter-opening titles.'],
  ['section', 'display', 'extrabold', 44, 80, 1.03, -0.04, 'none', null, 'Chapter headings (h2).'],
  ['h3', 'display', 'extrabold', 26, 32, 1.08, -0.03, 'none', null, 'Module headings.'],
  ['h4', 'display', 'extrabold', 20, 24, 1.15, -0.02, 'none', null, 'Sub-module and card headings.'],
  ['quote', 'quote', 'regular', 24, 32, 1.3, -0.02, 'none', null, 'Pull quotes and quote cards in Lora Italic.'],
  ['intro', 'reading', 'regular', 19, 22, 1.5, 0, 'none', null, 'Chapter introduction paragraph.'],
  ['body', 'reading', 'regular', 17, 17, 1.6, 0, 'none', null, 'Running text.'],
  ['bodySmall', 'reading', 'regular', 15, 15, 1.6, 0, 'none', null, 'Table cells and dense specimen notes.'],
  ['ui', 'reading', 'semibold', 15, 15, 1.4, 0, 'none', null, 'Buttons, navigation and form controls.'],
  ['caption', 'reading', 'regular', 14, 14, 1.5, 0, 'none', null, 'Figure captions and source lines.'],
  ['label', 'reading', 'bold', 13, 13, 1.4, 0.06, 'uppercase', null, 'Eyebrows, column heads and tags, set in capitals at 13 px with 6% tracking (T-9).'],
  ['dataLabel', 'reading', 'semibold', 13, 13, 1.3, 0, 'none', 'tabular-nums', 'Chart labels, axis values and table figures, with tabular figures and the true minus sign.'],
  ['figure', 'display', 'extrabold', 48, 104, 1.0, -0.04, 'none', 'tabular-nums', 'Big numbers in reports and specimens, with tabular figures and the true minus sign.'],
  ['ask', 'reading', 'bold', 19, 19, 1.2, 0, 'none', null, 'Ask button label. White on Pillar Red passes only as large text, so it never sets below 19 px bold (T-7).'],
];
const type = Object.fromEntries(TYPE.map(([name, fam, wt, minPx, maxPx, lh, tr, tt, numeric, job]) => [name, {
  $type: 'typography',
  $description: job,
  $value: { $kind: 'type', family: `oa.font.family.${fam}`, weight: `oa.font.weight.${wt}`, minPx, maxPx, lineHeight: lh, trackingEm: tr },
  ext: { tier: 'semantic', textTransform: tt, ...(numeric ? { numeric, minusSign: 'U+2212' } : {}), ...(fam === 'quote' ? { fontStyle: 'italic' } : {}) },
}]));

// ------------------------------------------------------------------------------------------ space, size, layout
const SPACE = [['0', 0], ['050', 4], ['100', 8], ['150', 12], ['200', 16], ['300', 24], ['400', 32], ['500', 40], ['600', 48], ['800', 64], ['1000', 80], ['1300', 104]];
const space = {
  $description: 'Eleven steps on V5\'s 8 px rhythm plus zero, named by the multiple of 8 times 100. Type rhythm in rem.',
  ...Object.fromEntries(SPACE.map(([k, p]) => [k, tok('dimension', { $kind: 'remFromPx', px: p }, `${p} px at the default text size.`)])),
};

const size = {
  icon: {
    small: tok('dimension', px(16), 'Civic Line icon at 16 px. At this size an icon is one color, with no red (R10, DR-67).', { oneColor: true }),
    medium: tok('dimension', px(24), 'Civic Line icon at 24 px, the smallest size that may carry a red accent.'),
    large: tok('dimension', px(48), 'Civic Line icon at 48 px. A pillar mark under this size sits with its word (R9, DR-67).'),
  },
  target: {
    minimum: tok('dimension', px(24), 'Smallest pointer target, WCAG 2.2 success criterion 2.5.8.'),
    touch: tok('dimension', px(44), 'Height of tabs, links and buttons in the studio pages and the guide.'),
  },
};

const BREAKPOINTS = [['wide', 1440, 12, 24, 64], ['desktop', 1024, 12, 24, 40], ['tablet', 768, 8, 24, 32], ['phone', 390, 4, 16, 20], ['phoneSmall', 360, 4, 16, 16]];
const layout = {
  breakpoint: Object.fromEntries(BREAKPOINTS.map(([n, w]) => [n, tok('dimension', px(w),
    n === 'phoneSmall' ? `Small phone design and test width, ${w} px; the same layout holds the 320 px reflow test.` : `${n[0].toUpperCase() + n.slice(1)} design and test width, ${w} px.`,
    w >= 768
      ? { mediaQuery: `(min-width: ${w / 16}em)`, mediaQueryNote: 'Media queries cannot read custom properties, so a stylesheet writes this query in em, which follows text size.' }
      : { mediaQuery: null, mediaQueryNote: n === 'phone' ? 'The base layout: no query.' : 'A test width for the base layout: no query.' })])),
  grid: Object.fromEntries(BREAKPOINTS.map(([n, w, cols, gutter, margin]) => [n, {
    columns: tok('number', cols, `Columns at the ${n} width.`, { unit: 'columns' }),
    gutter: tok('dimension', px(gutter), `Gutter between columns at the ${n} width.`),
    margin: tok('dimension', px(margin), `Page margin at the ${n} width.`),
  }])),
  measure: {
    bodyIdeal: tok('dimension', rem(33.88), 'Body measure for 68 characters of 17 px Inter, measured over 26,950 characters of V5 prose.', { chars: 68 }),
    bodyMax: tok('dimension', rem(37.37), 'Widest body measure, 75 characters of 17 px Inter.', { chars: 75 }),
    introMax: tok('dimension', rem(41.91), 'Widest intro measure, 65 characters of 22 px Inter.', { chars: 65 }),
  },
};

const radius = {
  none: tok('dimension', px(0), 'Every box, button and input.'),
  full: tok('number', 0.5, 'Circles: Signal Grid nodes, badges and the round container mark. DTCG has no percentage, so the value is a fraction and CSS writes 50%.', { css: '50%' }),
};

const border = {
  width: {
    hairline: tok('dimension', px(1), 'Dividers, keylines and chart axes.'),
    rule: tok('dimension', px(2), 'The current-page underline.'),
    bar: tok('dimension', px(4), 'State bar beside selected, error and warning items.'),
    focusRing: tok('dimension', px(2), 'Keyboard focus outline.'),
    underline: tok('dimension', px(1), 'Link underline at rest.'),
    underlineHover: tok('dimension', px(2), 'Link underline on hover.'),
  },
  focusOffset: tok('dimension', px(2), 'Gap between a control and its focus ring.'),
};

const opacity = {
  $description: 'Two decorative jobs and no others (T-10). A color token is never transparent.',
  watermarkOnLight: tok('number', 0.08, 'Charcoal watermark on Newsprint or White. Decoration only: it measures 1.17:1 and never carries meaning.', { composite: { ink: '{oa.color.palette.charcoal}', ground: '{oa.color.palette.newsprint}' } }),
  watermarkOnDark: tok('number', 0.10, 'Newsprint watermark on Charcoal or Prussian. Decoration only: it measures 1.24:1 and never carries meaning.', { composite: { ink: '{oa.color.palette.newsprint}', ground: '{oa.color.palette.charcoal}' } }),
};

const motion = {
  duration: {
    fast: tok('duration', ms(120), 'Hover, focus and toggles.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
    standard: tok('duration', ms(200), 'Reveals, panels and node fills.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
    slow: tok('duration', ms(320), 'Page-level moves, the hinge settle and the ring slide.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
    stagger: tok('duration', ms(40), 'Delay between siblings.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
    hinge: tok('duration', ms(680), 'The hinge draw, played on request only.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
    lever: tok('duration', ms(560), 'The lever land, played on request only.', { reducedMotionValue: { value: 0, unit: 'ms' } }),
  },
  easing: {
    standard: tok('cubicBezier', [0.2, 0, 0, 1], 'Most transitions.'),
    enter: tok('cubicBezier', [0, 0, 0.2, 1], 'Arriving: panels, the ampersand and the lever.'),
    exit: tok('cubicBezier', [0.4, 0, 1, 1], 'Leaving, at the fast duration.'),
  },
};

const zIndex = {
  base: tok('number', 0, 'The page.'),
  raised: tok('number', 10, 'Specimen overlays.'),
  sticky: tok('number', 40, 'Sticky navigation.'),
  overlay: tok('number', 90, 'Menus and popovers outside the top layer.'),
  skip: tok('number', 100, 'The skip link.'),
};

// ------------------------------------------------------------------------------------------ chart
// Colors: Explainer's ground tokens (work/boards/phase-2/data-viz/01-explainer/build_concept.py,
// ground_tokens), the stretch test's added grounds (stretch/build_stretch.py, stretch_ground) and
// diverging pair B from the palette lab (work/build/scripts/phase-2/dataviz_palette_lab.py), on the two
// chart grounds. Component tokens point at the semantic data and text roles; chart-only roles point at tints.
const NC = (n, c) => ({ newsprint: n, charcoal: c });
const steps = (n, make) => Object.fromEntries(Array.from({ length: n }, (_, i) => [`step${i + 1}`, make(i + 1)]));
const SEQ_N = ['verdigrisN82', 'verdigrisN52p75', 'verdigrisN23p5', 'verdigrisC5p75', 'verdigrisC35'];
const SEQ_C = ['verdigrisC75', 'verdigrisC50', 'verdigrisC20', 'verdigrisN25', 'verdigrisN55'];
const SEQ_LABEL_N = ['charcoal', 'charcoal', 'charcoal', 'white', 'white'];
const SEQ_LABEL_C = ['newsprint', 'newsprint', 'newsprint', 'charcoal', 'charcoal'];
const DIV_N = [P('prussian'), T('prussianN62'), T('stoneN90'), T('verdigrisN55'), T('verdigrisC25')];
const DIV_LABEL_N = ['white', 'charcoal', 'charcoal', 'charcoal', 'white'];
const MAG_N = [T('stoneN88'), T('stoneN55'), T('stoneC10'), T('stoneC60')];
const MAG_C = [T('stoneC75'), T('stoneC40'), T('stoneN55'), T('stoneN85')];
const MAG_LABEL_N = ['charcoal', 'charcoal', 'newsprint', 'newsprint'];
const MAG_LABEL_C = ['newsprint', 'newsprint', 'charcoal', 'charcoal'];
const DIV_WORDS = ['strong Prussian end', 'light Prussian step', 'midpoint, tinted toward the page', 'light Verdigris step', 'strong Verdigris end'];

const chartColor = {
  $description: 'Chart color on Newsprint, the page color (DR-53), and on Charcoal, the dark ground (DR-50). One dark subject against gray context; red only for the one point a title names.',
  subject: component('Subject: the series the title names and its labels (Explainer ink). 3 px lines, 6.5 px dots.', NC('{oa.color.data.emphasis.onNewsprint}', '{oa.color.data.emphasis.onCharcoal}')),
  context: component('Context: every other series, 2 px, so the subject reads first (Explainer ctx).', NC('{oa.color.data.context.onNewsprint}', '{oa.color.data.context.onCharcoal}')),
  label: component('Direct labels on the subject and chart headings.', NC('{oa.color.text.primary.onNewsprint}', '{oa.color.text.primary.onCharcoal}')),
  secondary: component('Ticks, notes, measure lines and source lines (Explainer sec).', NC('{oa.color.text.secondary.onNewsprint}', '{oa.color.text.secondary.onCharcoal}')),
  baseline: component('The zero baseline and reference rules, 1.5 px.', NC('{oa.color.data.emphasis.onNewsprint}', '{oa.color.data.emphasis.onCharcoal}')),
  leader: component('Leaders from a note to its mark, 1 px.', NC('{oa.color.data.context.onNewsprint}', '{oa.color.data.context.onCharcoal}')),
  point: component('The one point a title names, in working red at the third rank. Only when no error or ask holds the view\'s red.', NC('{oa.color.data.emphasisRed.onNewsprint}', '{oa.color.data.emphasisRed.onCharcoal}')),
  pointKeyline: component('The 1 px keyline around a red point on Newsprint, where Pillar Red measures 2.96:1.', { newsprint: '{oa.color.border.strong.onNewsprint}' }),
  party: {
    mark: component('Every mark that stands for a party\'s lead, vote or share: one neutral ink for every party, with the party named on the mark (DR-48, DR-58).', NC('{oa.color.data.emphasis.onNewsprint}', '{oa.color.data.emphasis.onCharcoal}'),
      { newsprint: { partyMark: true }, charcoal: { partyMark: true } }),
  },
  labelOnSubject: semantic('text', 'Text set on a subject-colored bar or chip (Explainer inv).', NC(P('white'), P('charcoal')),
    { newsprint: { ground: '{oa.color.data.emphasis.onNewsprint}' }, charcoal: { ground: '{oa.color.data.emphasis.onCharcoal}' } }),
  chip: {
    fill: semantic('graphic', 'Fill of the evidence-label chip above a chart title.', NC(P('charcoal'), P('newsprint'))),
    label: semantic('text', 'Text in the evidence-label chip.', NC(P('newsprint'), P('charcoal')),
      { newsprint: { ground: '{oa.chart.color.chip.fill.onNewsprint}' }, charcoal: { ground: '{oa.chart.color.chip.fill.onCharcoal}' } }),
  },
  lightFill: semantic('dataFill', 'Light fill: a category under the subject, with its value printed (Explainer lt).', NC(T('stoneN55'), P('stone')),
    { newsprint: { valuesPrinted: true }, charcoal: { valuesPrinted: true } }),
  track: semantic('decorative', 'Track: the whole a share sits in (Explainer lt2).', NC(T('stoneN88'), T('stoneC55'))),
  gridline: semantic('decorative', 'Gridline, 1 px. It may pass behind a label, which carries a ground-colored halo.', NC(T('stoneN70'), T('stoneC45'))),
  band: semantic('decorative', 'Band: a stretch of time a note names.', NC(T('whiteN55'), T('stoneC72'))),
  land: semantic('decorative', 'Map land under data marks (stretch test).', NC(T('whiteN55'), T('stoneC80'))),
  diverging: {
    $description: 'Diverging pair B, Prussian through the page color to Verdigris (DR-54). Neither end keeps its order in grayscale, so a boxed arrow or a printed sign carries direction. Newsprint only until a Charcoal ramp is measured.',
    fill: steps(5, (i) => semantic('dataFill', `Diverging pair B, step ${i} of 5: the ${DIV_WORDS[i - 1]}.`, { newsprint: DIV_N[i - 1] },
      { newsprint: { valuesPrinted: true, scale: 'diverging', step: i } })),
    label: steps(5, (i) => semantic('text', `Text on diverging step ${i}.`, { newsprint: P(DIV_LABEL_N[i - 1]) },
      { newsprint: { ground: `{oa.chart.color.diverging.fill.step${i}.onNewsprint}` } })),
  },
  sequential: {
    $description: 'Sequential Verdigris, five steps per ground, light to strong on Newsprint and dark to light on Charcoal, so the most always reads strongest (palette lab; stretch S16).',
    fill: steps(5, (i) => semantic('dataFill', `Sequential Verdigris, step ${i} of 5.`, NC(T(SEQ_N[i - 1]), T(SEQ_C[i - 1])),
      { newsprint: { valuesPrinted: true, scale: 'sequential', step: i }, charcoal: { valuesPrinted: true, scale: 'sequential', step: i } })),
    label: steps(5, (i) => semantic('text', `Text on sequential step ${i}.`, NC(P(SEQ_LABEL_N[i - 1]), P(SEQ_LABEL_C[i - 1])),
      { newsprint: { ground: `{oa.chart.color.sequential.fill.step${i}.onNewsprint}` }, charcoal: { ground: `{oa.chart.color.sequential.fill.step${i}.onCharcoal}` } })),
    outline: semantic('graphic', 'Outline of a sized circle on a sequential map: the strongest step, holding 3:1 on the ground and on the land (stretch qk).', NC(T(SEQ_N[4]), T(SEQ_C[4])),
      { newsprint: { groundsAlso: ['{oa.chart.color.land.onNewsprint}'] }, charcoal: { groundsAlso: ['{oa.chart.color.land.onCharcoal}'] } }),
  },
  magnitude: {
    $description: 'Gray steps by size, with no direction, for phone tile maps of shifts (DR-64; stretch S12). The figure prints in every tile.',
    fill: steps(4, (i) => semantic('dataFill', `Gray magnitude step ${i} of 4.`, NC(MAG_N[i - 1], MAG_C[i - 1]),
      { newsprint: { valuesPrinted: true, scale: 'magnitude', step: i }, charcoal: { valuesPrinted: true, scale: 'magnitude', step: i } })),
    label: steps(4, (i) => semantic('text', `Text on gray magnitude step ${i}.`, NC(P(MAG_LABEL_N[i - 1]), P(MAG_LABEL_C[i - 1])),
      { newsprint: { ground: `{oa.chart.color.magnitude.fill.step${i}.onNewsprint}` }, charcoal: { ground: `{oa.chart.color.magnitude.fill.step${i}.onCharcoal}` } })),
  },
};

const EXPL = (k) => `build_concept.py CHART_TOKENS${k}`;
const STR = (k) => `build_stretch.py STRETCH_TOKENS${k}`;
const chart = {
  $description: 'The chart kit\'s tokens: color roles on the two chart grounds and every size the Explainer generators draw with. Sizes are SVG px at the artboard\'s natural width.',
  color: chartColor,
  artboard: {
    wide: chartDim(1024, 'Widest artboard: a chart that breaks out of the reading column.', EXPL("['artboard']['wide']")),
    reading: chartDim(720, 'Artboard in the reading column.', EXPL("['artboard']['reading']")),
    mid: chartDim(600, 'Middle artboard for tablets and narrow columns.', EXPL("['artboard']['mid']")),
    phone: chartDim(358, 'Phone artboard: 390 px less the margins.', EXPL("['artboard']['phone']")),
    smallPhone: chartDim(328, 'Small phone artboard: 360 px less the margins.', EXPL("['artboard']['small_phone']")),
  },
  type: {
    $description: 'Type sizes inside chart drawings, in Inter and Inter Tight only (DR-47). Nothing under 13 px; phone artboards set nothing under 14 px except tile codes.',
    label: chartDim(15, 'Direct labels on marks.', EXPL("['type']['label']"), { role: 'fontSize' }),
    tick: chartDim(13, 'Axis tick values.', EXPL("['type']['tick']"), { role: 'fontSize' }),
    note: chartDim(14, 'Notes inside the drawing.', EXPL("['type']['note']"), { role: 'fontSize' }),
    noteLeading: chartDim(19, 'Leading of notes inside the drawing.', EXPL("['type']['note_leading']"), { role: 'lineHeight' }),
    phoneMin: chartDim(14, 'Smallest type on phone artboards.', EXPL("['type']['phone_min']"), { role: 'fontSize' }),
    tileCodePhone: chartDim(13, 'State codes in tile maps on phones, the one phone size under 14 px.', EXPL("['type']['tile_code_phone']"), { role: 'fontSize' }),
    big: chartDim(116, 'The big number in a big-number chart.', EXPL("['type']['big']"), { role: 'fontSize' }),
    bigPhone: chartDim(88, 'The big number on phones.', EXPL("['type']['big_phone']"), { role: 'fontSize' }),
    eyebrow: chartDim(13, 'Eyebrows inside the drawing, capitals at 6% tracking.', EXPL("['type']['eyebrow']"), { role: 'fontSize' }),
    titleSize: chartDim(28, 'Chart title, Inter Tight 800.', EXPL("['type']['title'][0]"), { role: 'fontSize' }),
    titleLeading: chartDim(32, 'Leading of the chart title.', EXPL("['type']['title'][1]"), { role: 'lineHeight' }),
    titlePhoneSize: chartDim(22, 'Chart title on phones.', EXPL("['type']['title_phone'][0]"), { role: 'fontSize' }),
    titlePhoneLeading: chartDim(27, 'Leading of the chart title on phones.', EXPL("['type']['title_phone'][1]"), { role: 'lineHeight' }),
    measureSize: chartDim(17, 'Measure line under the title: what is counted, where and when.', EXPL("['type']['measure'][0]"), { role: 'fontSize' }),
    measureLeading: chartDim(27, 'Leading of the measure line.', EXPL("['type']['measure'][1]"), { role: 'lineHeight' }),
  },
  line: {
    hairline: chartDim(1, 'Gridlines and leaders.', EXPL("['line']['hairline']")),
    baseline: chartDim(1.5, 'Baselines and reference rules.', EXPL("['line']['baseline']")),
    context: chartDim(2, 'Context series.', EXPL("['line']['context']")),
    subject: chartDim(3, 'The subject series.', EXPL("['line']['subject']")),
    selected: chartDim(6, 'A selected series on an interactive chart.', EXPL("['line']['selected']")),
  },
  dot: {
    subjectRadius: chartDim(6.5, 'Radius of a subject value\'s dot.', EXPL("['dot']['subject_r']")),
    openRadius: chartDim(5.5, 'Radius of the open dot for an earlier value.', EXPL("['dot']['open_r']")),
    vertexRadius: chartDim(3, 'Radius of a line vertex.', EXPL("['dot']['vertex_r']")),
    smallVertexRadius: chartDim(2.25, 'Radius of a vertex in small multiples.', EXPL("['dot']['small_vertex_r']")),
  },
  bar: {
    height: chartDim(24, 'Bar height.', EXPL("['bar']['height']")),
    pitch: chartDim(42, 'Distance from one bar to the next.', EXPL("['bar']['pitch']")),
    denseHeight: chartDim(16, 'Bar height past ten rows.', EXPL("['bar']['dense_height']")),
    densePitch: chartDim(36, 'Bar pitch past ten rows.', EXPL("['bar']['dense_pitch']")),
    phoneHeight: chartDim(20, 'Bar height on phones, with the label above the bar.', EXPL("['bar']['phone_height']")),
    phonePitch: chartDim(58, 'Bar pitch on phones.', EXPL("['bar']['phone_pitch']")),
  },
  unit: {
    size: chartDim(14, 'Side of one square in a unit chart.', EXPL("['unit']['size']")),
    gap: chartDim(3, 'Gap between unit squares.', EXPL("['unit']['gap']")),
  },
  note: {
    width: chartDim(520, 'Widest note under a drawing.', EXPL("['note']['width']")),
    minChars: chartNum(45, 'characters', 'Shortest line a note may wrap to.', EXPL("['note']['min_chars']")),
    maxChars: chartNum(75, 'characters', 'Longest line a note may run to.', EXPL("['note']['max_chars']")),
    gap: chartDim(10, 'Gap between a note and its mark.', EXPL("['note']['gap']")),
    leaderMin: chartDim(12, 'Shortest leader the layout guard accepts.', EXPL("['note']['leader_min']")),
  },
  guard: {
    headroom: chartNum(1.15, 'ratio', 'Width allowance on every label box, for readers who widen text spacing.', EXPL("['guard']['headroom']")),
    linePad: chartDim(1, 'Clearance the layout guard keeps between a label box and a line.', EXPL("['guard']['line_pad']")),
  },
  halo: chartDim(4, 'Ground-colored halo behind a label that a gridline passes behind.', EXPL("['halo']")),
  hatch: {
    pitch: chartDim(5, 'Spacing of the hatch for contested evidence.', EXPL("['hatch']['pitch']")),
    weight: chartDim(1.5, 'Stroke of the hatch.', EXPL("['hatch']['weight']")),
  },
  keyline: chartDim(1, 'Keyline around a red point on Newsprint.', EXPL("['keyline']")),
  gapYears: chartNum(1, 'years', 'A unit chart gives each year its own column after the last run of two or more empty years; this is the gap it allows.', EXPL("['gap_years']")),
  arrow: {
    shaft: chartDim(2, 'Shaft of a shift arrow.', STR("['arrow']['shaft']")),
    headLength: chartDim(8, 'Length of an arrowhead.', STR("['arrow']['head_len']")),
    headHalfWidth: chartDim(4.5, 'Half the width of an arrowhead.', STR("['arrow']['head_half']")),
    phoneHeadLength: chartDim(6, 'Length of an arrowhead on phones.', STR("['arrow']['phone_head_len']")),
    phoneHeadHalfWidth: chartDim(3.5, 'Half the width of an arrowhead on phones.', STR("['arrow']['phone_head_half']")),
    tailRadius: chartDim(2.25, 'Radius of the dot at an arrow\'s start.', STR("['arrow']['tail_r']")),
    tipRadius: chartDim(0.5, 'Radius of the dot at an arrow\'s tip.', STR("['arrow']['tip_r']")),
  },
  shiftAxis: {
    pitch: chartDim(20, 'Row pitch in a shift-arrow chart.', STR("['shift_axis']['pitch']")),
    label: chartDim(14, 'Row labels in a shift-arrow chart.', STR("['shift_axis']['label']"), { role: 'fontSize' }),
    breakGap: chartDim(32, 'Gap that marks a broken axis.', STR("['shift_axis']['break_gap']")),
    phoneLollipopPitch: chartDim(44, 'Row pitch of the phone lollipop drawing.', STR("['shift_axis']['phone_lollipop_pitch']")),
  },
  tile: {
    sizeMax: chartDim(80, 'Largest tile in a tile-grid map.', STR("['tile']['size_max']")),
    gap: chartDim(6, 'Gap between tiles.', STR("['tile']['gap']")),
    midGap: chartDim(4, 'Gap between tiles at the middle artboard.', STR("['tile']['mid_gap']")),
    phoneGap: chartDim(2.5, 'Gap between tiles on phones.', STR("['tile']['phone_gap']")),
    phoneColumns: chartNum(11, 'columns', 'Columns of the tile grid on phones.', STR("['tile']['phone_cols']")),
    frame: chartDim(2, 'Outline of a tile that changed hands.', STR("['tile']['frame']")),
  },
  spark: {
    line: chartDim(2, 'A sparkline\'s own series.', STR("['spark']['line']")),
    context: chartDim(1.5, 'Context line in a sparkline panel.', STR("['spark']['context']")),
    endRadius: chartDim(3, 'Dot at a sparkline\'s end.', STR("['spark']['end_r']")),
    gapX: chartDim(30, 'Gap between sparkline panels.', STR("['spark']['gap_x']")),
    phoneGapX: chartDim(18, 'Gap between sparkline panels on phones.', STR("['spark']['phone_gap_x']")),
  },
  columns: {
    fillShare: chartNum(0.72, 'ratio', 'Share of a period\'s width a column fills.', STR("['columns']['fill_share']")),
    averageLine: chartDim(3, 'Moving-average line over columns.', STR("['columns']['avg_line']")),
    vertexRadius: chartDim(1.5, 'Vertex dot on the average line.', STR("['columns']['vertex_r']")),
    height: chartDim(360, 'Plot height of a column chart.', STR("['columns']['height']")),
    phoneHeight: chartDim(290, 'Plot height of a column chart on phones.', STR("['columns']['phone_height']")),
  },
  bubble: {
    radiusMax: {
      wide: chartDim(50, 'Largest circle on the wide artboard.', STR("['bubble']['r_max']['wide']")),
      mid: chartDim(34, 'Largest circle on the middle artboard.', STR("['bubble']['r_max']['mid']")),
      phone: chartDim(23, 'Largest circle on the phone artboard.', STR("['bubble']['r_max']['phone']")),
      smallPhone: chartDim(21, 'Largest circle on the small phone artboard.', STR("['bubble']['r_max']['small_phone']")),
    },
    gap: chartDim(2, 'Gap between circles.', STR("['bubble']['gap']")),
    outline: chartDim(1, 'Circle outline.', STR("['bubble']['outline']")),
    ring: chartDim(2, 'Ring around a circle a note names.', STR("['bubble']['ring']")),
    keyStep: chartDim(64, 'Width of one step in the color key.', STR("['bubble']['key_seg']")),
    labelPad: chartDim(3, 'Padding around a circle\'s label.', STR("['bubble']['label_pad']")),
    leaderClear: chartDim(3, 'Clearance between a leader\'s label and any other circle.', STR("['bubble']['leader_clear']")),
  },
  results: {
    gap: chartDim(12, 'Gap between results-table columns.', STR("['results']['gap']")),
    bar: chartDim(6, 'In-row bar height.', STR("['results']['bar']")),
    barGap: chartDim(4, 'Gap between in-row bars.', STR("['results']['bar_gap']")),
    shiftHead: chartDim(8, 'Arrowhead in the shift column.', STR("['results']['shift_head']")),
    shiftMin: chartDim(130, 'Narrowest shift column.', STR("['results']['shift_min']")),
    htmlHeadroom: chartNum(1.06, 'ratio', 'Width allowance on measured HTML text in the table.', STR("['results']['html_headroom']")),
    twoLineMin: chartDim(560, 'Narrowest container that takes two-line cards.', STR("['results']['two_line_min']")),
  },
  tag: {
    padX: chartDim(6, 'Padding each side of a tag\'s text.', STR("['tag']['pad_x']")),
    height: chartDim(18, 'Height of a tag box for 13 px text.', STR("['tag']['height']")),
    ascentEm: chartNum(0.77, 'em', 'Top of the d above the baseline in Inter, for boxing a tag.', STR("['tag']['ascent_em']")),
    descentEm: chartNum(0.23, 'em', 'Foot of the g below the baseline in Inter, for boxing a tag.', STR("['tag']['descent_em']")),
  },
};

// ------------------------------------------------------------------------------------------ components
const componentTokens = {
  button: {
    ask: {
      fill: component('Ask button fill. When an error holds the view\'s red, use the primary button instead.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.action.ask.fill.${SURFACE_KEY[s]}}`])),
        Object.fromEntries(SURF4.map((s) => [s, { fallback: `{oa.component.button.primary.fill.${SURFACE_KEY[s]}}` }]))),
      label: component('Ask button label.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.action.ask.label.${SURFACE_KEY[s]}}`]))),
      keyline: component('The 1 px edge that gives the red fill its boundary on Newsprint.', { newsprint: '{oa.color.border.strong.onNewsprint}' }),
      labelType: tok('typography', '{oa.type.ask}', 'Ask button label style: 19 px bold or larger.', { tier: 'component' }),
    },
    primary: {
      fill: component('Primary button fill.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.action.primary.fill.${SURFACE_KEY[s]}}`]))),
      fillHover: component('Primary button fill on hover.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.action.primary.fillHover.${SURFACE_KEY[s]}}`]))),
      label: component('Primary button label.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.action.primary.label.${SURFACE_KEY[s]}}`]))),
    },
    disabled: {
      label: component('Disabled button label. Pair it with a reason line, such as "Choose a size to download".', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.state.disabled.text.${SURFACE_KEY[s]}}`]))),
      edge: component('Disabled button edge, drawn dashed.', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.state.disabled.edge.${SURFACE_KEY[s]}}`])),
        Object.fromEntries(SURF4.map((s) => [s, { strokeStyle: 'dashed' }]))),
    },
  },
  icon: {
    ink: component('Civic Line icon ink. At 16 px the whole icon takes this one color (R10).', Object.fromEntries(SURF4.map((s) => [s, `{oa.color.graphic.essential.${SURFACE_KEY[s]}}`]))),
    accent: component('Red accent of a standalone icon, or of the current icon in a row or menu, at 24 px and up: signature red, bare on Newsprint (R11, DR-66). White on Prussian.',
      Object.fromEntries(SURF4.map((s) => [s, `{oa.color.identity.signature.${SURFACE_KEY[s]}}`])),
      Object.fromEntries(SURF4.map((s) => [s, { minSize: '{oa.size.icon.medium}' }]))),
  },
  appIcon: {
    tile: tok('color', '{oa.color.surface.charcoal}', 'App icon tile: Charcoal by default (R13, DR-67).', { tier: 'component' }),
    mark: tok('color', '{oa.color.graphic.essential.onCharcoal}', 'The icon on the app icon tile, in Newsprint (G1-09).', { tier: 'component' }),
    accent: tok('color', '{oa.color.identity.signature.onCharcoal}', 'Red accent on the app icon tile: signature red, since the icon stands alone.', { tier: 'component' }),
  },
  avatar: {
    tile: tok('color', '{oa.color.surface.charcoal}', 'Avatar tile: Charcoal by default (R13, DR-67).', { tier: 'component' }),
    mark: tok('color', '{oa.color.graphic.essential.onCharcoal}', 'The mark on the avatar tile, in Newsprint.', { tier: 'component' }),
    accent: tok('color', '{oa.color.identity.signature.onCharcoal}', 'Red accent on the avatar: signature red, since the mark stands alone.', { tier: 'component' }),
  },
};

export const tree = {
  oa: {
    color,
    font,
    type,
    space,
    size,
    layout,
    radius,
    border,
    opacity,
    motion,
    zIndex,
    chart,
    component: componentTokens,
  },
};
