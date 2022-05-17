#ifndef ATAN_SATURATION_H
#define ATAN_SATURATION_H

#include "ap_axi_sdata.h"
#include <hls_stream.h>

#include "ap_int.h"

#define DATA_WIDTH 16
#define ACC_WIDTH 32

typedef ap_axis<DATA_WIDTH, 0, 0, 0> pkt_t;

void atan_saturation(
	      hls::stream< pkt_t >& din,
	      hls::stream< pkt_t >& dout,
	  ap_int<16> atan_lut_memory[65536],
	  int active_saturation);

#endif
