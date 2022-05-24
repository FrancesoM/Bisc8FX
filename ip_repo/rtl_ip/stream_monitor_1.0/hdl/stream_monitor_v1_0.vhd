library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity stream_monitor_v1_0 is
	generic (
		-- Users to add parameters here

		-- User parameters ends
		-- Do not modify the parameters beyond this line


		-- Parameters of Axi Slave Bus Interface S00_AXIS
		C_S00_AXIS_TDATA_WIDTH	: integer	:= 16;

		-- Parameters of Axi Master Bus Interface M00_AXIS
		C_M00_AXIS_TDATA_WIDTH	: integer	:= 16;
		C_M00_AXIS_START_COUNT	: integer	:= 32;

		-- Parameters of Axi Slave Bus Interface S00_AXI
		C_S00_AXI_DATA_WIDTH	: integer	:= 32;
		C_S00_AXI_ADDR_WIDTH	: integer	:= 4
	);
	port (
		-- Users to add ports here

		-- User ports ends
		-- Do not modify the ports beyond this line


		-- Ports of Axi Slave Bus Interface S00_AXIS
		s00_axis_tdata	: in std_logic_vector(C_S00_AXIS_TDATA_WIDTH-1 downto 0);
		s00_axis_tvalid	: in std_logic;
		s00_axis_tready : in std_logic;

		-- Ports of Axi Master Bus Interface M00_AXIS
		m00_axis_aclk	: in std_logic;
		m00_axis_aresetn	: in std_logic;
		m00_axis_tvalid	: out std_logic;
		m00_axis_tdata	: out std_logic_vector(C_M00_AXIS_TDATA_WIDTH-1 downto 0);
		m00_axis_tstrb	: out std_logic_vector((C_M00_AXIS_TDATA_WIDTH/8)-1 downto 0);
		m00_axis_tlast	: out std_logic;
		m00_axis_tready	: in std_logic;

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
		s00_axi_rready	: in std_logic
	);
end stream_monitor_v1_0;

architecture arch_imp of stream_monitor_v1_0 is

	component stream_monitor_v1_0_S00_AXI is
		generic (
		C_S_AXI_DATA_WIDTH	: integer	:= 32;
		C_S_AXI_ADDR_WIDTH	: integer	:= 4
		);
		port (
		TRANSFER_COUNT : out std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0); 
		CTRL_REG       : out std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_ACLK	    : in std_logic;
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
	end component stream_monitor_v1_0_S00_AXI;
	
	-- AXI ctrl regs
	signal i_transaction_count : integer;
	signal b32_transaction_count_max : std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
	signal b32_ctrl_reg : std_logic_vector(C_S00_AXI_DATA_WIDTH-1 downto 0);
	
	-- Logic for capture transactions
	signal b_valid_transaction : std_logic;
	signal b16_data_r  : std_logic_vector(C_S00_AXIS_TDATA_WIDTH-1 downto 0);
	signal b_collected_data_r         : std_logic;
	
	-- State machine for start/stop
	type state_t is (IDLE,CAPTURE);
	signal state : state_t;
	
	signal b_begin_pre_r : std_logic;
	signal b_begin_r : std_logic;

begin

-- Instantiation of Axi Bus Interface S00_AXI
stream_monitor_v1_0_S00_AXI_inst : stream_monitor_v1_0_S00_AXI
	generic map (
		C_S_AXI_DATA_WIDTH	=> C_S00_AXI_DATA_WIDTH,
		C_S_AXI_ADDR_WIDTH	=> C_S00_AXI_ADDR_WIDTH
	)
	port map (
	    TRANSFER_COUNT => b32_transaction_count_max,
	    CTRL_REG       => b32_ctrl_reg,
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
    
    process( m00_axis_aclk ) is
	begin
	  if (rising_edge (m00_axis_aclk)) then
	    if ( m00_axis_aresetn = '0' ) then
	      i_transaction_count <= 0;
	      b16_data_r <= (others => '0');
	      b_collected_data_r <= '0';
	      
	      -- state machine
	      state <= IDLE;
	      b_begin_pre_r <= '0';
	      b_begin_r <= '0';
	      
	    else
	    
	    case state is
	    
	       when IDLE => 
	           
	           b_begin_r     <= b32_ctrl_reg(0);
	           b_begin_pre_r <= b_begin_r;
	           
	           if ( (b_begin_r = '1') xor (b_begin_pre_r = '1') ) then
	               state <= CAPTURE;
	           end if;
	       
	       when CAPTURE => 
	    
              -- Monitor has found a valid transaction - we need to push it out
              if ( s00_axis_tvalid = '1' and s00_axis_tready = '1' ) then  
                -- Push it out only if slave downstream is ready - which should happen if DMA is configured correctly. 
                -- If this does not happen, data is lost. 
                if ( m00_axis_tready = '1' ) then
                    b16_data_r <= s00_axis_tdata;
                    b_collected_data_r <= '1';
                    
                    if ( i_transaction_count < to_integer(unsigned(b32_transaction_count_max)) ) then 
                        i_transaction_count <= 0;
                        state <= IDLE;
                    else
                        i_transaction_count <= i_transaction_count+1;
                    end if;
                    
                else
                    b_collected_data_r <= '0';
                end if; 
              else
                b_collected_data_r <= '0';
              end if; 
          
          end case; 
         
	    end if;
	    
	  end if;
	end process;

    m00_axis_tvalid	<= '0' when state = IDLE else b_collected_data_r;
	m00_axis_tdata	<= b16_data_r;
	m00_axis_tstrb	<= (others => '1');
	m00_axis_tlast  <= '1' when i_transaction_count = (to_integer(unsigned(b32_transaction_count_max))-1) else '0';
    
    
	-- User logic ends

end arch_imp;
