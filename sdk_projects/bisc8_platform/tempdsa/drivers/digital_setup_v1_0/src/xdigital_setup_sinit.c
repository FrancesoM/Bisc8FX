// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#include "xparameters.h"
#include "xdigital_setup.h"

extern XDigital_setup_Config XDigital_setup_ConfigTable[];

XDigital_setup_Config *XDigital_setup_LookupConfig(u16 DeviceId) {
	XDigital_setup_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XDIGITAL_SETUP_NUM_INSTANCES; Index++) {
		if (XDigital_setup_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XDigital_setup_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XDigital_setup_Initialize(XDigital_setup *InstancePtr, u16 DeviceId) {
	XDigital_setup_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XDigital_setup_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XDigital_setup_CfgInitialize(InstancePtr, ConfigPtr);
}

#endif

