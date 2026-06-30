# Hero background video

Drop a factory / automation / robotics clip here as `hero.mp4`, then enable it
in your `.env`:

```
HERO_VIDEO_URL=video/hero.mp4
HERO_VIDEO_POSTER=img/hero-poster.jpg   # optional still frame shown while loading
```

Guidelines for a good hero loop:
- 8-20 second seamless loop, no audio, 1920x1080, H.264 MP4.
- Keep it under ~5-8 MB (compress with HandBrake) so the page stays fast.
- Darker / slower footage works best behind white text.

Free, license-cleared sources: Pexels Videos, Coverr, Mixkit (download the MP4,
put it here). For an EXTERNAL URL instead of a local file, set
`HERO_VIDEO_URL=https://...` and add that host to `media-src` in
`config/settings/base.py` (CSP).

When `HERO_VIDEO_URL` is empty, the hero falls back to the animated
circuit-grid + AI-network graphic (no video). Nothing breaks if no file is set.
