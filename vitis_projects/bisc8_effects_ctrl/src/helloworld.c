/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "sleep.h"
#include "xtime_l.h"

#include "PWM_generator.h"
#include "xpwm_scaling.h"
#include "xdigital_setup.h"
#include "xil_cache.h"
#include "xatan_saturation.h"
#include "stream_monitor.h"

#include "xbram.h"
#include "atan_lut_steep_0.h"
#include "atan_lut_steep_1.h"
#include "atan_lut_steep_2.h"
#include "atan_lut_steep_3.h"

#include "xaxidma.h"

#define FS_HZ (41810.0f)


// Accomodate 20 seconds of recording at 16bits per 42kHz
#define NSAMPLES (20*42000*2)
__attribute__((section(".debug_axis0"))) unsigned char debug_axis0[NSAMPLES];
__attribute__((section(".debug_axis1"))) unsigned char debug_axis1[NSAMPLES];

// Processing IPs
XPwm_scaling pwmScal;
XDigital_setup digSetup;
XAtan_saturation atanSat;

// Memories
XBram bramInst;

// Monitoring IPs
XAxiDma dma0;
XAxiDma dma1;

int init_dma(XAxiDma* p_dma_inst, int dma_device_id)
{

	XAxiDma_Config* cfg_ptr;
	int status;

	cfg_ptr = XAxiDma_LookupConfig(dma_device_id);
	if (!cfg_ptr)
	{
		xil_printf("ERROR! No hardware configuration found for AXI DMA with device id %d.\r\n", dma_device_id);
		return -1;
	}

	status = XAxiDma_CfgInitialize(p_dma_inst, cfg_ptr);
	if (status != XST_SUCCESS)
	{
		xil_printf("ERROR! Initialization of AXI DMA failed with %d\r\n", status);
		return -1;
	}

	// Test for Scatter Gather
	if (XAxiDma_HasSg(p_dma_inst))
	{
		xil_printf("ERROR! Device configured as SG mode.\r\n");
		return -1;
	}

	// Disable interrupts for both channels
	XAxiDma_IntrDisable(p_dma_inst, XAXIDMA_IRQ_ALL_MASK, XAXIDMA_DEVICE_TO_DMA);
	XAxiDma_IntrDisable(p_dma_inst, XAXIDMA_IRQ_ALL_MASK, XAXIDMA_DMA_TO_DEVICE);

	// Reset DMA
	XAxiDma_Reset(p_dma_inst);
	while (!XAxiDma_ResetIsDone(p_dma_inst)) {}

	return 0;


}

void init_peripherals()
{
	XDigital_setup_Initialize(&digSetup,XPAR_DIGITAL_SETUP_0_DEVICE_ID);
	XDigital_setup_Set_gain(&digSetup,300);

	XPwm_scaling_Initialize(&pwmScal, XPAR_PWM_SCALING_0_DEVICE_ID);
	XPwm_scaling_Set_pwm_max_val(&pwmScal,2048);

	XAtan_saturation_Initialize(&atanSat,XPAR_ATAN_SATURATION_0_DEVICE_ID);
	XAtan_saturation_Set_active_saturation(&atanSat,1);

	PWM_GENERATOR_mWriteReg(XPAR_PWM_GENERATOR_0_S00_AXI_BASEADDR,0,2047);

	XBram_Config* bramCfg;
	bramCfg = XBram_LookupConfig(XPAR_AXI_BRAM_CTRL_0_DEVICE_ID);

	// Here I only care about bramInst.MemBaseAddress or I could use directly XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR
	XBram_CfgInitialize(&bramInst,bramCfg,XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR);

	// Load one saturation table
	UINTPTR Addr = bramInst.Config.MemBaseAddress;
	for( int i = 0; i < (1<<16) ; i+=2 )
	{
		unsigned int w2bram;
		short MSB = atan_lut_steep_0[i+1];
		short LSB = atan_lut_steep_0[i];
		unsigned int   MSB_shifted = ((unsigned int)MSB)<<16;

		// Tricky, if you don't mask LSB the sign extend of a negative number will cover the MSB_Shifted
		w2bram = (unsigned int)MSB_shifted | ( ( (unsigned int) LSB) & 0xffff ) ;

		*(unsigned int*)Addr  = w2bram;
		Addr+=4;
	}

	// Now init the DMAs
	init_dma(&dma0, XPAR_AXI_DMA_0_DEVICE_ID);
	init_dma(&dma1, XPAR_AXI_DMA_1_DEVICE_ID);

};

