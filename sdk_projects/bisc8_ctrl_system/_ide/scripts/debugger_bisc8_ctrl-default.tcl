# Usage with Vitis IDE:
# In Vitis IDE create a Single Application Debug launch configuration,
# change the debug type to 'Attach to running target' and provide this 
# tcl script in 'Execute Script' option.
# Path of this script: C:\Users\francesco.maio\Desktop\Bisc8FX\sdk_projects\bisc8_ctrl_system\_ide\scripts\debugger_bisc8_ctrl-default.tcl
# 
# 
# Usage with xsct:
# To debug using xsct, launch xsct and run below command
# source C:\Users\francesco.maio\Desktop\Bisc8FX\sdk_projects\bisc8_ctrl_system\_ide\scripts\debugger_bisc8_ctrl-default.tcl
# 
connect -url tcp:127.0.0.1:3121
targets -set -nocase -filter {name =~"APU*"}
rst -system
after 3000
targets -set -filter {jtag_cable_name =~ "Xilinx PYNQ-Z1 003017A40D21A" && level==0 && jtag_device_ctx=="jsn-Xilinx PYNQ-Z1-003017A40D21A-23727093-0"}
fpga -file C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/bisc8_ctrl/_ide/bitstream/top_wrapper.bit
targets -set -nocase -filter {name =~"APU*"}
loadhw -hw C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/bisc8_platform/export/bisc8_platform/hw/top_wrapper.xsa -mem-ranges [list {0x40000000 0xbfffffff}] -regs
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"}
source C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/bisc8_ctrl/_ide/psinit/ps7_init.tcl
ps7_init
ps7_post_config
targets -set -nocase -filter {name =~ "*A9*#0"}
dow C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/bisc8_ctrl/Debug/bisc8_ctrl.elf
configparams force-mem-access 0
bpadd -addr &main
