/*******************************************************************************
Vendor: Xilinx
Associated Filename: example.cpp
Purpose: AXI stream interface example for Vivado HLS using side channel data
Revision History: February 13, 2012 - initial release

*******************************************************************************
#-  (c) Copyright 2011-2018 Xilinx, Inc. All rights reserved.
#-
#-  This file contains confidential and proprietary information
#-  of Xilinx, Inc. and is protected under U.S. and
#-  international copyright and other intellectual property
#-  laws.
#-
#-  DISCLAIMER
#-  This disclaimer is not a license and does not grant any
#-  rights to the materials distributed herewith. Except as
#-  otherwise provided in a valid license issued to you by
#-  Xilinx, and to the maximum extent permitted by applicable
#-  law: (1) THESE MATERIALS ARE MADE AVAILABLE "AS IS" AND
#-  WITH ALL FAULTS, AND XILINX HEREBY DISCLAIMS ALL WARRANTIES
#-  AND CONDITIONS, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
#-  BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, NON-
#-  INFRINGEMENT, OR FITNESS FOR ANY PARTICULAR PURPOSE; and
#-  (2) Xilinx shall not be liable (whether in contract or tort,
#-  including negligence, or under any other theory of
#-  liability) for any loss or damage of any kind or nature
#-  related to, arising under or in connection with these
#-  materials, including for any direct, or any indirect,
#-  special, incidental, or consequential loss or damage
#-  (including loss of data, profits, goodwill, or any type of
#-  loss or damage suffered as a result of any action brought
#-  by a third party) even if such damage or loss was
#-  reasonably foreseeable or Xilinx had been advised of the
#-  possibility of the same.
#-
#-  CRITICAL APPLICATIONS
#-  Xilinx products are not designed or intended to be fail-
#-  safe, or for use in any application requiring fail-safe
#-  performance, such as life-support or safety devices or
#-  systems, Class III medical devices, nuclear facilities,
#-  applications related to the deployment of airbags, or any
#-  other applications that could lead to death, personal
#-  injury, or severe property or environmental damage
#-  (individually and collectively, "Critical
#-  Applications"). Customer assumes the sole risk and
#-  liability of any use of Xilinx products in Critical
#-  Applications, subject only to applicable laws and
#-  regulations governing limitations on product liability.
#-
#-  THIS COPYRIGHT NOTICE AND DISCLAIMER MUST BE RETAINED AS
#-  PART OF THIS FILE AT ALL TIMES.
#- ************************************************************************


This file contains confidential and proprietary information of Xilinx, Inc. and
is protected under U.S. and international copyright and other intellectual
property laws.

DISCLAIMER
This disclaimer is not a license and does not grant any rights to the materials
distributed herewith. Except as otherwise provided in a valid license issued to
you by Xilinx, and to the maximum extent permitted by applicable law:
(1) THESE MATERIALS ARE MADE AVAILABLE "AS IS" AND WITH ALL FAULTS, AND XILINX
HEREBY DISCLAIMS ALL WARRANTIES AND CONDITIONS, EXPRESS, IMPLIED, OR STATUTORY,
INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, NON-INFRINGEMENT, OR
FITNESS FOR ANY PARTICULAR PURPOSE; and (2) Xilinx shall not be liable (whether
in contract or tort, including negligence, or under any other theory of
liability) for any loss or damage of any kind or nature related to, arising under
or in connection with these materials, including for any direct, or any indirect,
special, incidental, or consequential loss or damage (including loss of data,
profits, goodwill, or any type of loss or damage suffered as a result of any
action brought by a third party) even if such damage or loss was reasonably
foreseeable or Xilinx had been advised of the possibility of the same.

CRITICAL APPLICATIONS
Xilinx products are not designed or intended to be fail-safe, or for use in any
application requiring fail-safe performance, such as life-support or safety
devices or systems, Class III medical devices, nuclear facilities, applications
related to the deployment of airbags, or any other applications that could lead
to death, personal injury, or severe property or environmental damage
(individually and collectively, "Critical Applications"). Customer assumes the
sole risk and liability of any use of Xilinx products in Critical Applications,
subject only to applicable laws and regulations governing limitations on product
liability.

THIS COPYRIGHT NOTICE AND DISCLAIMER MUST BE RETAINED AS PART OF THIS FILE AT
ALL TIMES.

*******************************************************************************/
#include "digital_setup.h"

