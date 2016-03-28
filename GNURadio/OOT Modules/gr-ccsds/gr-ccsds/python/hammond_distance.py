
_data_shift_reg = 0x0ACFFC1D;
_asm_preamble = 0x1ACFFC1D;

distance = (_data_shift_reg & 0xffffffff) ^ _asm_preamble;
distance = ((distance & 0xaaaaaaaa) >> 1) + (distance & 0x55555555);
distance = ((distance & 0xcccccccc) >> 2) + (distance & 0x33333333);
distance = ((distance & 0xf0f0f0f0) >> 4) + (distance & 0x0f0f0f0f);
distance = (distance >> 24) + ((distance >> 16) & 0x0f) + ((distance >> 8) & 0x0f) + (distance & 0x0f);

print distance