int dma_begin_collect_data(XAxiDma* p_dma_inst, int num_bytes, unsigned char* dest)
{

		// Local variables
		int       status    = 0;

		// Flush cache

		Xil_DCacheFlushRange((UINTPTR)dest, num_bytes);

		// Kick off S2MM transfer
		status = XAxiDma_SimpleTransfer
		(
			p_dma_inst,
			(UINTPTR)dest,
			num_bytes,
			XAXIDMA_DEVICE_TO_DMA
		);
		if (status != XST_SUCCESS)
		{
			xil_printf("ERROR! Failed to kick off S2MM transfer!\n\r");
			return -1;
		}

		return 0;
}

int dma_wait_completion(XAxiDma* p_dma_inst)
{
		// Wait for transfer to complete
		while (XAxiDma_Busy(p_dma_inst, XAXIDMA_DEVICE_TO_DMA)) {}

		// Check DMA for errors
		if ((XAxiDma_ReadReg(p_dma_inst->RegBase, XAXIDMA_RX_OFFSET+XAXIDMA_SR_OFFSET) & XAXIDMA_IRQ_ERROR_MASK) != 0)
		{
			xil_printf("ERROR! AXI DMA returned an error during the S2MM transfer.\n\r");
			return -1;
		}

		return 0;

}

void acquire_data_blocking()
{

    int start_flag;
	XTime tEnd, tCur;

	// How many samples to capture
	float seconds_to_acquire = 10.0f;
	int   samples_to_acquire   = (int)( seconds_to_acquire * FS_HZ );
	int   bytes_to_acquire     = samples_to_acquire*2;

	// Configure the stream monitor
	STREAM_MONITOR_mWriteReg(	XPAR_STREAM_MONITOR_0_S00_AXI_BASEADDR,
								0,
								samples_to_acquire);

	STREAM_MONITOR_mWriteReg(	XPAR_STREAM_MONITOR_1_S00_AXI_BASEADDR,
								0,
								samples_to_acquire);


	// Arm the DMAs - Then they will wait for a valid transaction
	dma_begin_collect_data(&dma0, bytes_to_acquire, debug_axis0);
	dma_begin_collect_data(&dma1, bytes_to_acquire, debug_axis1);

	// Start count - down
    xil_printf("Start acquisition in..\n 3 \n");
    sleep(1);
    xil_printf(" 2 \n");
    sleep(1);
    xil_printf(" 1 \n");
    sleep(1);
	xil_printf("Acquiring %d bytes to 0x%x and 0x%x...\n",bytes_to_acquire,debug_axis0,debug_axis1);

	XTime_GetTime(&tCur);

	// Launch the stream monitor - This will begin the valid transaction and put tlast after "samples_to_acquire" transactions
	int flag0 = STREAM_MONITOR_mReadReg(XPAR_STREAM_MONITOR_0_S00_AXI_BASEADDR,4);
	int flag1 = STREAM_MONITOR_mReadReg(XPAR_STREAM_MONITOR_0_S00_AXI_BASEADDR,4);

	// We need to toggle the flag to start the monitor
	flag0 ^= 1;
	flag1 ^= 1;

	STREAM_MONITOR_mWriteReg(	XPAR_STREAM_MONITOR_0_S00_AXI_BASEADDR,
								4,
								flag0);

	STREAM_MONITOR_mWriteReg(	XPAR_STREAM_MONITOR_1_S00_AXI_BASEADDR,
								4,
								flag1);

	// And now we wait for the DMA to finish - This should last the same seconds we have defined before
	dma_wait_completion(&dma0);
	dma_wait_completion(&dma1);



	XTime_GetTime(&tEnd);

	float seconds = (float)(tEnd - tCur) / (float) COUNTS_PER_SECOND;

	xil_printf("Acquisition done : %d seconds \n\n",(int)seconds);

	xil_printf("First 10 samples monitor 0: \n");
	for (int k = 0; k < 10 ; k++)
	{
		xil_printf(" %d - ", *( ( (short*)debug_axis0) + k ));
	}

	xil_printf("\n");
}

