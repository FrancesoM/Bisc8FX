library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

Library xpm;
use xpm.vcomponents.all;

entity PWM_generator_v1_0 is
	generic (
		-- Users to add parameters here
		TIMER_BITS 				: integer := 16;
		TEST_TOP				: integer := 2**12;
		USE_FIX_TOP            : boolean := FALSE; -- Use this to fix at compile time the top, instead of picking it from AXI config
		-- User parameters ends
		-- Do not modify the parameters beyond this line


		-- Parameters of Axi Slave Bus Interface S00_AXI
		C_S00_AXI_DATA_WIDTH	: integer	:= 32;
		C_S00_AXI_ADDR_WIDTH	: integer	:= 4;

		-- Parameters of Axi Slave Bus Interface S00_AXIS
		C_S00_AXIS_TDATA_WIDTH	: integer	:= 16
	);
	port (
		-- Users to add ports here
		pwm_clk			: in std_logic;
		pwm_rst			: in std_logic;
		pwm_out         : out std_logic;
		arst            : in std_logic;
		-- User ports ends
		-- Do not modify the ports beyond this line


		-- Ports of Axi Slave Bus Interface S00_AXI
		s00_axi_aclk	: in std_logic;
		s00_axi_aresetn	: in std_logic;
		s00_axi_awaddr	: in std_logic_vector(C_S00_AXI_ADDR_WIDTH-1 downto 0);
		s00_axi_awprot	: in std_logic_vector(2 downto 0);
		s00_axi_awvalid	: in std_logic;
		s00_axi_awready	: out std_logic;
		s00_axi_wdata	: in std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
		s00_axi_wstrb	: in std_logic_vector((C_S00_AXI_DATA_WIDTH/8)-1 downto 0);
		s00_axi_wvalid	: in std_logic;
		s00_axi_wready	: out std_logic;
		s00_axi_bresp	: out std_logic_vector(1 downto 0);
		s00_axi_bvalid	: out std_logic;
		s00_axi_bready	: in std_logic;
		s00_axi_araddr	: in std_logic_vector(C_S00_AXI_ADDR_WIDTH-1 downto 0);
		s00_axi_arprot	: in std_logic_vector(2 downto 0);
		s00_axi_arvalid	: in std_logic;
		s00_axi_arready	: out std_logic;
		s00_axi_rdata	: out std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
		s00_axi_rresp	: out std_logic_vector(1 downto 0);
		s00_axi_rvalid	: out std_logic;
		s00_axi_rready	: in std_logic;

		-- Ports of Axi Slave Bus Interface S00_AXIS
		s00_axis_aclk	: in std_logic;
		s00_axis_aresetn	: in std_logic;
		s00_axis_tready	: out std_logic;
		s00_axis_tdata	: in std_logic_vector(C_S00_AXIS_TDATA_WIDTH-1 downto 0);
		s00_axis_tstrb	: in std_logic_vector((C_S00_AXIS_TDATA_WIDTH/8)-1 downto 0);
		s00_axis_tlast	: in std_logic;
		s00_axis_tvalid	: in std_logic
	);
end PWM_generator_v1_0;

architecture arch_imp of PWM_generator_v1_0 is

	-- component declaration
	component PWM_generator_v1_0_S00_AXI is
		generic (
		C_S_AXI_DATA_WIDTH	: integer	:= 32;
		C_S_AXI_ADDR_WIDTH	: integer	:= 4
		);
		port (
		TOP_TIMER_CNT : out std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_ACLK	: in std_logic;
		S_AXI_ARESETN	: in std_logic;
		S_AXI_AWADDR	: in std_logic_vector(C_S_AXI_ADDR_WIDTH-1 downto 0);
		S_AXI_AWPROT	: in std_logic_vector(2 downto 0);
		S_AXI_AWVALID	: in std_logic;
		S_AXI_AWREADY	: out std_logic;
		S_AXI_WDATA	: in std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_WSTRB	: in std_logic_vector((C_S_AXI_DATA_WIDTH/8)-1 downto 0);
		S_AXI_WVALID	: in std_logic;
		S_AXI_WREADY	: out std_logic;
		S_AXI_BRESP	: out std_logic_vector(1 downto 0);
		S_AXI_BVALID	: out std_logic;
		S_AXI_BREADY	: in std_logic;
		S_AXI_ARADDR	: in std_logic_vector(C_S_AXI_ADDR_WIDTH-1 downto 0);
		S_AXI_ARPROT	: in std_logic_vector(2 downto 0);
		S_AXI_ARVALID	: in std_logic;
		S_AXI_ARREADY	: out std_logic;
		S_AXI_RDATA	: out std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_RRESP	: out std_logic_vector(1 downto 0);
		S_AXI_RVALID	: out std_logic;
		S_AXI_RREADY	: in std_logic
		);
	end component PWM_generator_v1_0_S00_AXI;

	-- pwm registers for counting
	signal pwm_duty_s : std_logic_vector(TIMER_BITS-1 downto 0);
	signal pwm_read_enable_s  : std_logic;
	signal pwm_empty_fifo_s  : std_logic;

	signal pwm_cnt_r   : integer range 0 to 2**TIMER_BITS-1;
	signal pwm_duty_r  : integer range 0 to 2**TIMER_BITS-1;
	signal pwm_top_r   : integer range 0 to 2**TIMER_BITS-1;
	signal pwm_top_source   : integer range 0 to 2**TIMER_BITS-1;

	signal pwm_top_axi_s : std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);


