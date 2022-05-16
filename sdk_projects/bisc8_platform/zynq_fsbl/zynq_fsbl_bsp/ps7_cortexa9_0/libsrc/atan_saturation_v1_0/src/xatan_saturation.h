// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef XATAN_SATURATION_H
#define XATAN_SATURATION_H

#ifdef __cplusplus
extern "C" {
#endif

/***************************** Include Files *********************************/
#ifndef __linux__
#include "xil_types.h"
#include "xil_assert.h"
#include "xstatus.h"
#include "xil_io.h"
#else
#include <stdint.h>
#include <assert.h>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stddef.h>
#endif
#include "xatan_saturation_hw.h"

/**************************** Type Definitions ******************************/
#ifdef __linux__
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;
#else
typedef struct {
    u16 DeviceId;
    u32 Control_BaseAddress;
} XAtan_saturation_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XAtan_saturation;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XAtan_saturation_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XAtan_saturation_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XAtan_saturation_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XAtan_saturation_ReadReg(BaseAddress, RegOffset) \
    *(volatile u32*)((BaseAddress) + (RegOffset))

#define Xil_AssertVoid(expr)    assert(expr)
#define Xil_AssertNonvoid(expr) assert(expr)

#define XST_SUCCESS             0
#define XST_DEVICE_NOT_FOUND    2
#define XST_OPEN_DEVICE_FAILED  3
#define XIL_COMPONENT_IS_READY  1
#endif

/************************** Function Prototypes *****************************/
#ifndef __linux__
int XAtan_saturation_Initialize(XAtan_saturation *InstancePtr, u16 DeviceId);
XAtan_saturation_Config* XAtan_saturation_LookupConfig(u16 DeviceId);
int XAtan_saturation_CfgInitialize(XAtan_saturation *InstancePtr, XAtan_saturation_Config *ConfigPtr);
#else
int XAtan_saturation_Initialize(XAtan_saturation *InstancePtr, const char* InstanceName);
int XAtan_saturation_Release(XAtan_saturation *InstancePtr);
#endif


void XAtan_saturation_Set_active_saturation(XAtan_saturation *InstancePtr, u32 Data);
u32 XAtan_saturation_Get_active_saturation(XAtan_saturation *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
