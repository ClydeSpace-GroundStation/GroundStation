/* -*- c++ -*- */
/*
 * Copyright 2012 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <ec_ax25_decoder_b.h>
#include <gnuradio/blocks/pdu.h>

//#include <ppio.h>
#include <cstdio>
#include <stdexcept>
#include <time.h>
#include <iostream>
#include <fstream>
using namespace std;

//--------------- Private Methods ------------------------------------

void
ec_ax25_decoder_b::printer(unsigned short frame_size, unsigned char *frame_buf)
{
	//std::cout << "printer" << std::endl;
	int		adr_len;
	unsigned int	bit_shifted;
	int		i;

	if (frame_buf[13]&0x01){
		adr_len=14;
	}
	else if (frame_buf[20]&0x01){
		adr_len=21;
	}
	else{
		adr_len=28;
	}
	time_t rawtime;
	struct tm * timeinfo;
	time ( &rawtime );
	timeinfo = localtime ( &rawtime );
	printf ( "Current local time and date: %s", asctime (timeinfo) );
	printf("Destination:  ");
	for(i=0; i<frame_size-2; i++){
		bit_shifted= frame_buf[i]>>1;
		if(i==13 & adr_len>14){
			printf("\nLayer 2 repeater subfield 1:  ");
		}
		else if(i==20 & adr_len>21){
			printf("\nLayer 2 repeater subfield 2:  ");
		}
		else if(i==6){
			printf("\nSource:  ");
		}
		else if(i==adr_len-1){
			printf("\nControl, PID and Info:\n");
		}
		else if(i<adr_len){
			if(bit_shifted<0x7F && bit_shifted>=0x20){
				printf("%c", bit_shifted);
			}
			else{
				printf(" %02X ", bit_shifted);
			}
		}
		else {
			if(frame_buf[i]<0x7F && frame_buf[i]>=0x20){
				printf("%c", frame_buf[i]);
			}
			else{
				printf(" %02X ", frame_buf[i]);
			}
		}
	}
printf("\n\n");
}

void
ec_ax25_decoder_b::file_output_1(unsigned short frame_size, unsigned char *frame_buf, const char *filename)
{
	int		adr_len;
	unsigned int	bit_shifted;
	int		i;

	FILE * myfile;
	myfile = fopen (filename,"a+");
	time_t rawtime;
	struct tm * ptm;
	time ( &rawtime );
	ptm = gmtime ( &rawtime );

	if (frame_buf[13]&0x01){
		adr_len=14;
	}
	else if (frame_buf[20]&0x01){
		adr_len=21;
	}
	else{
		adr_len=28;
	}
  	fprintf (myfile, "%04d-%02d-%02dT%02d:%02d:%02d;",ptm->tm_year+1900 ,ptm->tm_mon+1 ,ptm->tm_mday, (ptm->tm_hour)%24, ptm->tm_min, ptm->tm_sec);
	for(i=0; i<frame_size-2; i++){
		bit_shifted= frame_buf[i]>>1;
		if(i==13 & adr_len>14){
			fprintf(myfile, ";");
		}
		else if(i==20 & adr_len>21){
			fprintf(myfile, ";");
		}
		else if(i==6){
			fprintf(myfile, ";");
		}
		else if(i==adr_len-1){
			fprintf(myfile, ";");
		}
		else if(i<adr_len){
			if(bit_shifted<0x7F && bit_shifted>=0x20){
				fprintf(myfile, "%c", bit_shifted);
			}
			else{
				fprintf(myfile, " %02X ", bit_shifted);
			}
		}
		else {
			if(frame_buf[i]<0x7F && frame_buf[i]>=0x20){
				fprintf(myfile, "%02X", frame_buf[i]);
			}
			else{
				fprintf(myfile, "%02X", frame_buf[i]);
			}
		}
	}
fprintf(myfile, ";\n");
fclose (myfile);
}

void
ec_ax25_decoder_b::file_output_2(unsigned short frame_size, unsigned char *frame_buf, const char *filename)
{
	int		adr_len;
	unsigned int	bit_shifted;
	int		i;

	FILE * myfile;
	myfile = fopen (filename,"a+");
	time_t rawtime;
	struct tm * ptm;
	time ( &rawtime );
	ptm = gmtime ( &rawtime );

	if (frame_buf[13]&0x01){
		adr_len=14;
	}
	else if (frame_buf[20]&0x01){
		adr_len=21;
	}
	else{
		adr_len=28;
	}
	fprintf(myfile, "UTC when packet was received: ");
	fprintf (myfile, "%04d-%02d-%02dT%02d:%02d:%02d;",ptm->tm_year+1900 ,ptm->tm_mon+1 ,ptm->tm_mday, (ptm->tm_hour)%24, ptm->tm_min, ptm->tm_sec);
	fprintf(myfile, "Destination:  ");
	for(i=0; i<frame_size-2; i++){
		bit_shifted= frame_buf[i]>>1;
		if(i==13 & adr_len>14){
			fprintf(myfile, "\nLayer 2 repeater subfield 1:  ");
		}
		else if(i==20 & adr_len>21){
			fprintf(myfile, "\nLayer 2 repeater subfield 2:  ");
		}
		else if(i==6){
			fprintf(myfile, "\nSource:  ");
		}
		else if(i==adr_len-1){
			fprintf(myfile, "\nControl, PID and Info:\n");
		}
		else if(i<adr_len){
			if(bit_shifted<0x7F && bit_shifted>=0x20){
				fprintf(myfile, "%c", bit_shifted);
			}
			else{
				fprintf(myfile, " %02X ", bit_shifted);
			}
		}
		else {
			if(frame_buf[i]<0x7F && frame_buf[i]>=0x20){
				fprintf(myfile, "%c", frame_buf[i]);
			}
			else{
				fprintf(myfile, " %02X ", frame_buf[i]);
			}
		}
	}
fprintf(myfile, "\n\n");
fclose (myfile);
}


//A FASTER ALGORITHM TO MAKE THE CRC, THAN THE BY IZ2EEQ AND
//SPACECRAFT GROUNDSTATION.

unsigned short
ec_ax25_decoder_b::crc16(unsigned char *data_p, unsigned short lenght)
{
	unsigned short crc = 0xFFFF;
	unsigned int data;
	unsigned short crc16_table[] = {
		0x0000, 0x1081, 0x2102, 0x3183,
		0x4204, 0x5285, 0x6306, 0x7387,
		0x8408, 0x9489, 0xa50a, 0xb58b,
		0xc60c, 0xd68d, 0xe70e, 0xf78f
	};
	while(lenght--){
		crc = ( crc >> 4 ) ^ crc16_table[(crc & 0xf) ^ (*data_p & 0xf)];
		crc = ( crc >> 4 ) ^ crc16_table[(crc & 0xf) ^ (*data_p++ >> 4)];
	}
	data = crc;
	crc = (crc << 8) | (data >> 8 & 0xff);
	return (~crc);
}

//ALGORITHM USED BY IZ2EEQ
//http://digilander.libero.it/iz2eeq/
/*

unsigned short ec_ax25_decoder_b::crc16(unsigned char *data_p, unsigned short lenght) {
	unsigned short fcs=0x0000;
	unsigned char i;
	unsigned char k;
	for (int i=0; i<lenght; i++) {
	        fcs = fcs ^ *data_p++;
		for (int k=0;k<8;k++) {
			if (fcs & 0x01) {
			fcs = (fcs >> 1) ^ 0x1021;
			}
			else {
				fcs>>=1;
			}
		}
	}
	return(fcs^0xFFFF);
}

*/