begin

-- Instantiation of Axi Bus Interface S00_AXI
PWM_generator_v1_0_S00_AXI_inst : PWM_generator_v1_0_S00_AXI
	generic map (
		C_S_AXI_DATA_WIDTH	=> C_S00_AXI_DATA_WIDTH,
		C_S_AXI_ADDR_WIDTH	=> C_S00_AXI_ADDR_WIDTH
	)
	port map (
		TOP_TIMER_CNT => pwm_top_axi_s,
		S_AXI_ACLK	=> s00_axi_aclk,
		S_AXI_ARESETN	=> s00_axi_aresetn,
		S_AXI_AWADDR	=> s00_axi_awaddr,
		S_AXI_AWPROT	=> s00_axi_awprot,
		S_AXI_AWVALID	=> s00_axi_awvalid,
		S_AXI_AWREADY	=> s00_axi_awready,
		S_AXI_WDATA	=> s00_axi_wdata,
		S_AXI_WSTRB	=> s00_axi_wstrb,
		S_AXI_WVALID	=> s00_axi_wvalid,
		S_AXI_WREADY	=> s00_axi_wready,
		S_AXI_BRESP	=> s00_axi_bresp,
		S_AXI_BVALID	=> s00_axi_bvalid,
		S_AXI_BREADY	=> s00_axi_bready,
		S_AXI_ARADDR	=> s00_axi_araddr,
		S_AXI_ARPROT	=> s00_axi_arprot,
		S_AXI_ARVALID	=> s00_axi_arvalid,
		S_AXI_ARREADY	=> s00_axi_arready,
		S_AXI_RDATA	=> s00_axi_rdata,
		S_AXI_RRESP	=> s00_axi_rresp,
		S_AXI_RVALID	=> s00_axi_rvalid,
		S_AXI_RREADY	=> s00_axi_rready
	);

	-- Add user logic here

--https://docs.xilinx.com/api/khub/documents/D0h3w5xHefBZYAuB5WP9oA/content?Ft-Calling-App=ft%2Fturnkey-portal&Ft-Calling-App-Version=3.11.26&filename=ug953-vivado-7series-libraries.pdf#386224146
-- xpm_fifo_async: Asynchronous FIFO
-- Xilinx Parameterized Macro, Version 2016.4
	xpm_fifo_async_inst : xpm_fifo_async
		generic map (
			FIFO_MEMORY_TYPE => "block", --string; "auto", "block", or "distributed";
			ECC_MODE => "no_ecc", --string; "no_ecc" or "en_ecc";
			RELATED_CLOCKS => 0, --positive integer; 0 or 1
			FIFO_WRITE_DEPTH => 16, --positive integer
			WRITE_DATA_WIDTH => C_S00_AXIS_TDATA_WIDTH, --positive integer
			FULL_RESET_VALUE => 0, --positive integer; 0 or 1;
			READ_MODE => "std", --string; "std" or "fwft";
			FIFO_READ_LATENCY => 1, --positive integer;
			READ_DATA_WIDTH => C_S00_AXIS_TDATA_WIDTH, --positive integer
			DOUT_RESET_VALUE => "0", --string
			CDC_SYNC_STAGES => 2, --positive integer
			WAKEUP_TIME => 0 --positive integer; 0 or 2;
	)
		port map (
			sleep => '0',
			rst => arst,
			wr_clk => s00_axis_aclk,
			wr_en => s00_axis_tvalid,
			din => s00_axis_tdata,
			rd_clk => pwm_clk,
			rd_en => pwm_read_enable_s,
			empty => pwm_empty_fifo_s, 
			dout => pwm_duty_s,
			injectsbiterr => '0',
			injectdbiterr => '0'
	);
	-- End of xpm_fifo_async_inst instance declaration
	
	-- combinatorial process to drive the output
	pwm_out <= '0' when pwm_cnt_r > pwm_duty_r else '1';
	pwm_read_enable_s <= '1' when pwm_empty_fifo_s = '0' else '0';

	s00_axis_tready <= '1';

    fix_top : if USE_FIX_TOP generate
      begin
         pwm_top_source <= TEST_TOP;
      end;
    else generate 
      begin
         pwm_top_source <= to_integer(unsigned(pwm_top_axi_s));
      end;
   end generate fix_top;

	process (pwm_clk)
	begin
	  if rising_edge(pwm_clk) then 
	    if pwm_rst = '0' then
	      	-- what do we need to reset?
	      	pwm_cnt_r  <= 0;
	      	pwm_duty_r <= 0;
	      	pwm_top_r  <= TEST_TOP;
	    else

	    	-- If FIFO is not empty, read value from it
	    	if( pwm_read_enable_s = '1') then
	    		pwm_duty_r <= to_integer(unsigned(pwm_duty_s))  ;
	    	end if;

	    	-- Keep increasing val
	    	if ( pwm_cnt_r = pwm_top_r) then
	    		pwm_cnt_r <= 0;
	    	else
		    	pwm_cnt_r <= pwm_cnt_r+1;
		    end if;

		    pwm_top_r <= pwm_top_source;

	    end if;
	  end if;
	end process;

	-- User logic ends

end arch_imp;
