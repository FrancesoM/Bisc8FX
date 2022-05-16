#include "ap_axi_sdata.h"
#include <hls_stream.h>

void pwm_scaling(
      hls::stream< ap_axis<16,0,0,0> >& din,
      hls::stream< ap_axis<16,0,0,0> >& dout,
	  unsigned int pwm_max_val)
{
#pragma HLS INTERFACE axis port=dout
#pragma HLS INTERFACE axis port=din
#pragma HLS INTERFACE s_axilite port=pwm_max_val

	// We have an incoming stream of data, from -32768 to 32767,
	// but the PWM expects unsigned data, from 0 to 4095

	// Why int? Because we need more bits when background shifting in case we overflow

	scale: do{
#pragma HLS PIPELINE
			int 			in_signed = din.read().data;

			// Anyway we keep it as int to account more bits for the pwm rescaling multiplication
			unsigned int    in_unsigned_bounded;
			unsigned short	out_unsigned;

			// The signal now must be clipped before converting to unsigned
			in_signed = in_signed + 32768;
			in_signed = in_signed >= 65534 ? 65534 : in_signed;
			in_signed = in_signed < 0 ? 0 : in_signed;

			// Safe conversion to unsigned
			in_unsigned_bounded = (unsigned int)in_signed;

			// PWM rescaling (shift saves us a dsp for division)
			in_unsigned_bounded = ( in_unsigned_bounded*pwm_max_val ) >> 16;

			// Clip PWM between 0 and max (??)

			ap_axis<16,0,0,0> out_signal;
			out_signal.data = (unsigned short)in_unsigned_bounded;

			dout.write(out_signal);
	}while(1);

}
