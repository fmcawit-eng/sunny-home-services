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

---

# GENERATED 2026-07-14 (round 4) - service-recognizable + fully clean

| File | Job | Note |
|---|---|---|
| services/heating.jpg | 2b90fed1-2e37-4dc0-806d-cedabf0717b6 | furnace w/ visible burner flame; text-scrub of 26666ba7 |
| services/drains.jpg | 09f4fb35-b75c-4266-ab48-d23efaf7cc36 | drum auger cable into cleanout; text-scrub of be52c24e |
| services/why-team.jpg | 443a5e90-71fd-453a-a5b0-7789daa99d5a | belt clutter removed from 2d3815e6 |

Confirmed recipe: soul_2 ALWAYS invents gibberish brand text on equipment, so every
equipment shot needs the nano_banana_pro "remove ALL text..." edit pass afterward.

---

# GENERATED 2026-07-14 (round 5) - clear product-style tiles + van number fix

Switched tile generation to nano_banana_pro text-to-image: it follows "no text"
reliably (soul_2 does not) and produces cleaner product-style compositions.

| File | Job |
|---|---|
| services/air-conditioning.jpg | fa3b6608-8952-483b-8ffd-93c58511efe0 |
| services/heating.jpg | ffa579bc-2116-4abf-9077-0eb26137d2d1 |
| services/plumbing.jpg | 4505ce10-65bb-443c-8d52-871863b72f1d |
| services/drains.jpg | 08dbed42-4490-448c-944b-9d48303ee76f |
| services/water-heater.jpg | b4d4f066-07b4-4c55-b42b-c87c34c7ca7c |
| services/air-quality.jpg | cc7ae432-a37e-47bb-bcda-4a42939ff233 |
| van2-current.jpg | 8df36e82-f90e-440a-ac94-4723675ce7a2 - phone on the wrap updated from 801.649.COOL (2665) to 801.887.9650 (edit of the client's own van photo). Original preserved as van2.png. |

hero2.mp4: re-encoded with a 2.5s hold on the final frame (logo) via ffmpeg tpad.
Original preserved as hero2-original.mp4.

---

# GENERATED 2026-07-15 (round 6) - technicians in BRANDED Sunny uniform

Final direction per user: technicians in the proper branded uniform. Each is a
nano_banana_pro edit of OUR OWN round-1 technician generation, adding the client's
own brand-logo.png as a chest patch + cap mark. Clean provenance throughout.

| File | Job (edit of) |
|---|---|
| services/air-conditioning.jpg | 2539fc6c (0e31b256) |
| services/heating.jpg | 750ab739 (72534eb2) |
| services/plumbing.jpg | dbca933b (2a5ccaa7) |
| services/drains.jpg | b4e56e88 (0b3c5918) |
| services/water-heater.jpg | bc87ed8f (11f0c1a1, + tank text scrub) |
| services/air-quality.jpg | ebbc9960 (3569334b) |

---

# GENERATED 2026-07-15 (round 7) - wide-angle branded set + 4:3 van

Single-step recipe discovered: nano_banana_pro text-to-image WITH brand-logo.png as a
reference image renders the branded uniform directly (no separate logo-edit pass).

| File | Job | Angle |
|---|---|---|
| services/air-conditioning.jpg | bdb9bbae | low three-quarter, backyard + Wasatch |
| services/heating.jpg | c6d55ea6 | over-the-shoulder, mechanical room |
| services/plumbing.jpg | f16e5ba5 | doorway into kitchen |
| services/drains.jpg | 7f7a7334 | high angle, side yard |
| services/water-heater.jpg | 718b2839 | side profile, garage corner |
| services/air-quality.jpg | 07eaec73 | low angle, hallway |
| van2-current.jpg | 88a8f875 | outpainted to 4:3 so cover fills the About band with the whole van in frame |

## Round 8 - Hub page imagery (2026-07-14)

All nano_banana_pro (model id resolves to nano_banana_2), text2image with brand-logo.png
(media c2af1527-3e81-4b77-991d-d4d73ad4e47b) as the logo reference for any technician shot;
equipment-only shots are plain text prompts. Heroes 16:9, cards 4:3. One generation per slot.

### Cooling (air-conditioner.html)
- heroes/cooling.jpg - d1254f1d-bb57-4d89-9208-458af57b7b69 (tech at condenser, brick home, Wasatch backdrop)
- services/card-ac-repair.jpg - f0a7d19e-c701-4749-9802-060dec4c71a5 (gauges on condenser)
- services/card-ac-maintenance.jpg - 743faee8-ec5e-41b0-aaa0-04ae50fb3aeb (coil rinse)
- services/card-ac-install.jpg - 79c733db-2e53-4b85-a3ce-12487c9f05a4 (two techs setting new unit; clean SUNNY back print)
- services/card-ac-emergency.jpg - 60353540-5e01-44c6-be61-85255e738f52 (dusk arrival)
- split reuses services/air-conditioning.jpg (round 7)

### Heating (heating.html)
- heroes/heating.jpg - 10e1d339-aed0-4728-9b40-51bb15bd4b7c (furnace inspection, utility room)
- services/card-heating-install.jpg - ba8ef6ad-3ecb-4ce9-8336-0fc5c2ca01f... (ba8ef6ad-3ecb-4ce9-8336-e0fc5c2ca01f) (two techs, new furnace)
- services/card-heating-repair.jpg - 01057a4c-6ebe-404c-a8c5-095a6835b145 (multimeter diagnosis)
- services/card-heating-maintenance.jpg - adaac655 base, FIXED by edit 1e943257-1673-49eb-98e2-c20fb98e4c2c
  (original had an Amazon-branded box on the shelf; edit replaced boxes with plain cartons)
- services/card-heating-emergency.jpg - 2e2dbdd8-537d-4eec-89ef-65c2e0e54d2a (snowy night walk-up)
- splits reuse services/heating.jpg + services/team-heating.jpg (rounds 6-7)

### Mini Splits (mini-splits.html)
- heroes/mini-splits.jpg - a37725f0-c828-4064-9f31-2961ce08949b (living room, wall unit, tech on step stool)
- services/minisplit-system.jpg - 87e8efc5-cf96-4fff-b069-23760a7bd12a (outdoor unit on bracket, no people)
- services/card-ms-install.jpg - d46fd8a8-fff2-4145-b352-9be886dcde58
- services/card-ms-repair.jpg - 23e01a6e-f63b-4643-a6a9-688b4ed47e65
- services/card-ms-maintenance.jpg - 8ac0db8b-9698-452e-a8a8-a863e13b4858

### Heat Pumps (heat-pumps.html)
- heroes/heat-pumps.jpg - 3607cc73-c85a-4a56-afe5-50abf4299053 (unit in snow, Wasatch, no people)
- services/heatpump-service.jpg - fb10acda base, logo cleaned by edit 1526e87c-3d13-48f3-9f7e-fdb996c70522
  (jacket back patch re-rendered from the logo reference)

### Indoor Air Quality (indoor-air-quality.html)
- heroes/indoor-air-quality.jpg - aecea83d base, FIXED by edit 7c22de8d-a9d7-4c89-b26c-11c1fc217ac6
  (removed a floating holographic screen artifact)
- services/card-iaq-duct-cleaning.jpg - REGENERATED as 2c1f429c-b0b4-4238-a7c1-455bf234fc3d
  (first take 463be6c5 had gibberish cap text "ELANY"; logo-patch edit 21b05635 did not fix it;
  final take frames the tech from behind with the logo on the shirt back - back prints render reliably)
- services/card-iaq-ductwork.jpg - 70d237f6-fe53-4260-8585-d517b87bfedc (no people)
- services/card-iaq-humidifier.jpg - ae11526c-7ec8-4306-b16f-71f44eaa2fb4 (no people)
- services/card-iaq-dehumidifier.jpg - c655890f-9e27-4d21-96e8-6aa36df45c73 (no people)
- services/card-iaq-uv.jpg - 7acdedb5-2130-4a6d-a146-e1ff19b5177f (no people)
- filtration card reuses services/air-quality.jpg (round 7)

### Lessons this round
- Editing garbled text ON CLOTHING rarely converges; regenerating with the logo on the
  SHIRT BACK (tech facing away) is the reliable recipe.
- nano_banana edit calls default to 3:4 portrait - ALWAYS pass aspect_ratio explicitly
  when editing a 4:3/16:9 source or the crop shifts.
- Watch for third-party props (Amazon boxes) in utility-room scenes; scrub with a
  "plain unmarked boxes" edit.

## Round 9 - Child pages + index promotion (2026-07-14)

All nano_banana_pro text2image with brand-logo.png reference (media c2af1527-3e81-4b77-991d-d4d73ad4e47b),
16:9 heroes, technicians working the page's exact service in branded Sunny uniform, wide angle,
"logo printed large and clean across his upper back" phrasing used where the back faces camera
(back prints render reliably; front cap patches occasionally garble at close range but heroes sit
under the 0.42-opacity teal overlay).

- heroes/ac-repair.jpg - f1a56bf0-dc67-4e0a-a507-38ab29abdee2 (multimeter at open condenser panel)
- heroes/ac-installation.jpg - 9f10e7a4-a548-4fe4-83dc-cfaec2d3c270 (two techs, hand truck, new pad; clean SUNNY back print)
- heroes/ac-maintenance.jpg - e240ecf3-459e-464c-8277-d0a86dc8fdf3 (gauges + tablet tune-up)
- heroes/emergency-ac-repair.jpg - 1d3db169-84ce-4ca0-8fe7-17168601378f (dusk work-light repair, back print)
- heroes/furnace-repair.jpg - aa8145c5-0a4b-485e-97ad-e46c47dc1703 (igniter replacement, utility room)
- heroes/furnace-installation.jpg - 81870c20-7463-40ef-bf53-f3fdac2af287 (two techs setting new furnace, back print)
- heroes/furnace-maintenance.jpg - 5d125c65-9241-4b0e-8503-2151606cc02c (combustion analyzer tune-up)
- heroes/emergency-heating-repair.jpg - 04c3862d-fe95-4f64-b105-e584cf12c654 (night no-heat call, back print)
- services/heating-work.jpg - 81feca76-5714-4f88-92e1-d4ea293a9b64 (4:3; replaces team-heating.jpg on heating.html)

Retired from the repo this round (git history keeps them): the AI re-skin quarantine
(repair/repair2/installation/installation2/maintenance/maintenance2/tuneup/tuneup2/garage .png),
van.png + van2.png (old phone number; van2-current.jpg with 801.887.9650 is the only van asset),
and map.png (Ogden pin). team-*.jpg close-up set kept on disk but no longer referenced by any page.

## Round 10 - Black uniform correction (2026-07-15)

BRAND RULE (permanent): Sunny technician uniforms are BLACK - black polo, black cap/beanie,
black winter jacket, blue hexagon Sunny logo patch. The round-7 homepage set and why-team.jpg
were already correct; rounds 8-9 were generated in light gray by mistake and all 26 technician
images were recolored via nano_banana_pro edits (source job + logo ref, aspect_ratio pinned,
prompt: "Change the technician's light-gray polo shirt and light-gray cap to a solid BLACK work
polo and BLACK cap... keep the Sunny Home Services logo patch clearly readable").

Recolor edit job IDs (target <- edit):
- heroes/cooling.jpg <- 63a225f3 | heroes/heating.jpg <- 81a44399 | heroes/mini-splits.jpg <- 5f22bd03
- heroes/indoor-air-quality.jpg <- a8298c2d | services/heatpump-service.jpg <- fb211c9e (navy->black jacket)
- services/heating-work.jpg <- 426e187d
- card-ac-repair <- 457c14a7 | card-ac-maintenance <- 1b2d3b82 | card-ac-install <- 3f2666e7
- card-ac-emergency <- c50c60f2 | card-heating-install <- 8fbca7e4 | card-heating-repair <- 33687f2b
- card-heating-maintenance <- 6ccdb217 | card-heating-emergency <- 25c5a33d (tan->black jacket)
- card-ms-install <- ee3efb7b | card-ms-repair <- 9f674d0b | card-ms-maintenance <- aa2a4720
- card-iaq-duct-cleaning <- c69cd87f
- heroes/ac-repair <- 87ad00ea | heroes/ac-installation <- a049dd91 | heroes/ac-maintenance <- 6b60b4a1
- heroes/emergency-ac-repair <- f6a7a133 | heroes/furnace-repair <- 46943be7
- heroes/furnace-installation <- ea7705aa | heroes/furnace-maintenance <- 28b4af6d
- heroes/emergency-heating-repair <- ad1f5475

26 edits x 2 credits = 52 credits. Recolor edits preserve composition and logos reliably;
this is the cheapest fix for a wardrobe-color mistake (vs regenerating).

## Round 11 - Service Area page (2026-07-15)
- heroes/service-area.jpg - 7d50101e-a8fc-461c-846b-64deae9a8581 (golden-hour aerial of a Wasatch Front
  neighborhood, no people/text; also reused as the coming-soon.html hero). Text-only prompt, 2 credits.
