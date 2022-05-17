#define STREAM_LENGTH 100

#include "digital_setup.h"
#include "stdio.h"

int main() {
  int err = 0;

  hls::stream<pkt_t  > inStream;
  hls::stream<pkt_t  > outStream;
  pkt_t   dataStream_in;
  pkt_t   dataStream_out;

  unsigned short temp;


  /* Load input data from files. All IPs here follow this structure:

  C:\Users\francesco.maio\Desktop\Bisc8FX\ip_repo\hls_ip\digital_setup\digital_setup_prj\csim\build

	Bisc8FX
	 |__ ip_repo
	 |      |
	 |      |__ hls_ip
 	 |		      |
 	 |		      |__ < ip >
  	 |					|
  	 |					|__  < ip solution >
  	 |					        |
  	 |					        |__ csim (C simulation )
  	 |							|	 |
  	 |                          |    |__ build <--- Here is where the C simulation runs
  	 | 							|
  	 |							|__ sim ( RTL- cosimulation )
	 |								 |
	 |								 |__ wrapc <--- Here is where the co-simulation runs
	 |
	 |__ utils
	     	|
	     	|__ raw_data


  */

  FILE *fp;
  fp=fopen("../../../../../../utils/raw_data/adc_stream_capture.dat","r");

  if( fp == NULL)
  {
	  printf("Can't open input file! \n");
	  return -1;
  }

  for (int i=0; i<200000; i++)
  {
	  fscanf(fp, "%d", &temp);
	  dataStream_in.data=temp;
	  inStream.write(dataStream_in);
  }

  fscanf(fp, "%d", &temp);
  dataStream_in.data=temp;
  dataStream_in.last=1;
  inStream.write(dataStream_in);

  fclose(fp);

  digital_setup(inStream,outStream,100);

  printf("\n Reading output stream..\n");

  fp=fopen("../../../../../../utils/raw_data/digital_setup_out.dat","w");

  if( fp == NULL)
  {
	  printf("Can't open output file! \n");
	  return -1;
  }

  while(!outStream.empty()) {

	  fprintf(fp,"%d\n", outStream.read().data.to_int());
  }

  fclose(fp);

  return err;
}