//ALGORITH USED BY GMSK SPACECRAFT GROUNDSTATION
//https://www.cgran.org/wiki/GMSKSpacecraftGroundstation

//                                      16   12   5
// this is the CCITT CRC 16 polynomial X  + X  + X  + 1.
// This is 0x1021 when x is 2, but the way the algorithm works
// we use 0x8408 (the reverse of the bit pattern).  The high
// bit is always assumed to be set, thus we only use 16 bits to
// represent the 17 bit value.
//
// We have to use the reverse pattern because serial comm using
// UARTs abd USRTs send out each byte LSBit first, but the
// CRC algorithm is specified using MSBit first.  So this
// whole algorithm is reversed to compensate.  The main loop
// shifts right instead of left as in the cannonical algorithm
//
/*
unsigned short ec_ax25_decoder_b::crc16(unsigned char *data_p, unsigned short length)
{
	const int     POLY = 0x8408;   // 1021H bit reversed
	unsigned char i;
	unsigned int  data;
	unsigned int  crc = 0xffff;
	if (length == 0)
		return (~crc);
	do{
		for (i=0, data=(unsigned int)0xff & *data_p++;
		i < 8;
		i++, data >>= 1)
		{
			if ((crc & 0x0001) ^ (data & 0x0001)){
				crc = (crc >> 1) ^ POLY;
			{
			else{
				crc >>= 1;
			}
		}
	} while (--length);
	crc = ~crc;
	data = crc;
	crc = (crc << 8) | (data >> 8 & 0xff);

	return (crc);
}
*/

