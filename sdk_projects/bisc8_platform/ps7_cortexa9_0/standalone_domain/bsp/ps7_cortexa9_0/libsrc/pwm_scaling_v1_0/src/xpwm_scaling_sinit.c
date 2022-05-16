// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#include "xparameters.h"
#include "xpwm_scaling.h"

extern XPwm_scaling_Config XPwm_scaling_ConfigTable[];

XPwm_scaling_Config *XPwm_scaling_LookupConfig(u16 DeviceId) {
	XPwm_scaling_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XPWM_SCALING_NUM_INSTANCES; Index++) {
		if (XPwm_scaling_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XPwm_scaling_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XPwm_scaling_Initialize(XPwm_scaling *InstancePtr, u16 DeviceId) {
	XPwm_scaling_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XPwm_scaling_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XPwm_scaling_CfgInitialize(InstancePtr, ConfigPtr);
}

#endif

