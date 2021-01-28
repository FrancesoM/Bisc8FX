############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2018 Xilinx, Inc. All Rights Reserved.
############################################################
open_project -reset signal_conditioning
set_top digital_conditioning
add_files pre_process/pre_process.cpp
open_solution "pre_process"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
config_compile -no_signed_zeros=0 -unsafe_math_optimizations=0
config_export -description {Condition signal to meet further processing. ADC data is shifted to get the meaningful 12bits and brought to a 0 centered, amplified signed signal.} -display_name digital_conditioning -format ip_catalog -rtl verilog -vivado_phys_opt place -vivado_report_level 0
#source "./signal_conditioning/pre_process/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog -description "Condition signal to meet further processing. ADC data is shifted to get the meaningful 12bits and brought to a 0 centered, amplified signed signal. " -display_name "digital_conditioning"
