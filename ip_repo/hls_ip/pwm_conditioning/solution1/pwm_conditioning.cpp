#include "ap_axi_sdata.h"
#include <hls_stream.h>

void pwm_conditioning(
      hls::stream< ap_axis<16,0,0,0> >& din,
      hls::stream< ap_axis<16,0,0,0> >& dout,
	  int offset_cal )
{
#pragma HLS INTERFACE axis port=dout
#pragma HLS INTERFACE axis port=din
#pragma HLS INTERFACE s_axilite port=offset_cal


	// We have an incoming stream of data, from -2048 to 2047,
	// but the PWM expects unsigned data, from 0 to 4095

	short 			in_signed = din.read().data;
	unsigned short	out_unsigned;

	// The signal now must be clipped before converting to unsigned
	in_signed = in_signed + offset_cal; //This background level must be set through an axi reg eventually
	in_signed = in_signed >= 4095 ? 4095 : in_signed;
	in_signed = in_signed < 0 ? 0 : in_signed;

	//Clip
	out_unsigned = (unsigned short)in_signed;

	ap_axis<16,0,0,0> out_signal;
	out_signal.data = out_unsigned;

	dout.write(out_signal);

}
