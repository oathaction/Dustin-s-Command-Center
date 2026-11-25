// Chat 13b (DR-330, board 1's item 2, locked identity approved by name): on Newsprint, ampersand B in a hinge headline
// takes Rule 05.3's keyline, a 1 px Charcoal edge drawn inside the mark. B keeps its Pillar Red, its shape and its size;
// on White and Charcoal it takes none, and B in the wordmark, the lockmark, the favicon, the avatars and the badge never
// does. keyline(svg, id) takes B as lib.mark() draws it and draws the master's own outline stroked 2 px wide at any scale
// and clipped to the mark, so the inner pixel shows: the method of board 1's pictures (DD10-NF1) and of the guide's
// stage_a_identity_s04.keyline_b. The outline is placed once and drawn by <use> for the fill, the clip and the edge.
// Not a renderer of its own: the share card and the social post import it.
export const KEYLINE = 'var(--oa-color-border-strong-on-newsprint)';   // Rule 05.3: Charcoal, the control edge that keylines red

export function keyline(svg, id) {
  const paths = svg.match(/<path\b[^>]*\/>/g) || [];
  if (paths.length !== 1) throw new Error(`hinge keyline: B should hold one outline, found ${paths.length}`);
  const d = (paths[0].match(/\sd="([^"]+)"/) || [])[1];
  if (!d) throw new Error('hinge keyline: B\'s outline has no path data');
  return svg.replace(paths[0], `<defs><path id="${id}" d="${d}" vector-effect="non-scaling-stroke"/>`
    + `<clipPath id="${id}-c"><use href="#${id}"/></clipPath></defs><use href="#${id}" fill="currentColor"/>`
    + `<use href="#${id}" fill="none" clip-path="url(#${id}-c)" stroke-width="2" style="stroke:${KEYLINE}"/>`);
}
