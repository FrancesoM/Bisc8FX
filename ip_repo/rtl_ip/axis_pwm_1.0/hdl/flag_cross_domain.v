module Flag_CrossDomain(
	input rst,
    input clkA,
    input FlagIn_clkA,   // this is a one-clock pulse from the clkA domain
    input clkB,
    output FlagOut_clkB   // from which we generate a one-clock pulse in clkB domain
);

reg FlagToggle_clkA; 
reg [2:0] SyncA_clkB;

assign FlagOut_clkB = (SyncA_clkB[2] ^ SyncA_clkB[1]);  // and create the clkB flag

always @(posedge clkA) 
if (~rst) begin 
	FlagToggle_clkA <= 0;
end else begin
	FlagToggle_clkA <= FlagToggle_clkA ^ FlagIn_clkA;  // when flag is asserted, this signal toggles (clkA domain)
end

always @(posedge clkB) 
if (~rst)  begin
	SyncA_clkB <= {1'b0,1'b0,1'b0};
end else begin
	SyncA_clkB <= {SyncA_clkB[1:0], FlagToggle_clkA};  // now we cross the clock domains
end

endmodule