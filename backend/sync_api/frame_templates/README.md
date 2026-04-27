Place optional frame reference images here to improve uptie recognition.

Create subfolders named `uptie1`, `uptie2`, `uptie3`, and `uptie4`, then add cropped frame samples from your screenshots. The recognizer resizes each template to the extracted card-frame signature and compares it with template matching.

Use just the frame, not the full identity card.

The reason is in services.py:329 and services.py:361: the live screenshot card is converted into a border-only signature by zeroing the inner area, then the matcher compares that against your template. Since the template image is loaded directly and not masked the same way, including portrait art, name text, or level text in the template will add noise and usually make matching worse.

Best format:

Crop the full outer card rectangle so the border shape is preserved.
Remove or avoid most of the interior art/text.
Keep the decorative edges, corners, glow, and border pattern.
Use several samples per uptie if the frame style varies by rarity or lighting.
If you want the safest manual approach, make templates that look like:

the whole card outline is present
the center is mostly black, transparent, or tightly cropped away
only the frame and corner ornaments remain