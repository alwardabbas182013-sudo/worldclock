# World Clock (Kivy) → APK build instructions

I can't compile the `.apk` for you in this chat (that needs the Android SDK/NDK
and network access, which this sandbox doesn't have), but this project is
ready to build on your own machine in ~15 minutes.

## 1. Test it on your computer first (fastest way to check it works)
```bash
pip install kivy pytz
python main.py
```
You should see a scrolling list of cities with live-updating clocks.

## 2. Build the actual APK (do this on Linux, or WSL on Windows)
Buildozer only runs on Linux/macOS. Easiest path on Windows: install WSL2 + Ubuntu.

```bash
sudo apt update
sudo apt install -y python3-pip build-essential git openjdk-17-jdk unzip
pip install buildozer cython

cd worldclock
buildozer android debug
```

First build takes 10-20 min (downloads Android SDK/NDK automatically).
The finished file appears at:
```
worldclock/bin/worldclock-1.0-armeabi-v7a-debug.apk
```

## 3. Install it on your phone
```bash
adb install bin/worldclock-*-debug.apk
```
Or just copy the .apk to your phone and tap it (enable "install from unknown sources").

## Files in this project
- `main.py` — the app (Kivy UI, list of 14 world cities, updates every second)
- `buildozer.spec` — build config (app name, permissions, target API)

## Want to customize?
- Add/remove cities: edit the `CITIES` list at the top of `main.py` (format: `("Display Name", "IANA/Timezone")`)
- Change colors/theme: happy to restyle it — just say the word