int
ec_ax25_decoder_b::crc_valid(int frame_size, unsigned char * frame)
{
	unsigned short frame_crc;
	unsigned short calc_crc;
	frame_crc = frame[frame_size-1] | (frame[frame_size-2] << 8);
	calc_crc = crc16(frame, frame_size-2);
	//fprintf(stderr, "frame: %x,  calc: %x\n", frame_crc, calc_crc);
	return(calc_crc == frame_crc);
}

int
ec_ax25_decoder_b::unstuff(int             bit_buf_size,
                               unsigned char * bit_buf,
                               int *           frame_buf_size,
                               unsigned char * frame_buf)
{
	int           i;
	unsigned char data_bit;
	int           accumulated_bits;
	int           bytes;
	int           consecutive_one_bits;
	int           status;

	//std::cout << "bit buf:  " << bit_buf_size << std::endl;

	int unstuff_count = 0;

	accumulated_bits = 0;
	bytes = 0;
	consecutive_one_bits = 0;
	for(i=0; i<bit_buf_size; i++)
	{
		data_bit = bit_buf[i];
		if( (consecutive_one_bits != 5) || (data_bit == 1) ){
			// Not a stuffed 0,  Write it to frame_buf
			frame_buf[bytes] = (frame_buf[bytes] >> 1) | (data_bit << 7);
			accumulated_bits++;
			if(accumulated_bits == 8){
				bytes++;
				accumulated_bits = 0;
			}
		} else {
			//std::cout << "Removed bit" << std::endl;
			unstuff_count += 1;
		}

		if(data_bit == 1){
			consecutive_one_bits++;
		}
		else{
			consecutive_one_bits = 0;
		}
	}
	//std::cout << unstuff_count << " bits unstuffed" << std::endl;
	//std::cout << "Accum bits:  " << accumulated_bits << std::endl;
	// Now check for an integer number of bytes
	if(accumulated_bits == 0){
		status = SUCCESS;
		*frame_buf_size = bytes;
	}
	else{
		status = FAIL;
		*frame_buf_size = 0;
		//*frame_buf_size = bytes;
	}
	return status;
}

void
ec_ax25_decoder_b::hdlc_state_machine(unsigned char next_bit)
{
	int		next_state;
	int		i;
	unsigned char	frame_buf[FRAME_BUF_MAX];
	int		frame_size;
	int		status;
	int		adr_len;
	unsigned int	bit_shifted;
	switch(d_state){
		case HUNT:
		// Preload the first 7 bits to get things started
		d_byte = (d_byte >> 1) | (next_bit << 7);
		d_accumulated_bits++;
		//std::cout << "State = HUNT " << d_accumulated_bits << std::endl;
		if(d_accumulated_bits < 7){
			next_state = HUNT;
		}
		else{
			next_state = IDLE;
		}
		break;

		case IDLE:
		     //cout << "State = IDLE" << std::endl;
		d_byte = (d_byte >> 1) | (next_bit << 7);
		if(d_byte == FLAG){
			// Count it and keep hunting for more flags
			d_flag_cnt++;
			d_byte = 0x00;
			d_accumulated_bits = 0;
			next_state = HUNT;
		}
		else{
			// A non-FLAG byte starts a frame
			// Store the bits in the bit_buf, lsb first, and
			// change states.
			for(i=0; i<8; i++){
				d_bit_buf[i] = (d_byte >> i) & 0x01;
			}
			d_bit_buf_size = 8;
			next_state = FRAMING;
			//std::cout << "Flag found!" << std::endl;
		}
		break;

		case FRAMING:
		     //std::cout << "State = FRAMING   bit_buf_size = "<< d_bit_buf_size << std::endl;
		// Collect frame bits in bit_buf for later unstuffing
		if(d_bit_buf_size < BIT_BUF_MAX){
			// std::cout << "index: " << d_bit_buf_size << "   BIT_BUF_MAX: " << BIT_BUF_MAX << std::endl;
			d_bit_buf[d_bit_buf_size] = next_bit;
			d_bit_buf_size++;
		}
		// Count consecutive 1 bits
		if(next_bit == 1){
			d_consecutive_one_bits++;
		}
		else{
			d_consecutive_one_bits = 0;
		}
		// Test for Aborts and FLAGs
		if(d_consecutive_one_bits > 7){
			// Too many 1 bits in a row. Abort.
			d_byte = 0x00;
			d_accumulated_bits = 0;
			next_state = HUNT;
			// std::cout << "Aborted here1" << std::endl;
		}
		else{
			// Pack bit into byte buffer and check for FLAG
			d_byte = (d_byte >> 1) | (next_bit << 7);
			if(d_byte != FLAG){
				// Keep on collecting frame bits
				//fprintf(stderr, "  byte = %x\n", d_byte);
				next_state = FRAMING;
				// std::cout << "Aborted here2" << std::endl;
			}
			else {
			// It's a FLAG. Frame is terminated.
			//fprintf(stderr, "  2nd FLAG,   number bits: %d    lastbyte:%x\n",d_bit_buf_size,d_byte);
			d_flag_cnt++;
			// Remove flag from bit_buf
			d_bit_buf_size -= 8;
			// Process bit_buf and
			// see if we got a good frame.
			status = unstuff(d_bit_buf_size, d_bit_buf, &frame_size, frame_buf);
			// std::cout << "Status 1: " << status << "   Frame size: " << frame_size << std::endl;

			// std::cout << "Frame size: " << frame_size << "   Status: " << status << std::endl;

			if(frame_size > 13 & frame_size < FRAME_MAX & status != FAIL){
					// Size OK. Check crc
		      status = crc_valid(frame_size, frame_buf);
					// std::cout << "Status 2: " << status << std::endl;
					//status = 1;

					if(status != FAIL){

						// std::cout << "Frame succesful" << std::endl;

						// Good frame! Log statistics
						d_good_byte_cnt += frame_size-2; // don't count CRC

						// pmt::pmt_t vecpmt(pmt::make_blob(frame_buf

						pmt::pmt_t vecpmt(pmt::make_blob(&frame_buf[16], frame_size-18));
						pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL, vecpmt));

						message_port_pub(PDU_PORT_ID, pdu);



						if (d_printing){
							printer(frame_size, frame_buf);
						}
						if (d_print_to_file == 1){
							file_output_1(frame_size, frame_buf, d_filename);
						}
						else if (d_print_to_file == 2){
							file_output_2(frame_size, frame_buf, d_filename);
						}
					// } else {
					// 	std::cout << "Frame failed" << std::endl;
				} //else {
						//std::cout << "Failed1" << std::endl;
					//}
				} //else {
					//std::cout << "Failed2" << std::endl;
				//}

		        	// Hunt for next flag or frame
		        	d_byte = 0x00;
		        	d_accumulated_bits = 0;
		        	next_state = HUNT;
				//std::cout << "Aborted here3" << std::endl;
			}
		}
		break;
	} // end switch
	// Save new state and return
	d_state = next_state;
}

