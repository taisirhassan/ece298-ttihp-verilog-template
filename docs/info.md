<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an 8-bit programmable synchronous counter with tri-state outputs. The counter increments by 1 with each clock cycle by default. It has the following features:

1. **Programmable**: The counter can be loaded with an 8-bit base value when the load signal is active.
2. **Synchronous**: All operations are synchronized with the clock.
3. **Tri-state outputs**: The output can be enabled or disabled using the tri-state enable signal.

The counter value is available on both the dedicated outputs (uo_out) and the tri-state bidirectional pins (uio_out) when the tri-state enable is active.

## How to test

The counter has the following inputs:
- `ui_in[0]`: Load signal - When high, the counter loads the base value from uio_in
- `ui_in[1]`: Tri-state enable - When high, the counter value is output on uio_out; when low, the uio_out pins are in input mode
- `uio_in[7:0]`: Base count - 8-bit value to load into the counter when load is high
- `rst_n`: Active low reset - Sets the counter to 0
- `clk`: Clock input - Counter increments on the rising edge

To test the counter:
1. Reset the counter by setting rst_n low, then high.
2. Observe the counter incrementing on uo_out[7:0] with each clock cycle.
3. Apply a value to uio_in[7:0] and pulse ui_in[0] high to load a new value.
4. Toggle ui_in[1] to enable/disable the tri-state outputs on uio_out[7:0].

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
