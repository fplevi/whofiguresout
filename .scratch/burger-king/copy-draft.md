# Burger King Delivery Concept — copy draft

Status: aguardando aprovação. Texto final em inglês; notas em português.

Imagens: recapturar todas no site publicado (https://fplevi.github.io/BurguerKingDelivery/), porque as de `output/portfolio-v2/` são anteriores ao "Onde vamos entregar?" do cardápio. Script: `.scratch/burger-king/capture.mjs`.

Fontes: `D:\Projetos\BurguerKingNewSite` (README do protótipo, ADRs 0001 e 0002, `output/portfolio-v2/SOURCE-COPY.md`), Figma `BElIaiOW5D1qFF8QStnoDo` node `458:13203`.

## Meta

- `<title>`: Burger King Delivery Concept | Felipe Levi
- description / og: A self-initiated redesign of fast-food delivery: only what's needed to order, on any phone. Not affiliated with Burger King.

## Header

- Tag: Independent Concept
- Title: Burger King Delivery Concept
- Hook: A self-initiated redesign of fast-food delivery, focused on what it takes to place an order and nothing else.
- Disclaimer (texto simples logo abaixo do hook): This is a self-initiated study. It was not commissioned by or affiliated with Burger King, and it has not been validated with users.

### Word search — "The case in five words"

| Word | Chip | Category | Caption |
| --- | --- | --- | --- |
| CLUTTER | Clutter | Problem | Delivery apps put coupons, offers and pop-ups between the customer and the order. |
| NOCOUPONS | No coupons | Decision | No offers tab, coupons or unsolicited pop-ups. Attention stays on choosing food. |
| TRAY | Tray | Decision | Take an ingredient out, keep it in the tray, and put it back before applying. |
| ADDRESSFIRST | Address first | Decision | Customers check delivery to their address before giving a phone number. |
| BUDGET | Budget | Trade-off | A 3D burger costs weight and battery. A strict budget and an SVG fallback keep it usable on simpler devices. |

### Meta pills

- Type: Self-initiated study
- Role: Design Direction
- Delivery: Web prototype

## The Problem

**Ordering food shouldn't feel like a sales funnel.**

Delivery apps often surround the order with coupons, offers and pop-ups. My hypothesis: a flow with only what's needed to order, that runs on any phone, is a calmer and more honest experience. This is a personal point of view, not a research finding.

## My Role

**Directed end to end. Built with AI.**

The decisions in this case are mine. Design and code were produced through a fully AI-driven workflow. Whenever the AI fell short of what I intended, I made targeted adjustments in Figma to get the result I wanted.

## The Decisions

**Less to decide. More control over what matters.**

### 01 — Leave out coupons and offers

There is no offers tab, no coupon field, no prize wheel and no unsolicited pop-up. The menu shows the product, its ingredients and its price, and the customer decides when to add it to the cart. Removing these prompts is deliberate: the flow should help people order what they came for, not push them to consume more.

Media: `captures/menu-visitor.png`, capturada no site publicado (mostra "Onde vamos entregar?", que reforça a decisão 04)
Alt: Menu with the Whopper in 3D beside its description, a purchase card with combo option, quantity and item total, and a grid of burgers below, with no offers or coupon areas.

### 02 — See inside the burger, then decide

Customers open the burger to see each ingredient as a separate layer. Taking one out moves it to a tray beside the burger, where it stays until they put it back or apply the change. Nothing is final until they apply it, so changing your mind costs one tap. The model shows which ingredients are in the recipe, not exact portions.

Media: `ingredient-control.mp4` (mudo, loop, sem autoplay com reduced motion), poster `ingredients-intact.png`
Alt / legenda: The burger opens into layers; the cheese is taken out to the tray and then put back before applying.

### 03 — Keep the 3D light enough for any phone

The 3D burger is there to explain the recipe, not to show off. Every burger is modeled by code, with no downloaded ingredient images, and the 3D part has a fixed weight and speed budget. Without WebGL, the same burger is drawn in SVG and every interaction still works. Motion is reduced when the system asks for it. In lab tests with a 4× slower CPU, the 3D code weighed 159.5 KB gzipped and the first frame appeared in about 1.2 s. It has not been tested on physical phones.

Nota: "simple" aqui = orçamento controlado, não visual pobre; as imagens mostram detalhe, e o texto não afirma que roda em qualquer aparelho como fato.

Media: `burger-assembled.png` + `burger-fallback.png` lado a lado
Legendas: WebGL · SVG fallback
Alt: The same Whopper rendered in 3D with WebGL and drawn as an SVG illustration when WebGL is unavailable.

### 04 — Check the address before asking who you are

Customers want to know whether delivery reaches them before creating an account. The delivery address can be chosen from the menu without confirming a phone number, and the app only speaks up when it doesn't deliver to that area. The phone number comes later, at checkout.

Media: `captures/address-visitor.png` (recortada), capturada no site publicado
Alt: Delivery address page opened from the menu by a visitor, with address search and current location, while the header still offers Identifique-se and no checkout steps are shown.

Nota: a captura antiga (`04-saved-addresses`) mostrava a Identificação já concluída e contradizia a decisão; foi descartada.

## What Shipped

**A complete flow, simulated where it has to be.**

The prototype covers the whole journey: menu, customization, cart, checkout, order confirmation and order tracking, on desktop and mobile. Maps, sign-in and payments are simulated, with fixed data, so the flow can be explored without real services.

| Card | Media | Texto |
| --- | --- | --- |
| Cart | `desktop-cart.png` | Each item shows what was taken out of it, and combo, drink and quantity can be edited in place. Removing an item can be undone. |
| Checkout | `desktop-checkout.png` | Checkout follows three steps: identification, address and payment, with Pix or credit card. The order summary stays visible beside each step. |
| Order tracking | `captures/tracking.png` | After confirmation, the customer follows the order through each status, with the delivery window and the route from the store to the address on a map. Statuses advance on simulated timing. |
| Mobile | `mobile-menu.png` + `mobile-ingredients.png` | On phones, the page becomes a single column, and the main action stays fixed at the bottom of the screen. |

Nota: acompanhamento conferido no site publicado em 2026-10-24 (pedido com cartão → "Acompanhar pedido" → `#conta/pedidos/BK-10483`). O README do protótipo está desatualizado nesse ponto.

## Try It

**See it for yourself.**

The prototype is live. Nothing in it was tested with users, so treat it as a proposal to explore, not a proven result.

CTA: Open the prototype ↗ → https://fplevi.github.io/BurguerKingDelivery/

## Footer note (acima de Next project)

Burger King and its trademarks belong to their owners. This is an unpaid, unvalidated design study.

## Next project

Harmony → (Design System). Convênios passa a apontar para este case.

## Home card 05

- Tag: Independent Concept
- Title: Burger King Delivery Concept
- Hook: A calmer delivery flow: no coupons, no pop-ups, just the order. With a 3D burger you can take apart.
- Stat: Live prototype / self-initiated, not validated
