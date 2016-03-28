##################################################
# GNU Radio Python Flow Graph
# Title: Randomise & ASM Frame
# Generated: Tue Aug 11 23:18:55 2015
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes

class randomise_asm(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "Randomise & ASM Frame",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Variables
        ##################################################
        self.Randomiser = Randomiser = (255, 72, 14, 192, 154, 13, 112, 188, 142, 44, 147, 173, 167, 183, 70, 206, 90, 151, 125, 204, 50, 162, 191, 62, 10, 16, 241, 136, 148, 205, 234, 177, 254, 144, 29, 129, 52, 26, 225, 121, 28, 89, 39, 91, 79, 110, 141, 156, 181, 46, 251, 152, 101, 69, 126, 124, 20, 33, 227, 17, 41, 155, 213, 99, 253, 32, 59, 2, 104, 53, 194, 242, 56, 178, 78, 182, 158, 221, 27, 57, 106, 93, 247, 48, 202, 138, 252, 248, 40, 67, 198, 34, 83, 55, 170, 199, 250, 64, 118, 4, 208, 107, 133, 228, 113, 100, 157, 109, 61, 186, 54, 114, 212, 187, 238, 97, 149, 21, 249, 240, 80, 135, 140, 68, 166, 111, 85, 143, 244, 128, 236, 9, 160, 215, 11, 200, 226, 201, 58, 218, 123, 116, 108, 229, 169, 119, 220, 195, 42, 43, 243, 224, 161, 15, 24, 137, 76, 222, 171, 31, 233, 1, 216, 19, 65, 174, 23, 145, 197, 146, 117, 180, 246, 232, 217, 203, 82, 239, 185, 134, 84, 87, 231, 193, 66, 30, 49, 18, 153, 189, 86, 63, 210, 3, 176, 38, 131, 92, 47, 35, 139, 36, 235, 105, 237, 209, 179, 150, 165, 223, 115, 12, 168, 175, 207, 130, 132, 60, 98, 37, 51, 122, 172, 127, 164, 7, 96, 77, 6, 184, 94, 71, 22, 73, 214, 211, 219, 163, 103, 45, 75, 190, 230, 25, 81, 95, 159, 5, 8, 120, 196, 74, 102, 245, 88)
        self.ASM = ASM = (0x1A, 0xCF, 0xFC, 0x1D)

        ##################################################
        # Blocks
        ##################################################
        self.blocks_xor_xx_0 = blocks.xor_bb()
        self.blocks_vector_source_x_0_1_0 = blocks.vector_source_b(Randomiser, True, 1, [])
        self.blocks_vector_source_x_0_1 = blocks.vector_source_b(ASM, True, 1, [])
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (4, 255))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_mux_0, 0), (self, 0))    
        self.connect((self.blocks_vector_source_x_0_1, 0), (self.blocks_stream_mux_0, 0))    
        self.connect((self.blocks_vector_source_x_0_1_0, 0), (self.blocks_xor_xx_0, 1))    
        self.connect((self.blocks_xor_xx_0, 0), (self.blocks_stream_mux_0, 1))    
        self.connect((self, 0), (self.blocks_xor_xx_0, 0))    


    def get_Randomiser(self):
        return self.Randomiser

    def set_Randomiser(self, Randomiser):
        self.Randomiser = Randomiser
        self.blocks_vector_source_x_0_1_0.set_data(self.Randomiser)

    def get_ASM(self):
        return self.ASM

    def set_ASM(self, ASM):
        self.ASM = ASM
        self.blocks_vector_source_x_0_1.set_data(self.ASM)

