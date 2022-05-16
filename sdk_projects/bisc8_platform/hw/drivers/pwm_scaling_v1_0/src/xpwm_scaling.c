// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
/***************************** Include Files *********************************/
#include "xpwm_scaling.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XPwm_scaling_CfgInitialize(XPwm_scaling *InstancePtr, XPwm_scaling_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XPwm_scaling_Set_pwm_max_val(XPwm_scaling *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XPwm_scaling_WriteReg(InstancePtr->Control_BaseAddress, XPWM_SCALING_CONTROL_ADDR_PWM_MAX_VAL_DATA, Data);
}

u32 XPwm_scaling_Get_pwm_max_val(XPwm_scaling *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XPwm_scaling_ReadReg(InstancePtr->Control_BaseAddress, XPWM_SCALING_CONTROL_ADDR_PWM_MAX_VAL_DATA);
    return Data;
}

