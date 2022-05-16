// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef XDIGITAL_SETUP_H
#define XDIGITAL_SETUP_H

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
#include "xdigital_setup_hw.h"

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
} XDigital_setup_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XDigital_setup;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XDigital_setup_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XDigital_setup_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XDigital_setup_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XDigital_setup_ReadReg(BaseAddress, RegOffset) \
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
int XDigital_setup_Initialize(XDigital_setup *InstancePtr, u16 DeviceId);
XDigital_setup_Config* XDigital_setup_LookupConfig(u16 DeviceId);
int XDigital_setup_CfgInitialize(XDigital_setup *InstancePtr, XDigital_setup_Config *ConfigPtr);
#else
int XDigital_setup_Initialize(XDigital_setup *InstancePtr, const char* InstanceName);
int XDigital_setup_Release(XDigital_setup *InstancePtr);
#endif


void XDigital_setup_Set_gain(XDigital_setup *InstancePtr, u32 Data);
u32 XDigital_setup_Get_gain(XDigital_setup *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
