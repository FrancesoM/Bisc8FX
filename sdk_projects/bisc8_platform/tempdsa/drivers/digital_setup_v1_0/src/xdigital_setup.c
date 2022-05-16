// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
/***************************** Include Files *********************************/
#include "xdigital_setup.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XDigital_setup_CfgInitialize(XDigital_setup *InstancePtr, XDigital_setup_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XDigital_setup_Set_gain(XDigital_setup *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XDigital_setup_WriteReg(InstancePtr->Control_BaseAddress, XDIGITAL_SETUP_CONTROL_ADDR_GAIN_DATA, Data);
}

u32 XDigital_setup_Get_gain(XDigital_setup *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XDigital_setup_ReadReg(InstancePtr->Control_BaseAddress, XDIGITAL_SETUP_CONTROL_ADDR_GAIN_DATA);
    return Data;
}

