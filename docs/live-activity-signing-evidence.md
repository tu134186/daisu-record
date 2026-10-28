# Live Activity rendering investigation — 2026-10-28

## Confirmed evidence

- Device screenshot IMG_3246 shows Activity.request succeeded for Build47, with a nonempty Activity ID. This establishes creation, not rendering or registration.
- Released Build47 IPA SHA256: 148312bdcdbff7fc1e543c4578fbbdeeadacff6b56c8e5a3b754a75797fdc5e7.
- Parsed the actual embedded CarIdleWidget Mach-O LC_CODE_SIGNATURE: three slots, no XML entitlements slot. Both package signing commands used codesign --force --sign - without --entitlements.
- IPA metadata says DTXcode=1640, SDK iphoneos18.5, minimum iOS16.2 for both bundles. Xcode26-specific reports do not directly explain this build.
- WidgetBundle does explicitly instantiate IdleWidget(). No missing entry was found.
- Timer interval uses finite dates, not Date infinity. The reported infinity-timer issue is not present.
- Car image is 1024x1024 (151923 compressed bytes); memory exhaustion is not established.

## Primary sources reviewed

1. Apple DTS: https://developer.apple.com/forums/thread/822724 — Activity ID can exist while no matching ActivityConfiguration is exposed by extension entry. The report is iOS26; it establishes the distinction, not our root cause.
2. Apple forums: https://developer.apple.com/forums/thread/763594 — compiler/API compatibility reports. The original poster identified isActivityFullscreen; another poster identified infinity in a timer range. Neither exists here.
3. TrollStore installer: https://github.com/opa334/TrollStore/blob/main/RootHelper/main.m — fallback application-identifier / developer-team entitlements are supplied only to the main executable. Extensions with no entitlements start with an empty dictionary, then get container entitlements. Defaults use TROLLTROLL.
4. TrollStore registration: https://github.com/opa334/TrollStore/blob/main/RootHelper/uicache.m — plugin TeamIdentifier is constructed from its own signature entitlements, with owner bundle assigned separately.
5. TrollStore README: https://github.com/opa334/TrollStore — existing entitlements are preserved when applying its signing bypass.

## Targeted correction

Build48 supplies explicit application-identifier for each bundle and a common TROLLTROLL developer-team entitlement. TROLLTROLL is a TrollStore fallback identity, not a paid Apple Developer team. No platform/no-sandbox/debug entitlements added. Package verifies extracted signed entitlements and signature structure before release. Timer layout remains Build47.

This corrects a verified packaging omission and removes main/extension identity asymmetry under the inspected TrollStore installation path. It does NOT establish that identity omission is the sole cause on this phone; installed signature, registration, and rendering logs remain unobserved. No claim of device success.
