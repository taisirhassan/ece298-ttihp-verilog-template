/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  // Signal declarations
  reg [7:0] count;         // Internal counter register
  wire load;               // Load signal
  wire tri_state_enable;   // Tri-state output enable
  wire [7:0] base_count;   // Base count to load
  
  // Input mapping
  assign load = ui_in[0];              // Load signal
  assign tri_state_enable = ui_in[1];  // Tri-state output enable
  assign base_count = uio_in;          // 8-bit base count from uio_in
  
  // Synchronous counter with load functionality
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      // Reset counter to 0
      count <= 8'h00;
    end else begin
      if (load) begin
        // Load base count when load signal is active
        count <= base_count;
      end else begin
        // Normal operation: increment counter
        count <= count + 1'b1;
      end
    end
  end
  
  // Tri-state output control using bidirectional pins
  // When tri_state_enable is high, output is enabled
  // When tri_state_enable is low, pins are set as inputs
  assign uio_out = count;              // Counter value to bidirectional output
  assign uio_oe = {8{tri_state_enable}}; // Enable all 8 outputs when tri_state_enable is high
  
  // Regular output always shows the counter value
  assign uo_out = count;
  
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:2], 1'b0};

endmodule
