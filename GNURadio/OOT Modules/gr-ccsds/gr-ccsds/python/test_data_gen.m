
% create preamble
preamble = bin2dec('00011010110011111111110000011101');
preamble_arr = de2bi(preamble,32);

% create random pre frame bit array
random_arr = rand(64,1);
random_bit = (random_arr>0.5).*(1) + (random_arr<=0.5).*(0);

% add random sequence before preamble
output = cat(1, random_bit, flipud(preamble_arr'));

% create random payload bit array
payload_arr = rand(8*255,1);
payload_bit = (payload_arr>0.5).*(1) + (payload_arr<=0.5).*(0);

for n=1:length(payload_bit)/8
   payload_byte(n) = bi2de(payload_bit(8*(n-1)+1:8*(n-1)+8)','left-msb'); 
end

% add payload to frame
output = cat(1, output, payload_bit);

% create random pre frame bit array
random_arr = rand(64,1);
random_bit = (random_arr>0.5).*(1) + (random_arr<=0.5).*(0);

% add random dat after frame
output = cat(1, output, random_bit);

% write bit sequence to file
fileID = fopen('bit_in.txt','w');
fprintf(fileID,'%i\n',output);
fclose(fileID);

% write payload to file
fileID = fopen('byte_out.txt','w');
fprintf(fileID,'%i\n',payload_byte);
fclose(fileID);
