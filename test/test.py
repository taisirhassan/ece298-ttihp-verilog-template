# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Initialize signals
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 1  # Not in reset initially

    # Wait for initial stabilization
    await ClockCycles(dut.clk, 2)

    # Reset the design
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)  # Wait for the clock edge after reset is released

    # Test normal counting - first cycle after reset should increment to 1
    dut._log.info("Test normal counting")
    await ClockCycles(dut.clk, 1)
    count1 = int(dut.uo_out.value)
    dut._log.info(f"Count after 1 cycle: {count1}")
    assert count1 == 1, f"Expected count=1, got {count1}"
    
    await ClockCycles(dut.clk, 1)
    count2 = int(dut.uo_out.value)
    dut._log.info(f"Count after 2 cycles: {count2}")
    assert count2 == 2, f"Expected count=2, got {count2}"
    
    # Test loading value - set up load operation properly
    dut._log.info("Test loading value")
    
    # Set up the load value
    dut.uio_in.value = 0x42  # Base count = 0x42 (66 decimal)
    
    # Go to the falling edge before load, then set load high
    await FallingEdge(dut.clk)
    dut.ui_in.value = 1  # Set load = 1
    
    # Wait for the next rising edge where the load happens
    await RisingEdge(dut.clk)
    
    # Wait for the next falling edge to see the result
    await FallingEdge(dut.clk)
    
    # Read the counter value
    count_after_load = int(dut.uo_out.value)
    dut._log.info(f"Count after load: {count_after_load}")
    assert count_after_load == 0x42, f"Expected count=0x42, got {count_after_load}"
    
    # Clear load signal before moving on
    dut.ui_in.value = 0  # Clear load
    
    # Continue counting from loaded value
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    count_after_continue = int(dut.uo_out.value)
    dut._log.info(f"Count after continue: {count_after_continue}")
    assert count_after_continue == 0x43, f"Expected count=0x43, got {count_after_continue}"
    
    # Test tri-state enable
    dut._log.info("Test tri-state enable")
    await FallingEdge(dut.clk)
    dut.ui_in.value = 2  # Set tri_state_enable = 1
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    count_with_tri = int(dut.uo_out.value)
    oe_value = int(dut.uio_oe.value)
    dut._log.info(f"Count with tri-state enabled: {count_with_tri}, OE value: {oe_value}")
    assert count_with_tri == 69, f"Expected count=69, got {count_with_tri}"
    assert oe_value == 0xFF, f"Expected all outputs enabled (0xFF), got {oe_value}"
    
    # Test reset
    dut._log.info("Test reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)  # Wait for the reset to take effect
    await FallingEdge(dut.clk)  # Check results after falling edge
    count_after_reset = int(dut.uo_out.value)
    dut._log.info(f"Count after reset: {count_after_reset}")
    assert count_after_reset == 0, f"Expected count=0 after reset, got {count_after_reset}"
    
    # Test overflow
    dut._log.info("Test overflow")
    # Set up for loading 0xFF
    dut.uio_in.value = 0xFF  # Base count = 0xFF (255 decimal)
    await FallingEdge(dut.clk)
    dut.ui_in.value = 1  # Set load = 1
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    count_max = int(dut.uo_out.value)
    dut._log.info(f"Count at max: {count_max}")
    assert count_max == 0xFF, f"Expected count=0xFF, got {count_max}"
    
    # Clear load signal
    dut.ui_in.value = 0  # Clear load
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    count_overflow = int(dut.uo_out.value)
    dut._log.info(f"Count after overflow: {count_overflow}")
    assert count_overflow == 0, f"Expected count=0 after overflow, got {count_overflow}"
