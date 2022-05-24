// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef XPWM_SCALING_H
#define XPWM_SCALING_H

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
#include "xpwm_scaling_hw.h"

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
} XPwm_scaling_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XPwm_scaling;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XPwm_scaling_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XPwm_scaling_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XPwm_scaling_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XPwm_scaling_ReadReg(BaseAddress, RegOffset) \
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
int XPwm_scaling_Initialize(XPwm_scaling *InstancePtr, u16 DeviceId);
XPwm_scaling_Config* XPwm_scaling_LookupConfig(u16 DeviceId);
int XPwm_scaling_CfgInitialize(XPwm_scaling *InstancePtr, XPwm_scaling_Config *ConfigPtr);
#else
int XPwm_scaling_Initialize(XPwm_scaling *InstancePtr, const char* InstanceName);
int XPwm_scaling_Release(XPwm_scaling *InstancePtr);
#endif


void XPwm_scaling_Set_pwm_max_val(XPwm_scaling *InstancePtr, u32 Data);
u32 XPwm_scaling_Get_pwm_max_val(XPwm_scaling *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
