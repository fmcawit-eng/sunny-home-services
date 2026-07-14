# Service Tile Photography Prompts (Gemini)

**All six** homepage service tiles need clean imagery. The previous AC/Heating photos
(`repair2.png`, `maintenance2.png`, `installation2.png`) were removed because they were
AI re-skins of third-party marketing photographs: the Higgsfield job history shows a
220x220 and a 460x559 web-thumbnail source image with prompts like *"replace the uniform
... to blue branded polo"* and *"change man's shirt and hat color to black, keep all
other elements the same."* The person, pose, equipment (a branded Lennox furnace), and
setting were all retained from a photo we do not own. Those files are still in
`assets/services/` for reference but must not be used on the site.

**Generate all six from these TEXT-ONLY prompts. Do not feed any source photo of a
person into the generator** - that is exactly what created the provenance problem. A
brand logo/mascot reference image for the uniform is fine; a real person's photo is not.

## Match these constraints in every prompt

So the six tiles look like one coherent set:

- **Technician wardrobe:** black short-sleeve polo shirt, black baseball cap, tan/khaki work pants, work boots. (The `2` variants of the existing files are the black-shirt versions. Match those, not the blue-shirt originals.)
- **Look:** photorealistic editorial photography, natural daylight, shallow depth of field, warm and friendly, not corporate-stiff.
- **Setting:** ordinary American suburban home, Utah/Mountain West feel.
- **Framing:** 3:2 landscape. The technician should sit in the **left or lower third**, because the tile applies a dark gradient scrim across the bottom for the caption text. Keep the top-right relatively clean.
- **No text, no visible brand logos, no watermarks** anywhere in the image.
- **Resolution:** at least 1600px wide.

Append this to each prompt:

> Photorealistic editorial photograph, natural daylight, shallow depth of field, 3:2 landscape, no text, no logos, no watermarks, high resolution.

Save results into `assets/services/` as `plumbing.png`, `drains.png`, `water-heater.png`, `air-quality.png`.

---

## 0a. Air Conditioning → `air-conditioning.png`

> A professional HVAC technician in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants kneeling beside an outdoor residential air-conditioning condenser unit next to a brick house, using a gauge to check the system. An open tool bag sits on the grass beside him. He looks focused and friendly. Bright natural daylight, green lawn.

## 0b. Heating → `heating.png`

> A professional HVAC technician in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants kneeling in front of an open residential gas furnace in a clean garage utility area, testing a component with a multimeter. An open tool bag rests on the concrete floor beside him. Warm indoor light, focused and friendly expression.

## 1. Plumbing → `plumbing.png`

> A professional plumber in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants kneeling on the floor of a clean, modern residential kitchen, working with a wrench on the supply lines under an open sink cabinet. An open tool bag with hand tools sits on a protective mat beside him. He looks focused and friendly. Warm daylight comes from a window behind him.

## 2. Drain and Sewers → `drains.png`

> A professional drain technician in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants kneeling in the side yard of a suburban home, feeding a black drain-cleaning cable into an open sewer cleanout pipe in the grass. A drain machine and a coiled cable sit next to him. Green lawn, house siding behind, bright natural daylight.

## 3. Water Heaters → `water-heater.png`

> A professional HVAC and plumbing technician in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants kneeling beside a tall residential tank water heater in a clean garage utility corner, checking the temperature and pressure valve with a tool in hand. Copper pipes and a gas line run above the unit. An open tool bag rests on the concrete floor. Soft daylight from a nearby window.

## 4. Indoor Air Quality → `air-quality.png`

> A professional HVAC technician in a black short-sleeve polo shirt, black baseball cap, and tan khaki work pants sliding a clean pleated air filter into the return-air housing of a residential furnace in a bright basement utility room. He holds the fresh white filter with both hands. Ductwork runs overhead. Clean, tidy space, soft natural light.

---

## After generating

In `sunny-home-services-markup-2.html`, find the four tiles marked with the comment
`The next 4 tiles await generated photography` and replace each placeholder:

```html
<!-- from -->
<div class="ac-tile-img ac-tile-ph ac-tile-ph-sky" data-parallax="6">
  <svg ...></svg>
</div>

<!-- to -->
<div class="ac-tile-img" data-parallax="6" style="background-image:url('assets/services/plumbing.png')"></div>
```

Then optimize: `sips -Z 2000 assets/services/plumbing.png --out assets/services/plumbing.png`

---

# Stale artwork carrying the OLD identity

These three assets still show the previous Marriott-Slaterville / Ogden identity and
the old phone number. They are visible to anyone reading the homepage.

## 1. `assets/map.png` - FIXED IN CODE
Was a Google Maps screenshot pinned on **Marriott-Slaterville / Ogden** (the old
address). Replaced with a live embed of 8461 Old Bingham Hwy, West Jordan. The old
PNG is now unused and can be deleted.

## 2. `assets/van2.png` and `assets/van.png` - NEEDS A DECISION
The van wrap in the photo reads **801.649.COOL (2665)**, not the 801.887.9650 used
everywhere else on the site. It is legible at full size on the homepage.