void set_gain_blocking()
{


	volatile char gain;

    int G;

	xil_printf("Select gain: \n a) 200 \n b) 250 \n c) 350 \n d) 500\n");

	gain = (unsigned) inbyte();
	while( gain < 65) { gain = (unsigned) inbyte(); };
	switch(gain){
	case 'a':
		G = 200;
		break;
	case 'b':
		G = 250;
		break;
	case 'c':
		G = 350;
		break;
	case 'd':
		G = 500;
		break;
	}

	xil_printf("Selected gain: %d\n",(unsigned)G);

	XDigital_setup_Set_gain(&digSetup,G);

}

void set_saturation_table_blocking()
{
    short *satLUT_ptr;
    int write_bram = 0;

    volatile char sat_level;

	xil_printf("Select saturation Level: \n n) NO saturation \n a) 1 \n b) 2 \n c) 3 \n d) 4\n");

	sat_level = (unsigned) inbyte();
	write_bram = 0;
	while( sat_level < 65) { sat_level = (unsigned) inbyte(); };
	switch(sat_level){
		case 'n':
			XAtan_saturation_Set_active_saturation(&atanSat,0);
			break;
		case 'a':
			XAtan_saturation_Set_active_saturation(&atanSat,1);
			satLUT_ptr = atan_lut_steep_0;
			write_bram = 1;
			break;
		case 'b':
			XAtan_saturation_Set_active_saturation(&atanSat,1);
			satLUT_ptr = atan_lut_steep_1;
			write_bram = 1;
			break;
		case 'c':
			XAtan_saturation_Set_active_saturation(&atanSat,1);
			satLUT_ptr = atan_lut_steep_2;
			write_bram = 1;
			break;
		case 'd':
			XAtan_saturation_Set_active_saturation(&atanSat,1);
			satLUT_ptr = atan_lut_steep_3;
			write_bram = 1;
			break;
		}

	xil_printf("Selected saturation: %c\n",sat_level);

	if( write_bram == 1  ){

		// Load one saturation table
		UINTPTR Addr = bramInst.Config.MemBaseAddress;
		for( int i = 0; i < (1<<16) ; i+=2 )
		{
			unsigned int w2bram;
			short MSB = satLUT_ptr[i+1];
			short LSB = satLUT_ptr[i];
			unsigned int   MSB_shifted = ((unsigned int)MSB)<<16;

			// Tricky, if you don't mask LSB the sign extend of a negative number will cover the MSB_Shifted
			w2bram = (unsigned int)MSB_shifted | ( ( (unsigned int) LSB) & 0xffff ) ;

			*(unsigned int*)Addr  = w2bram;
			Addr+=4;
		}

	}
}

int main()
{
    init_platform();

    //Disable cache otherwise we won't be able to see data written from PL
    Xil_DCacheDisable();

    init_peripherals();

    setvbuf(stdin, NULL, _IONBF, 0);
    volatile char cmd;

	xil_printf("\nSelect what to do:\n a) Acquire \n g) Change gain \n s) Enable overdrive \n");
	cmd = inbyte();
	while( cmd != 'g' && cmd != 'a' && cmd != 's'){ cmd = inbyte(); };

    while(1) {

    	switch( cmd )
    	{
			case 'a':
				acquire_data_blocking();
			break;

			case 'g':
				set_gain_blocking();
			break;

			case 's':
				set_saturation_table_blocking();
			break;
    	}

		//Clean serial
		setvbuf(stdin, NULL, _IONBF, 0);

		xil_printf("\nSelect what to do:\n a) Acquire \n g) Change gain \n s) Enable overdrive \n");

		cmd = inbyte();
		while( cmd != 'g' && cmd != 'a' && cmd != 's'){ cmd = inbyte(); };
		//while(inbyte() != 0x61);
		setvbuf(stdin, NULL, _IONBF, 0);

    };

    cleanup_platform();
    return 0;
}
