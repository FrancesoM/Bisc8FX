
`timescale 1 ns / 1 ps

module axis_pwm_v1_0 #
		// Do not modify the parameters beyond this line
	(
		// Users to add parameters here
		parameter integer TIMER_BITS = 12,
		// User parameters ends


		// Parameters of Axi Slave Bus Interface S00_AXIS
		parameter integer C_S00_AXIS_TDATA_WIDTH	= 16
		)
	(
		// Users to add ports here
		//----------Output Ports--------------
		output wire [TIMER_BITS-1:0] tim_out,
		output wire pwm_out,
		input wire pwm_clk,
		//------------Input Ports--------------
		
		// User ports ends
		// Do not modify the ports beyond this line


		// Ports of Axi Slave Bus Interface S00_AXIS
		input wire  s00_axis_aclk,
		input wire  s00_axis_aresetn,
		output wire  s00_axis_tready,
		input wire [C_S00_AXIS_TDATA_WIDTH-1 : 0] s00_axis_tdata,
		input wire [(C_S00_AXIS_TDATA_WIDTH/8)-1 : 0] s00_axis_tstrb,
		input wire  s00_axis_tlast,
		input wire  s00_axis_tvalid
		);

	// Add user logic here

		  // Flags for valid synchronization between clock domains
	  wire axi_new_data; //Asserted for one axi clock cycle when new data is sampled
	  wire pwm_new_data;

	  wire axi_read_data;  //Asserted for one pwm clock cycle when the new data is read
	  wire pwm_read_data;

	  reg axi_new_data_b; // Axi writes this
	  reg pwm_new_data_b; // But pwm reads it and acknowledge the axi part only when it can actually receive a new data
	  reg pwm_read_data_b; //Only pwm writes this

	   Flag_CrossDomain fcd_axi_to_pwm(.rst(s00_axis_aresetn),
	   								.clkA(s00_axis_aclk),
									.FlagIn_clkA(axi_new_data),
									.clkB(pwm_clk),
									.FlagOut_clkB(pwm_new_data) );

	   Flag_CrossDomain fcd_pwm_to_axi(.rst(s00_axis_aresetn),
	   								.clkA(pwm_clk),
									.FlagIn_clkA(pwm_read_data),
									.clkB(s00_axis_aclk),
									.FlagOut_clkB(axi_read_data) );


	  //------------Internal Variables--------
	  reg [TIMER_BITS-1:0] tim_out_b;
	  reg [TIMER_BITS-1:0] reg_duty;
	  reg [TIMER_BITS-1:0] reg_duty_b;
	  reg [TIMER_BITS-1:0] reg_duty_b_saved;
	  reg [TIMER_BITS-1:0] reg_top;

	  reg pwm_out_b;

	  // Axi variables
	  reg [C_S00_AXIS_TDATA_WIDTH-1:0] s00_axis_tdata_reg;
	  reg s00_axis_tready_reg;

	  // Continuous assignments
	  assign s00_axis_tready = s00_axis_tready_reg;
	  assign pwm_out = pwm_out_b;
	  assign tim_out = tim_out_b;

	  assign axi_new_data = axi_new_data_b;
	  assign pwm_read_data = pwm_read_data_b;

	  //-------------Code Starts Here-------

	  always @(posedge pwm_clk or negedge s00_axis_aresetn)
	  if (~s00_axis_aresetn) begin
	  	tim_out_b <= 12'b0 ;
		pwm_out_b  <= 1;
		reg_duty <= ((1<<TIMER_BITS)-1)/2; //Start with duty at 50%
		reg_top <= (1<<TIMER_BITS)-1;
		pwm_read_data_b <= 0;
		pwm_new_data_b <= 0;
	  end 

	  else  begin

	  	  // Timer logic
	      tim_out_b <= tim_out_b + 1;  // always increase the count
	      if ( tim_out_b >= reg_top-1 )  begin
			tim_out_b <= 12'b0 ;  //when reaching in_top, reset counter and reset tim_out_b to 1
			pwm_out_b  <= 1;
			if( pwm_new_data_b ) begin
				reg_duty <= reg_duty_b_saved;
				pwm_read_data_b <= 1;
			end

	      // PWM logic
	      end else begin
			if (tim_out_b >= reg_duty-1) begin //classic pwm logic
				pwm_out_b <= 0;
			end else begin
				pwm_out_b <= 1;
			end
			pwm_read_data_b <= 0; // Since it's a flag, bring this down the next cycle
	      end

	      // Sample flag, save new data, but don't tell axi that we are ready to accept a new one
	      // We will be when we set this new duty
	      if (pwm_new_data) begin
				reg_duty_b_saved <= reg_duty_b;
				pwm_new_data_b <= 1;
		  end	

	  end

	  // Axi stream logic

	  always @(posedge s00_axis_aclk or negedge s00_axis_aresetn) begin
	  	if(~s00_axis_aresetn) begin
			s00_axis_tready_reg <= 1;  
			axi_new_data_b <= 0;
	  	end else begin

	  		// We will sample when we are ready 
	  		if(s00_axis_tvalid && s00_axis_tready_reg) begin

	  			// Buffer the input data, it will become the next duty at the next tim overflow
	  			reg_duty_b <= s00_axis_tdata[TIMER_BITS-1:0];

	  			s00_axis_tready_reg <= 0;

	  			axi_new_data_b <= 1;  //This must be asserted for one cycle, then it will be broadcast into pwm clock domain

	  		end else begin
	  			axi_new_data_b <= 0;
	  		end

	  		// We become ready when we have read the new data
	  		if ( axi_read_data) begin
	  			s00_axis_tready_reg <= 1;
	  		end

	  	end
	  end

	// User logic ends

endmodule
