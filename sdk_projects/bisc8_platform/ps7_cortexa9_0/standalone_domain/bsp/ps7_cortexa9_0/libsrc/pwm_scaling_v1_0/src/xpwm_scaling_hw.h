// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
// control
// 0x00 : reserved
// 0x04 : reserved
// 0x08 : reserved
// 0x0c : reserved
// 0x10 : Data signal of pwm_max_val
//        bit 31~0 - pwm_max_val[31:0] (Read/Write)
// 0x14 : reserved
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XPWM_SCALING_CONTROL_ADDR_PWM_MAX_VAL_DATA 0x10
#define XPWM_SCALING_CONTROL_BITS_PWM_MAX_VAL_DATA 32