//--------------- Protected Methods ----------------------------------

// Constructor

// ec_ax25_decoder_b::ec_ax25_decoder_b (gr::msg_queue::sptr msgq, bool printing, int print_to_file, const char *filename)
ec_ax25_decoder_b::ec_ax25_decoder_b (bool printing, int print_to_file, const char *filename)
     : gr::sync_block ("ax25_decoder_b",
		       gr::io_signature::make(1, 1, sizeof(unsigned char)),
		       gr::io_signature::make(0, 0, 0)),
      //  d_target_queue(msgq),
       d_printing(printing),
       d_print_to_file(print_to_file),
       d_filename(filename),
       d_state(HUNT),
       d_byte(0x00),
       d_accumulated_bits(0),
       d_bit_buf_size(0),
       d_consecutive_one_bits(0),
       d_flag_cnt(0),
       d_good_byte_cnt(0)
{
  //******INITIALIZATION HERE ******
	message_port_register_out(PDU_PORT_ID);
}



//--------------- Friend (public constructor) ------------------------

ec_ax25_decoder_b_sptr
// ec_make_ax25_decoder_b (gr::msg_queue::sptr msgq, bool printing, int print_to_file, const char *filename)
ec_make_ax25_decoder_b (bool printing, int print_to_file, const char *filename)
{
// return ec_ax25_decoder_b_sptr (new ec_ax25_decoder_b (msgq, printing, print_to_file, filename));
return ec_ax25_decoder_b_sptr (new ec_ax25_decoder_b (printing, print_to_file, filename));
}


//--------------- Public Methods --------------------------------------

// Destructor

ec_ax25_decoder_b::~ec_ax25_decoder_b ()
{
}


int
ec_ax25_decoder_b::work (int noutput_items,
gr_vector_const_void_star &input_items,
gr_vector_void_star &output_items)
{
  const unsigned char * inbuf = (unsigned char *) input_items[0];
  unsigned char *out = (unsigned char *) output_items[0];
  int             i;
  int             nwritten = 0;
//  unsigned char   next_byte;
//  int             bit_count;
//  unsigned char   next_bit;
  // Loop thru each byte of the input stream, one bit per byte
//	printf("%c",d_print_to_file);

  for(i=0; i<noutput_items; i++)
  {
    hdlc_state_machine(inbuf[i] & 0x01);  // Low order bit
    nwritten++;
  }

  return nwritten;
}
