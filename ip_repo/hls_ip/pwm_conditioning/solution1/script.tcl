############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2018 Xilinx, Inc. All Rights Reserved.
############################################################
open_project pwm_conditioning
set_top pwm_conditioning
add_files pwm_conditioning/solution1/pwm_conditioning.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
config_export -description {From signed signal processing to PWM data format} -display_name PWM_conditioning -format ip_catalog -rtl verilog
#source "./pwm_conditioning/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog -description "From signed signal processing to PWM data format" -display_name "PWM_conditioning"
