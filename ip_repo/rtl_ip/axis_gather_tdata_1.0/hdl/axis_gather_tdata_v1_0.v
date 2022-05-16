
`timescale 1 ns / 1 ps

	module axis_gather_tdata_v1_0 #
	(
		// Users to add parameters here
		// 18bits number gives us 6seconds of recording, enough to test an effect feeling
        parameter BITS_COUNTER = 18,
		// User parameters ends
		// Do not modify the parameters beyond this line


		// Parameters of Axi Master Bus Interface M00_AXI
		parameter  C_M00_AXI_START_DATA_VALUE	= 32'hAA000000,
		parameter  C_M00_AXI_TARGET_SLAVE_BASE_ADDR	= 32'h40000000,
		parameter integer C_M00_AXI_ADDR_WIDTH	= 32,
		parameter integer C_M00_AXI_DATA_WIDTH	= 32,
		parameter integer C_M00_AXI_TRANSACTIONS_NUM	= 4,

		// Parameters of Axi Slave Bus Interface S00_AXI
		parameter integer C_S00_AXI_DATA_WIDTH	= 32,
		parameter integer C_S00_AXI_ADDR_WIDTH	= 4
	)
	(
		// Users to add ports here
		input wire axis_valid_1,
		input wire axis_ready_1,
		input wire[15:0] axis_data1,

		input wire axis_valid_2,
		input wire axis_ready_2,
		input wire[15:0] axis_data2,
		// User ports ends
		// Do not modify the ports beyond this line


		// Ports of Axi Master Bus Interface M00_AXI
		output wire  m00_axi_error,
		output wire  m00_axi_txn_done,
		input wire  m00_axi_aclk,
		input wire  m00_axi_aresetn,
		output wire [C_M00_AXI_ADDR_WIDTH-1 : 0] m00_axi_awaddr,
		output wire [2 : 0] m00_axi_awprot,
		output wire  m00_axi_awvalid,
		input wire  m00_axi_awready,
		output wire [C_M00_AXI_DATA_WIDTH-1 : 0] m00_axi_wdata,
		output wire [C_M00_AXI_DATA_WIDTH/8-1 : 0] m00_axi_wstrb,
		output wire  m00_axi_wvalid,
		input wire  m00_axi_wready,
		input wire [1 : 0] m00_axi_bresp,
		input wire  m00_axi_bvalid,
		output wire  m00_axi_bready,
		output wire [C_M00_AXI_ADDR_WIDTH-1 : 0] m00_axi_araddr,
		output wire [2 : 0] m00_axi_arprot,
		output wire  m00_axi_arvalid,
		input wire  m00_axi_arready,
		input wire [C_M00_AXI_DATA_WIDTH-1 : 0] m00_axi_rdata,
		input wire [1 : 0] m00_axi_rresp,
		input wire  m00_axi_rvalid,
		output wire  m00_axi_rready,

		// Ports of Axi Slave Bus Interface S00_AXI
		input wire  s00_axi_aclk,
		input wire  s00_axi_aresetn,
		input wire [C_S00_AXI_ADDR_WIDTH-1 : 0] s00_axi_awaddr,
		input wire [2 : 0] s00_axi_awprot,
		input wire  s00_axi_awvalid,
		output wire  s00_axi_awready,
		input wire [C_S00_AXI_DATA_WIDTH-1 : 0] s00_axi_wdata,
		input wire [(C_S00_AXI_DATA_WIDTH/8)-1 : 0] s00_axi_wstrb,
		input wire  s00_axi_wvalid,
		output wire  s00_axi_wready,
		output wire [1 : 0] s00_axi_bresp,
		output wire  s00_axi_bvalid,
		input wire  s00_axi_bready,
		input wire [C_S00_AXI_ADDR_WIDTH-1 : 0] s00_axi_araddr,
		input wire [2 : 0] s00_axi_arprot,
		input wire  s00_axi_arvalid,
		output wire  s00_axi_arready,
		output wire [C_S00_AXI_DATA_WIDTH-1 : 0] s00_axi_rdata,
		output wire [1 : 0] s00_axi_rresp,
		output wire  s00_axi_rvalid,
		input wire  s00_axi_rready
	);


	reg[C_M00_AXI_DATA_WIDTH-1:0] axi_wdata;
	reg[C_M00_AXI_ADDR_WIDTH-1:0] axi_waddr; 

	wire[31:0] testrData;
	wire[31:0] testrAddr; 

	reg pulseInitWrite; 

	// Axi slave - signal to start
	wire[C_S00_AXI_DATA_WIDTH-1:0] s00_start_reg;
	reg s00_transfer_done;

// Instantiation of Axi Bus Interface M00_AXI
	axis_gather_tdata_v1_0_M00_AXI # ( 
		.C_M_START_DATA_VALUE(C_M00_AXI_START_DATA_VALUE),
		.C_M_TARGET_SLAVE_BASE_ADDR(C_M00_AXI_TARGET_SLAVE_BASE_ADDR),
		.C_M_AXI_ADDR_WIDTH(C_M00_AXI_ADDR_WIDTH),
		.C_M_AXI_DATA_WIDTH(C_M00_AXI_DATA_WIDTH),
		.C_M_TRANSACTIONS_NUM(C_M00_AXI_TRANSACTIONS_NUM)
	) axis_gather_tdata_v1_0_M00_AXI_inst (
		.usr_waddr(axi_waddr),
		.usr_wdata(axi_wdata),
		.usr_raddr(testrData),
		.usr_rdata(testrAddr),
		.INIT_AXI_TXN(pulseInitWrite),
		.ERROR(m00_axi_error),
		.TXN_DONE(m00_axi_txn_done),
		.M_AXI_ACLK(m00_axi_aclk),
		.M_AXI_ARESETN(m00_axi_aresetn),
		.M_AXI_AWADDR(m00_axi_awaddr),
		.M_AXI_AWPROT(m00_axi_awprot),
		.M_AXI_AWVALID(m00_axi_awvalid),
		.M_AXI_AWREADY(m00_axi_awready),
		.M_AXI_WDATA(m00_axi_wdata),
		.M_AXI_WSTRB(m00_axi_wstrb),
		.M_AXI_WVALID(m00_axi_wvalid),
		.M_AXI_WREADY(m00_axi_wready),
		.M_AXI_BRESP(m00_axi_bresp),
		.M_AXI_BVALID(m00_axi_bvalid),
		.M_AXI_BREADY(m00_axi_bready),
		.M_AXI_ARADDR(m00_axi_araddr),
		.M_AXI_ARPROT(m00_axi_arprot),
		.M_AXI_ARVALID(m00_axi_arvalid),
		.M_AXI_ARREADY(m00_axi_arready),
		.M_AXI_RDATA(m00_axi_rdata),
		.M_AXI_RRESP(m00_axi_rresp),
		.M_AXI_RVALID(m00_axi_rvalid),
		.M_AXI_RREADY(m00_axi_rready)
	);

// Instantiation of Axi Bus Interface S00_AXI
	axis_gather_tdata_v1_0_S00_AXI # ( 
		.C_S_AXI_DATA_WIDTH(C_S00_AXI_DATA_WIDTH),
		.C_S_AXI_ADDR_WIDTH(C_S00_AXI_ADDR_WIDTH)
	) axis_gather_tdata_v1_0_S00_AXI_inst (
		.S_START_REG(s00_start_reg),
		.S_MAX_ELEM_TRANSFER_DONE(s00_transfer_done),
		.S_AXI_ACLK(s00_axi_aclk),
		.S_AXI_ARESETN(s00_axi_aresetn),
		.S_AXI_AWADDR(s00_axi_awaddr),
		.S_AXI_AWPROT(s00_axi_awprot),
		.S_AXI_AWVALID(s00_axi_awvalid),
		.S_AXI_AWREADY(s00_axi_awready),
		.S_AXI_WDATA(s00_axi_wdata),
		.S_AXI_WSTRB(s00_axi_wstrb),
		.S_AXI_WVALID(s00_axi_wvalid),
		.S_AXI_WREADY(s00_axi_wready),
		.S_AXI_BRESP(s00_axi_bresp),
		.S_AXI_BVALID(s00_axi_bvalid),
		.S_AXI_BREADY(s00_axi_bready),
		.S_AXI_ARADDR(s00_axi_araddr),
		.S_AXI_ARPROT(s00_axi_arprot),
		.S_AXI_ARVALID(s00_axi_arvalid),
		.S_AXI_ARREADY(s00_axi_arready),
		.S_AXI_RDATA(s00_axi_rdata),
		.S_AXI_RRESP(s00_axi_rresp),
		.S_AXI_RVALID(s00_axi_rvalid),
		.S_AXI_RREADY(s00_axi_rready)
	);

	// Add user logic here
//TODO: move the design into an easy state machine

	reg values_loaded;

	// Count beats up to 1<<16 -> almost 65000 transfers, for a total of almost 260kB 
	reg[BITS_COUNTER-1:0] transfer_count;

	//pwm_state machiene states
	parameter IDLE = 1'b0, SAMPLE = 1'b1;
	reg next_state;
	wire state;

	assign state = next_state;

	wire axis_valid_ready_transfer_1;
	wire axis_valid_ready_transfer_2;
	assign axis_valid_ready_transfer_1 = axis_valid_1&axis_ready_1;
	assign axis_valid_ready_transfer_2 = axis_valid_2&axis_ready_2;

	// Start mechanism 
	reg s00_start_reg_del;

	always @(posedge s00_axi_aclk) begin : proc_
		if(~s00_axi_aresetn) begin
			next_state <= IDLE;
			transfer_count <= 0;
			axi_wdata <= 0;
			axi_waddr <= 0;
			values_loaded <= 0;
			s00_transfer_done <= 0;
			s00_start_reg_del <= 0;
			pulseInitWrite <= 0;
		end else begin
            s00_start_reg_del <= s00_start_reg[0];
			case (state)

				IDLE: begin

					transfer_count <= 0;
					axi_wdata <= 0;
					axi_waddr <= 0;
					values_loaded <= 0;

					// User needs to toggle this bit to start the sample logic
					if ( s00_start_reg[0] != s00_start_reg_del ) begin
						next_state <= SAMPLE;
						s00_transfer_done <= 0;
					end

				end

				SAMPLE: begin
					 

					// Start master transaction - this works if axi is faster than sample,
					// which is the case since sample comes from the ADC at 40kHz and axi works at 100Mhz
					// otherwise this design will never work

					// This design also assumes no backpressure from the AXI Stream, meaning the two ports that are monitored 
					// will keep streaming. This is not a really big deal but in case the stream is stalled we might miss axis_valid_ready_transfer_1

					if (axis_valid_ready_transfer_1) begin
						axi_wdata[15:0] <= axis_data1;
					end 

					if (axis_valid_ready_transfer_2) begin
						axi_wdata[31:16] <= axis_data2;
						values_loaded <= 1;
					end else begin
						values_loaded <= 0;
					end

					if (values_loaded) begin
						pulseInitWrite <= 1;
						transfer_count <= transfer_count+1;
						axi_waddr <= axi_waddr+4; // Increase here otherwise we start at 4
					end else begin
						pulseInitWrite <= 0;
					end

					if( transfer_count == ((1<<BITS_COUNTER)-1) ) begin
						next_state <= IDLE;
						s00_transfer_done <= 1;
					end

					
				end
			endcase // state
		end
	end
	// User logic ends

	endmodule
