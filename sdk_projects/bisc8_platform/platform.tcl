# 
# Usage: To re-create this platform project launch xsct with below options.
# xsct C:\Users\francesco.maio\Desktop\Bisc8FX\sdk_projects\bisc8_platform\platform.tcl
# 
# OR launch xsct and run below command.
# source C:\Users\francesco.maio\Desktop\Bisc8FX\sdk_projects\bisc8_platform\platform.tcl
# 
# To create the platform in a different location, modify the -out option of "platform create" command.
# -out option specifies the output directory of the platform project.

platform create -name {bisc8_platform}\
-hw {C:\Users\francesco.maio\Desktop\Bisc8FX\sdk_projects\xsa\dsp_chain_220509.xsa}\
-proc {ps7_cortexa9_0} -os {standalone} -out {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects}

platform write
platform generate -domains 
platform active {bisc8_platform}
platform generate
domain active {zynq_fsbl}
bsp reload
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/dsp_chain_mos3v3.xsa}
platform clean
platform clean
platform generate
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/dsp_chain_220509.xsa}
platform clean
platform generate
platform clean
platform generate
platform clean
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/dsp_ila.xsa}
platform generate
platform clean
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/bisc8_locked.xsa}
platform generate
platform clean
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/BISC8_DRP.xsa}
platform generate
platform clean
platform config -updatehw {C:/Users/francesco.maio/Desktop/Bisc8FX/sdk_projects/xsa/BISC8_DBG_v0.xsa}
platform generate
platform clean
platform clean
