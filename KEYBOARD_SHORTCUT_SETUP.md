# Keyboard Shortcut Setup for SnapTask

**Prerequisites:** Run `./install.sh` first to install the `snaptask` command.

There are three methods to set up a keyboard shortcut:

## Method 1: macOS Shortcuts App (Recommended - Easiest)

1. Open the **Shortcuts** app

2. Click the **"+"** button to create a new shortcut

3. Add action: **"Run Shell Script"**

4. Paste this command:
   ```bash
   snaptask
   ```

   Or for Vision mode:
   ```bash
   snaptask --vision
   ```

5. Click the **(i)** info button in the top right

6. Check **"Use as Quick Action"**

7. Add keyboard shortcut (e.g., **⌘⇧A** or **⌃⌥S**)

8. Name it **"SnapTask"**

## Method 2: BetterTouchTool (If you have it)

1. Add new keyboard shortcut

2. Set it to run shell script: `snaptask`

3. Optional: Add notification with: `snaptask && osascript -e 'display notification "Analyzed!" with title "SnapTask"'`

## Method 3: Alfred (If you have it)

1. Create new workflow

2. Add hotkey trigger

3. Connect to "Run Script" action with command: `snaptask`

4. Set language to `/bin/bash`

## Environment Setup

Make sure your OPENAI_API_KEY is accessible. Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Then reload:
```bash
source ~/.zshrc
```
