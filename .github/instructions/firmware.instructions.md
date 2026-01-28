---
applyTo: "omi/**/*.{c,h,cpp,hpp},omiGlass/**/*.{c,h,cpp,hpp,ino}"
excludeAgent: "code-review"
---

## Firmware (Omi / OmiGlass) instructions

- Prefer the existing firmware architecture and patterns. Keep changes minimal and focused.
- Be careful with BLE protocol and audio pipeline correctness; regressions can break the Capture layer.
- Maintain codec compatibility (Opus preferred; don’t assume only one codec exists).
- Format C/C++ changes with `clang-format` when relevant.

### References

- BLE protocol spec: `docs/doc/developer/Protocol.mdx`

