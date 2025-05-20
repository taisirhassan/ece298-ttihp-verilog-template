# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0             # Load = 0, tri_state_enable = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Test normal counting
    dut._log.info("Test normal counting")
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 1, f"Expected count=1, got {dut.uo_out.value}"
    
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 2, f"Expected count=2, got {dut.uo_out.value}"
    
    # Test loading value
    dut._log.info("Test loading value")
    dut.uio_in.value = 0x42         # Base count = 0x42 (66 decimal)
    dut.ui_in.value = 1             # Set load = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x42, f"Expected count=0x42, got {dut.uo_out.value}"
    
    # Continue counting from loaded value
    dut.ui_in.value = 0             # Set load = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x43, f"Expected count=0x43, got {dut.uo_out.value}"
    
    # Test tri-state enable
    dut._log.info("Test tri-state enable")
    dut.ui_in.value = 2             # Set tri_state_enable = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x44, f"Expected count=0x44, got {dut.uo_out.value}"
    assert dut.uio_oe.value == 0xFF, f"Expected all outputs enabled"
    
    # Test reset
    dut._log.info("Test reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    assert dut.uo_out.value == 0, f"Expected count=0 after reset, got {dut.uo_out.value}"
    
    # Test overflow
    dut._log.info("Test overflow")
    dut.uio_in.value = 0xFF         # Base count = 0xFF (255 decimal)
    dut.ui_in.value = 1             # Set load = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0xFF, f"Expected count=0xFF, got {dut.uo_out.value}"
    
    dut.ui_in.value = 0             # Set load = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Expected count=0 after overflow, got {dut.uo_out.value}"
