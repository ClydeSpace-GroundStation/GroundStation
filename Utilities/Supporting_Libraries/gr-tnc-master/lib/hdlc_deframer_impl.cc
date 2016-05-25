/* -*- c++ -*- */
/* 
 * Copyright 2013 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */
 
//#define VERBOSE

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "hdlc_deframer_impl.h"
#include <assert.h>
#include <assert.h>
#include <stdexcept>
#include <stdio.h>
#include <gnuradio/blocks/pdu.h>


#define MAX_PACKET_LEN 16384
#define MIN_PACKET_LEN 8
#define FLAG 0x7e

namespace gr {
  namespace tnc {

    hdlc_deframer::sptr
    hdlc_deframer::make()
    {
      return gnuradio::get_initial_sptr
        (new hdlc_deframer_impl());
    }

    /*
     * The private constructor
     */
    hdlc_deframer_impl::hdlc_deframer_impl()
      : gr::sync_block("hdlc_deframer",
        gr::io_signature::make(1, 1, sizeof (unsigned char)),
	    gr::io_signature::make (0,0,0)) {
            
        message_port_register_out(pmt::mp("out"));    
        
		mode=true;
		state=STARTFLAG;
		pktbuf=new unsigned char [MAX_PACKET_LEN];
		sr=0;
		prevbit=0;
		descr=0;
    }

    static unsigned short checkfcs(unsigned char *pktbuf, int bytecount) {
        unsigned short fcs=0xFFFF;
        for (int i=0; i<bytecount-2; i++) {
            fcs = fcs ^ *pktbuf++;
            for (int k=0;k<8;k++) {
                if (fcs & 0x01) fcs = (fcs >> 1) ^ 0x8408;
                else fcs>>=1;
            }
        }
        return(fcs^0xFFFF);
    }

    static char* int2bin(int a) {
        static char str[64];
        int cnt=15;
        while (cnt > -1) {
            str[cnt--]=(a & 0x01)?'1':'0';
            a>>=1;
        } 
        return str;
    } 

    static char* char2bin(char a) {
        static char str[64];
        int cnt=7;
        while (cnt > -1) {
            str[cnt--]=(a & 0x01)?'1':'0';
            a>>=1;
        } 
        return str;
    } 
    /*
     * Our virtual destructor.
     */
    hdlc_deframer_impl::~hdlc_deframer_impl()
    {
    }

    int
    hdlc_deframer_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];

        int n=0;
        while (n < noutput_items){
        bit=*in;
        if (mode) {
            rbit=((descr>>11) & 1) ^ ((descr>>16) & 1) ^ bit;		//LFSR descrambling
            descr<<=1;
            descr|=bit;
            bit=rbit;
        }

        if (prevbit==bit) rbit=1;									//NRZI decoding
        else rbit=0;
        prevbit=bit;

        //TODO: do we need this?
        //rbit = bit;

        #ifdef VERBOSE
        //printf("Got %d (%d)\n",rbit,bit);
        #endif 

        switch (state) {
            case STARTFLAG:			//looking for start of head flags
                sr>>=1;
                if (rbit==1) sr|=0x80;
                if (sr==FLAG) {
                    state=PACKET;
                    bitctr=0;
                    flagctr=1;
        #ifdef VERBOSE
        printf("Start of Head Flags Found\n");
        #endif 				
                }
                break;
            case PACKET:			//looking for packet start (end of head flags)
                sr>>=1;
                if (rbit==1) sr|=0x80;
                bitctr++;
                if (bitctr==8) {
                    bitctr=0;
                    if (sr!=FLAG) {
                        state=ENDFLAG;
                        pktptr=pktbuf;
                        *pktptr=sr;
                        pktptr++;
                        bytectr=1;
                        ones=0;
        #ifdef VERBOSE
        printf("Start of Packet Found %02X after %d FLAGS\n",sr,flagctr);
        #endif					
                    }
                    else {
                        flagctr++;
        #ifdef VERBOSE
//        printf("Got FLAG\n");
        #endif						
                    }
                }
                break;
            case ENDFLAG:					//looking for start of tail flags
                if (ones==5) {
                    if (rbit==0) {	//destuffing
        //printf ("DESTUFFING!!!\n");

                    }
                    else {					//6 bits in a row - FLAG!
                        state=LASTFLAGBIT;	//we need to consume one more bit (last 0 of the flag)
        //printf("End of Packet Found (%d bytes)\n",bytectr);
                        if (bytectr>=MIN_PACKET_LEN) {					//check CRC and if OK send to out queue
                            //unsigned short gfcs = 0;
                            unsigned short gfcs = pktbuf[bytectr-1];
                            gfcs=(gfcs<<8)|pktbuf[bytectr-2];
                            unsigned short cfcs = checkfcs(pktbuf,bytectr);
                            //printf("\nCRC %X %X\n",gfcs,cfcs);
                            if (gfcs==cfcs/*true*/) {
                            //if (1){
                                bytectr-=2;
                                pmt::pmt_t vecpmt(pmt::make_blob(&pktbuf[0], bytectr));
                                pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL, vecpmt));
                                message_port_pub(pmt::mp("out"), pdu);
                            }
                            else {
                                printf("X");
                                fflush(stdout);
                            }
                        }
                    }







                }
                else {
                    *pktptr>>=1;
                    if (rbit==1) *pktptr|=0x80;
                    bitctr++;
                    if (bitctr==8) {
                        bitctr=0;
        #ifdef VERBOSE
        printf("Got BYTE %02X %s (%d)\n",*pktptr,char2bin(*pktptr),bytectr);
        #endif						
                        pktptr++;
                        bytectr++;
                    }
                }	
                if (rbit==1) ones++;
                else ones=0;
                break;
            case LASTFLAGBIT:		//just consume a bit
                state=STARTFLAG;

                sr=0;
                bitctr=0;
                break;
            case END:				//looking for end of tail flags
                sr>>=1;
                if (rbit==1) sr|=0x80;
                bitctr++;
                if (bitctr==8) {
                    bitctr=0;
                    if (sr!=FLAG) {
                        state=STARTFLAG;
                        sr=0;			
        printf("End of Tail Flags Found\n");
		
                    }
                    else {
        #ifdef VERBOSE
        //printf("Got FLAG\n");
        #endif						
                    }
                }
                break;
        }
        in++;
        n++;
        }
        return n;
        }

  } /* namespace tnc */
} /* namespace gr */