#include "atan_lut_almost_linear.h"

static ap_int<ACC_WIDTH>        s32_acc = 0;
static ap_uint<HISTORY_LEN_BITS> idx = 0;
static ap_uint<HISTORY_LEN_BITS> last_idx = 1; // It's basically 1 bwyond the current idx due to circular nature

void digital_setup(
      hls::stream< pkt_t >& din,
      hls::stream< pkt_t >& dout,
	  int gain)
{
#pragma HLS INTERFACE mode=s_axilite port=gain
#pragma HLS INTERFACE axis port=dout
#pragma HLS INTERFACE axis port=din
	// Assumption is that the ADC input is centered at 2048 thanks to analog conditioning

	// We want to remove the DC offset and center the signal around zero, to do so use a moving average approach and we remove
	// the average to each sample. This lifts us from the burden of selecting an arbitrary offset value.
	static ap_int<DATA_WIDTH> as16_history[HISTORY_LEN];
	#pragma HLS ARRAY_PARTITION variable=as16_history cyclic factor=2

	//First we shift it and then we remove the average, meaning we output a signed val
	ap_uint<DATA_WIDTH>  u16_adc_in;

	// We need a bigger precision data
	// TODO: in theory we could have a custom datatype, 18bits should suffice
	ap_int<ACC_WIDTH> s32_adc_in;

	int last_sample = 0;

#pragma HLS PIPELINE
		pkt_t pkt_in = din.read();
 		u16_adc_in = pkt_in.data;
		last_sample = pkt_in.last;

		// Rescale because the first 4 bits from ADC are not meaningful
		u16_adc_in = u16_adc_in >> 4;

		// update history and index. this is needed only to have the "last" value
		as16_history[idx] = ap_int<DATA_WIDTH>(u16_adc_in);

		s32_acc = s32_acc + u16_adc_in - as16_history[last_idx];

		// Subtract the background level (offset from opamp) and obtain a zero centered signal
		// This division ( for the average) needs to be an arithmetic shift... I hope it'll be
		s32_adc_in  = ((ap_int<ACC_WIDTH>)u16_adc_in) - ( s32_acc >> HISTORY_LEN_BITS ) ;

		s32_adc_in = s32_adc_in*gain;

		// Why clipping at 12bits? The PWM will take care of a more gentle rescaling
		// So clip at 16bits signed -> [ - 32768 : 32767 ]
		s32_adc_in = s32_adc_in >= (ap_int<ACC_WIDTH>)(32767) ? (ap_int<ACC_WIDTH>)(32767)  : s32_adc_in;
		s32_adc_in = s32_adc_in < (ap_int<ACC_WIDTH>)(-32768) ? (ap_int<ACC_WIDTH>)(-32768) : s32_adc_in;

		ap_int<DATA_WIDTH> s16_armonized = atan_lut_almost_linear[unsigned( s32_adc_in + (1<<15) ) ];

		ap_axis<DATA_WIDTH,0,0,0> out_signal;
		out_signal.data = s16_armonized;

		idx = (idx+1)&(HISTORY_LEN-1); //Modulo operation when D is power of 2; // Change this to shift modulo operation
		last_idx = (last_idx+1)&(HISTORY_LEN-1); //Modulo operation when D is power of 2

		dout.write(out_signal);

}


/*
  for(i = 0; i < STREAM_DEPTH-1; i++){
	  B[i].data = A[i].data;
	   B[i].keep = A[i].keep;
	   B[i].strb = A[i].strb;
	   B[i].last = 0;
   }

  //Tlast on the STREAM_DEPTHth packet
  B[STREAM_DEPTH-1].data = A[STREAM_DEPTH-1].data;
   B[STREAM_DEPTH-1].keep = A[STREAM_DEPTH-1].keep;
   B[STREAM_DEPTH-1].strb = A[STREAM_DEPTH-1].strb;
   B[STREAM_DEPTH-1].last = 1;
}
*/

