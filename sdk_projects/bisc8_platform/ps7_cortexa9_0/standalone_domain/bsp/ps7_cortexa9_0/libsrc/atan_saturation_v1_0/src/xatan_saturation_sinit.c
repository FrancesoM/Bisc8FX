// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#include "xparameters.h"
#include "xatan_saturation.h"

extern XAtan_saturation_Config XAtan_saturation_ConfigTable[];

XAtan_saturation_Config *XAtan_saturation_LookupConfig(u16 DeviceId) {
	XAtan_saturation_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XATAN_SATURATION_NUM_INSTANCES; Index++) {
		if (XAtan_saturation_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XAtan_saturation_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XAtan_saturation_Initialize(XAtan_saturation *InstancePtr, u16 DeviceId) {
	XAtan_saturation_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XAtan_saturation_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XAtan_saturation_CfgInitialize(InstancePtr, ConfigPtr);
}

#endif

