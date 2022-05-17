############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
############################################################
open_project pwm_scaling_prj
set_top pwm_scaling
add_files srcs/main.cpp
open_solution "pwm_scaling_solution" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10 -name default
source "./pwm_scaling_prj/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
