WriteCoach iOS sound fix
========================
Copy index.html and the assets folder into your existing website directory (merge/overwrite as appropriate).
Keep your existing phrase.txt and favicon.svg files; they are not included here.
The app has a renamed JavaScript bundle to avoid cached script reuse.

Changes:
- Set navigator.audioSession.type = "playback" where available (iOS silent mode).
- Support AudioContext or webkitAudioContext.
- Reuse a single audio context and resume it after an incorrect letter tap.
- Slightly raise volume and duration of the 180 Hz error tone.

WebKit bugs may still prevent audio in some home screen web apps. Test the site directly in Safari if needed.
