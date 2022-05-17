############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
############################################################
open_project atan_saturation_prj
set_top atan_saturation
add_files srcs/saturation_lut.h
add_files srcs/main.cpp
open_solution "atan_saturation_solution" -flow_target vivado
set_part {xc7z020-clg400-1}
create_clock -period 10 -name default
config_export -format ip_catalog -rtl verilog -vivado_clock 10
source "./atan_saturation_prj/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
