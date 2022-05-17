############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
############################################################
open_project digital_setup
set_top digital_setup
add_files srcs/atan_lut_almost_linear.h
add_files srcs/digital_setup.cpp
add_files srcs/digital_setup.h
add_files -tb srcs/digital_setup_test.cpp -cflags "-Wno-unknown-pragmas" -csimflags "-Wno-unknown-pragmas"
open_solution "digital_setup_prj" -flow_target vivado
set_part {xc7z020-clg400-1}
create_clock -period 10 -name default
config_export -format ip_catalog -rtl verilog -vendor Francesco -version 1.0
source "./digital_setup_prj/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -rtl verilog -format ip_catalog -vendor "Francesco"
