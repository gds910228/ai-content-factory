# Dense Knowledge Whiteboard

## Style Prompt

A high-density Chinese knowledge explainer on a clean whiteboard: expressive black hand-drawn line art, clear visual relationships, compact handwritten labels, restrained yellow, teal and orange accents, and a synchronized marker hand that reveals information in narrative order. The final frame should feel information-rich but remain readable at 1280×720.

## Colors

- Canvas: `#FFFFFF`; unrevealed module regions remain transparent.
- Primary ink and caption outline: `#171717`
- Warm emphasis: `#F6C453`
- Teal emphasis: `#3B9C95`
- Purple model/inference emphasis: `#8B5CF6`
- Orange emphasis: `#F08A5D`
- Red is reserved for risk and errors: `#EF4444`
- Caption panel: `rgba(55, 55, 55, 0.72)`

## Typography

- Knowledge labels and captions: `Hannotate SC`, `Kaiti SC`, `PingFang SC`, cursive
- Title: 44px, bold handwritten register
- Label and callout: 28–34px
- Bottom caption: 48px, white fill, black outline

## Motion

- Reveal image modules sequentially with independent transparent clip windows and an anchored marker hand.
- Fade and lift annotations in after their related module is complete.
- Reveal HTML technical components after their related module; use them for accurate Prompt, code, API, model, metric and risk text while preserving the hand-drawn whiteboard style.
- Use one caption group at a time with a short fade and a deterministic hard exit.
- Use 0.5s crossfades between scenes; do not animate outgoing scene elements away before the transition.

## What NOT to Do

- Do not render Chinese text inside generated images.
- Do not copy brands, logos, characters or wording from visual references.
- Do not place subject matter inside the bottom 110px caption safe area.
- Do not use gradients, dark canvases, dense background textures or unrelated decorative objects.
- Do not stretch or crop the supplied line-art image.
