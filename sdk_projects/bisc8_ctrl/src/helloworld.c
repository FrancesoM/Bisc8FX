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
#include "PWM_generator.h"
#include "xpwm_scaling.h"
#include "xdigital_setup.h"
#include "axis_gather_tdata.h"
#include "xil_cache.h"
#include "xatan_saturation.h"

#define ASCII_SERIAL
#define N_SAMPLES ((1<<18)-1)

__attribute__((section(".debug_axis"))) unsigned int debug_axis[N_SAMPLES];

XPwm_scaling pwmScal;
XDigital_setup digSetup;
XAtan_saturation atanSat;

void init_peripherals()
{
	XDigital_setup_Initialize(&digSetup,XPAR_DIGITAL_SETUP_0_DEVICE_ID);
	XDigital_setup_Set_gain(&digSetup,300);

	XPwm_scaling_Initialize(&pwmScal, XPAR_PWM_SCALING_0_DEVICE_ID);
	XPwm_scaling_Set_pwm_max_val(&pwmScal,2048);

	XAtan_saturation_Initialize(&atanSat,XPAR_ATAN_SATURATION_0_DEVICE_ID);
	XAtan_saturation_Set_active_saturation(&atanSat,1);

	PWM_GENERATOR_mWriteReg(XPAR_PWM_GENERATOR_0_S00_AXI_BASEADDR,0,2047);

};

int main()
{
    init_platform();

    //Disable cache otherwise we won't be able to see data written from PL
    Xil_DCacheDisable();

    init_peripherals();

    //print("Hello World\n\r");

    setvbuf(stdin, NULL, _IONBF, 0);
    volatile char cmd;
    volatile char gain;

#ifdef ASCII_SERIAL
    		xil_printf("\nSelect what to do:\n a) Acquire \n g) Change gain \n s) Enable overdrive \n");
#endif
	cmd = inbyte();
	while( cmd != 'g' && cmd != 'a' && cmd != 's'){ cmd = inbyte(); };

    int G;
    int start_flag;

    while(1) {

    	switch( cmd )
    	{
    	case 'a':

#ifdef ASCII_SERIAL
    		xil_printf("Acquiring data...");
#endif
        	// Start the monitoring IP by toggling bit on the REG_SLV0
        	start_flag = AXIS_GATHER_TDATA_mReadReg(XPAR_AXIS_GATHER_TDATA_0_S00_AXI_BASEADDR,0);
        	AXIS_GATHER_TDATA_mWriteReg(XPAR_AXIS_GATHER_TDATA_0_S00_AXI_BASEADDR,0,start_flag^1);

        	//xil_printf("Waiting to finish..\n");
        	while( ( ( AXIS_GATHER_TDATA_mReadReg(XPAR_AXIS_GATHER_TDATA_0_S00_AXI_BASEADDR,0) & (0b10) ) >> 1) != 1   )
        	{
        	};
        	//xil_printf("..Done\n");

#ifdef ASCII_SERIAL
    			unsigned short* pDataAxi1 = (unsigned  short*)debug_axis;
    			xil_printf("Starting at address: %08x \n",pDataAxi1);
    			for (int j = 0; j < 10 ; j+=4) { // Send only 10 samples instead of N_SAMPLES, for debug purposes and to not keep the serial port busy forever
    				unsigned  short Axi1 = *(pDataAxi1 + j);
    				xil_printf("%04x\n",Axi1);
    				// verbose xil_printf("%d: %d @ %08x \n",j,readval,pData+j);
    				}
#else //BYTE_SERIAL
    			unsigned char* pByteAxi1 = (unsigned  char*)debug_axis;
    			// Multiply by 4 because we want to send each char (one data byte at a time)
    			for (int j = 0; j < N_SAMPLES; j++) {
    				// Just because I don't know how to send one byte without printf
    				xil_printf("%c",*( ((unsigned  char*)debug_axis)+(4*j)));
    				xil_printf("%c",*( ((unsigned  char*)debug_axis)+(4*j)+1));
    				}
#endif

    #ifdef ASCII_SERIAL
    			unsigned short* pDataAxi2 = (unsigned  short*)&debug_axis;
    			xil_printf("Starting at address: %08x \n",pDataAxi2);
    			for (int j = 0; j < N_SAMPLES ; j+=4) {
    				unsigned  short Axi2 = *(pDataAxi2 + j + 1 );
    				xil_printf("%04x\n",Axi2);
    				// verbose xil_printf("%d: %d @ %08x \n",j,readval,pData+j);
    				}
    #else //BYTE_SERIAL
    			unsigned char* pByteAxi2 = (unsigned  char*)&debug_axis;
    			// Multiply by 4 because we want to send each char (one data byte at a time)
    			for (int j = 0; j < N_SAMPLES; j++) {
    				// Just because I don't know how to send one byte without printf
    				xil_printf("%c",*(((unsigned  char*)debug_axis)+(4*j)+2));
    				xil_printf("%c",*(((unsigned  char*)debug_axis)+(4*j)+3));
    				}
    #endif


#ifdef ASCII_SERIAL
        	print("Acquisition done\n");
#endif
    	break;

    	case 'g':
#ifdef ASCII_SERIAL
    		xil_printf("Select gain: \n a) 200 \n b) 250 \n c) 350 \n d) 500\n");
#endif
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
#ifdef ASCII_SERIAL
    		xil_printf("Selected gain: %d\n",(unsigned)G);
#endif
    		XDigital_setup_Set_gain(&digSetup,G);


    	break;

    	case 's':
    		XAtan_saturation_Set_active_saturation(&atanSat,XAtan_saturation_Get_active_saturation(&atanSat)^1);
    	break;

    	}




		//Clean serial
		setvbuf(stdin, NULL, _IONBF, 0);
#ifdef ASCII_SERIAL
		xil_printf("\nSelect what to do:\n a) Acquire \n g) Change gain \n s) Enable overdrive \n");
#endif
		cmd = inbyte();
		while( cmd != 'g' && cmd != 'a' && cmd != 's'){ cmd = inbyte(); };
		//while(inbyte() != 0x61);
		setvbuf(stdin, NULL, _IONBF, 0);



    };

    cleanup_platform();
    return 0;
}
