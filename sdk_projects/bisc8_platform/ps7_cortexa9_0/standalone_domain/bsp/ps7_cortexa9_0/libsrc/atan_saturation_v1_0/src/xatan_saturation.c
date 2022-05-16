// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
/***************************** Include Files *********************************/
#include "xatan_saturation.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XAtan_saturation_CfgInitialize(XAtan_saturation *InstancePtr, XAtan_saturation_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XAtan_saturation_Set_active_saturation(XAtan_saturation *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XAtan_saturation_WriteReg(InstancePtr->Control_BaseAddress, XATAN_SATURATION_CONTROL_ADDR_ACTIVE_SATURATION_DATA, Data);
}

u32 XAtan_saturation_Get_active_saturation(XAtan_saturation *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XAtan_saturation_ReadReg(InstancePtr->Control_BaseAddress, XATAN_SATURATION_CONTROL_ADDR_ACTIVE_SATURATION_DATA);
    return Data;
}

