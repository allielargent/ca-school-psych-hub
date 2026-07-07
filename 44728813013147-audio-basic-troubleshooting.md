---
id: 44728813013147
brand: "Parallel Help Center"
brand_id: 7011641908507
locale: "en-us"
title: "Audio Basic Troubleshooting"
category: "School Tech Support Hub"
section: "Troubleshooting Common Technical Issues"
labels: ["Windows", "Mac", "Audio"]
author: "Josiah Callaway"
created_at: "2025-12-23T16:17:10Z"
updated_at: "2026-05-19T13:20:29Z"
url: "https://help.parallellearning.com/hc/en-us/articles/44728813013147-Audio-Basic-Troubleshooting"
---
# Audio Basic Troubleshooting

## **Windows: The Quick Fixes**

**1. Check the "Speaker Selection"**

Windows often tries to send sound to the wrong place (like a monitor that doesn't have speakers).

* Click the **Speaker Icon** in the bottom right corner of your taskbar.
* Click the **small arrow** (or the name of the device) next to the volume bar.
* Try every option in that list. One of them is likely your actual speakers.

**2. The "Off and On" for Sound**

Sometimes the software that runs your sound gets "tired" and needs a nudge.

1. Right-click the **Start button** and select **Device Manager**.
2. Find **Sound, video and game controllers** and click the little arrow to open it.
3. Right-click your sound device (usually "Realtek" or "High Definition Audio").
4. Select **Disable device**, wait 5 seconds, then right-click it again and select **Enable device**.

**3. Update Drivers**

If you are still having issues after following the above steps, it could be a sound driver issue. You can look at [this guide](https://help.parallellearning.com/hc/en-us/articles/44204506013211-Sound-Drivers) to help with that!

---

## **Mac: The Quick Fixes**

**1. The "Sound Output" Check**

If you have headphones or a monitor plugged in, your Mac might be confused about where to send the audio.

* Click the **Apple Menu ()** > **System Settings** (or System Preferences).
* Click **Sound** and then the **Output** tab.
* Make sure the correct device is highlighted. Also, ensure the **Mute** box at the bottom isn't checked!

**2. Refresh the Audio Engine (No Restart Required)**

If the sound is glitchy or the volume buttons don't work, you can "reset" the sound system without restarting your whole computer.

1. Press **Command + Space** on your keyboard and type **Activity Monitor**, then hit Enter.
2. In the search bar at the top right, type `coreaudiod`.
3. Click on the result that appears.
4. Click the **X** at the top of the window and select **Force Quit**. *Don't worry—your Mac will immediately restart the sound system automatically.*

---

## **For Both: The Physical Check**

Before you assume the computer is broken, check these three "silent killers" of audio:

* **The Mute Key:** Look at the very top row of your keyboard. Is there a light on the "Mute" key (usually F1 or F10)?
* **The Wrong Plug:** If you use a desktop, ensure your speakers are plugged into the **Green** port, not the Pink (Microphone) or Blue (Line In) ports.
* **The Hub:** If your speakers are plugged into a USB hub or "dongle," try plugging them directly into the computer instead.