This is a real photo of a real wrapped van, so it is a client question, not a bug we
can fix in code:
- If 801.649.COOL is a dead number, the van needs rephotographing or the wrap needs
  updating, and the mockup needs a new image.
- If it is a live vanity line, decide which number the site should lead with.

If a regenerated image is wanted, prompt:

> A white-and-blue wrapped Ram ProMaster service van parked on a suburban street in
> West Jordan, Utah, with snow-capped Wasatch mountains behind it. The van wrap shows
> a large blue shield logo, a friendly cartoon sun mascot character, and clean text.
> Photorealistic, bright natural daylight, 3:2 landscape, side profile view, no
> readable phone number, no watermarks, high resolution.

Then add the correct phone number as an HTML overlay rather than baking it into the
image, so it can never go stale again.

## 3. Copy - FIXED IN CODE
The page title and the About section said "Northern Utah" (the old market). Both now
say West Jordan / the Wasatch Front, matching the brief.

---

# GENERATED 2026-07-14 - clean provenance record

All seven images were generated in Higgsfield (`soul_2` / text2image_soul_v2) from the
TEXT-ONLY prompts above. **No source photo of any person was used as input.** Job IDs,
kept so provenance is auditable:

| File | Higgsfield job |
|---|---|
| air-conditioning.jpg | 0e31b256-ac38-47d2-be2d-b16092a7c879 |
| heating.jpg | 72534eb2-9533-42ff-b478-0b0510cfa2af |
| plumbing.jpg | 2a5ccaa7-b41c-4411-9aeb-677849a1a288 |
| drains.jpg | 0b3c5918-e341-4cb1-846f-3025f89b8df0 |
| water-heater.jpg | a3723174-0e8f-4c4c-ba25-f2b8e0f96efa |
| air-quality.jpg | 3569334b-f681-4a3f-af0f-c645d78a2977 |
| why-team.jpg | da67b543-99da-4dca-aff5-0f6b0506b972 |

The old re-skinned files (repair*.png, maintenance*.png, installation*.png, tuneup*.png,
garage.png) remain quarantined here for reference only. Do not use them on any page.

---

# GENERATED 2026-07-14 (round 2) - equipment set + section backgrounds

User feedback: the technician set's uniform is not Sunny's real branding, so the tiles
now use EQUIPMENT-ONLY shots (no people, no uniform question). The people set is kept
as `team-*.jpg` for a possible logo-branded redo later. All text-only prompts, no
source images. Higgsfield `soul_2` job IDs:

| File | Job |
|---|---|
| services/air-conditioning.jpg (condenser) | 83845b7e-e3b9-43c5-8256-238d06544209 |
| services/heating.jpg (furnace/air handler) | 27671279-3cf4-4e03-af6e-a18ed206fe5d |
| services/plumbing.jpg (faucet) | 289982c3-2ed2-4749-9051-82b151a313c7 |
| services/drains.jpg (drain machine) | 19ff9bed-808d-4073-95a3-a1495ce2039c |
| services/water-heater.jpg (tank + tankless) | 479c47f9-457c-4a24-bf54-f3eda9f023bf |
| services/air-quality.jpg (filter + vent) | acb97dcf-e489-43f4-8973-934415e55de2 |
| bg/wasatch.jpg (neighborhood + mountains) | b5d9ca12-620e-4532-b5c2-220190d57d26 |
| bg/tools.jpg (tool flat-lay) | 60bd23f3-0f98-4f57-bd40-4579cbab295e |

---

# GENERATED 2026-07-14 (round 3) - unbranded equipment, Utah cues, logo uniform

User feedback: no branded equipment, Utah location feel, and the Why Choose Us photo
should wear the real Sunny logo. All Higgsfield, no third-party source images.

| File | Job | Note |
|---|---|---|
| services/air-conditioning.jpg | 03317c5b-6df8-48c2-9f5b-0271b246c35e | condenser, Wasatch peaks |
| services/heating.jpg | ec48b6c5-ac8b-47ba-82ef-1f11acff8afb | text-scrub edit of 78af24b2 |
| services/plumbing.jpg | dbe0be0c-ae71-4be1-808f-e1ee10d0761d | faucet, foothills window |
| services/drains.jpg | 968d07c4-3c8f-4d9f-a4a6-2d5299f92617 | text-scrub edit of 7b74c50f |
| services/water-heater.jpg | 1815bf95-6dd5-429f-8a8d-551722549bc0 | text-scrub edit of 18f6b42f |
| services/air-quality.jpg | 4182a63d-99a5-4219-a6d0-bc6fb32ec460 | filter + blank thermostat |
| services/why-team.jpg | 2d3815e6-06fa-465e-9091-17f96d92921c | Sunny logo added to OUR generated photo (da67b543) using the client's own brand-logo.png as reference. Clean provenance: generated person + client's own logo. |

Lesson: soul_2 invents gibberish brand text on equipment even when told not to.
The reliable recipe is generate, then run a nano_banana_pro edit: "remove ALL text,
letters, stickers, labels, badges and logos from every surface."
