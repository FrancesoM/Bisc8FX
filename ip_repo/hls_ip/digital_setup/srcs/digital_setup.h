#ifndef DIGITAL_SETUP_H
#define DIGITAL_SETUP_H

#include "ap_axi_sdata.h"
#include "ap_int.h"
#include <hls_stream.h>

#define HISTORY_LEN 512
#define HISTORY_LEN_BITS 9

#define DATA_WIDTH 16
#define ACC_WIDTH 32

typedef ap_axis<DATA_WIDTH, 0, 0, 0> pkt_t;


void digital_setup(
	      hls::stream< pkt_t >& din,
	      hls::stream< pkt_t >& dout,
		  int gain);

#endif
