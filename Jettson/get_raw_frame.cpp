//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//

#include "libpixyusb2.h"
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <string.h>
#include <fstream>
#include <queue>
#include <string.h>
#include <chrono>
using namespace std;

Pixy2        pixy;


int writePPM(uint16_t width, uint16_t height, uint32_t *image, const char *filename)
{

  int i, j;
  char fn[32];

  sprintf(fn, "%s.ppm", filename);
  FILE *fp = fopen(fn, "wb");
  if (fp==NULL)
    return -1;
  fprintf(fp, "P6\n%d %d\n255\n", width, height);
  for (j=0; j<height; j++)
  {
    for (i=0; i<width; i++)
      fwrite((char *)(image + j*width + i), 1, 3, fp);
  }
  fclose(fp);
  return 0;
}

int demosaic(uint16_t width, uint16_t height, const uint8_t *bayerImage, uint32_t *image)
{
  uint32_t x, y, xx, yy, r, g, b;
  uint8_t *pixel0, *pixel;
  
  for (y=0; y<height; y++)
  {
    yy = y;
    if (yy==0)
      yy++;
    else if (yy==height-1)
      yy--;
    pixel0 = (uint8_t *)bayerImage + yy*width;
    for (x=0; x<width; x++, image++)
    {
      xx = x;
      if (xx==0)
	xx++;
      else if (xx==width-1)
	xx--;
      pixel = pixel0 + xx;
      if (yy&1)
      {
        if (xx&1)
        {
          r = *pixel;
          g = (*(pixel-1)+*(pixel+1)+*(pixel+width)+*(pixel-width))>>2;
          b = (*(pixel-width-1)+*(pixel-width+1)+*(pixel+width-1)+*(pixel+width+1))>>2;
        }
        else
        {
          r = (*(pixel-1)+*(pixel+1))>>1;
          g = *pixel;
          b = (*(pixel-width)+*(pixel+width))>>1;
        }
      }
      else
      {
        if (xx&1)
        {
          r = (*(pixel-width)+*(pixel+width))>>1;
          g = *pixel;
          b = (*(pixel-1)+*(pixel+1))>>1;
        }
        else
        {
          r = (*(pixel-width-1)+*(pixel-width+1)+*(pixel+width-1)+*(pixel+width+1))>>2;
          g = (*(pixel-1)+*(pixel+1)+*(pixel+width)+*(pixel-width))>>2;
          b = *pixel;
        }
      }
      *image = (b<<16) | (g<<8) | r; 
    }
  }
}


int main()
{
  int  Result;
  uint8_t *bayerFrame;
  uint32_t rgbFrame[PIXY2_RAW_FRAME_WIDTH*PIXY2_RAW_FRAME_HEIGHT];
  
  const char *send_fifo_path = "/home/nitro/pixy2/build/get_raw_frame/pipe2";
  const char *receive_fifo_path = "/home/nitro/pixy2/build/get_raw_frame/pipe1";  // Path to the named pipe
  char buffer[256];
  
  
  printf ("=============================================================\n");
  printf ("= PIXY2 Get Raw Frame Example                               =\n");
  printf ("=============================================================\n");

  printf ("Connecting to Pixy2...");

  // Initialize Pixy2 Connection //
  {
    Result = pixy.init();

    if (Result < 0)
    {
      printf ("Error\n");
      printf ("pixy.init() returned %d\n", Result);
      return Result;
    }

    printf ("Success\n");
  }

  // Get Pixy2 Version information //
  {
    Result = pixy.getVersion();

    if (Result < 0)
    {
      printf ("pixy.getVersion() returned %d\n", Result);
      return Result;
    }

    pixy.version->print();
  }

  // need to call stop() befroe calling getRawFrame().
  // Note, you can call getRawFrame multiple times after calling stop().
  // That is, you don't need to call stop() each time.
  pixy.m_link.stop();
  
  
// Create the named pipe if it doesn't exist
    if (mkfifo(send_fifo_path, 0666) == -1) {
        perror("mkfifo");
    }

    void *shared_memory;
    int shmid;
    shmid=shmget((key_t)1000,1000000,0666|IPC_CREAT);

    int i = 0;
int divizor = 0;
	auto start_time = std::chrono::high_resolution_clock::now();
  while(1) {
  

  	pixy.m_link.stop();	
  
  	//usleep(1000);
	// grab raw frame, BGGR Bayer format, 1 byte per pixel
	pixy.m_link.getRawFrame(&bayerFrame);
	// convert Bayer frame to RGB frame
	demosaic(PIXY2_RAW_FRAME_WIDTH, PIXY2_RAW_FRAME_HEIGHT, bayerFrame, rgbFrame);
	// write frame to PPM file for verification
	//Result = writePPM(PIXY2_RAW_FRAME_WIDTH, PIXY2_RAW_FRAME_HEIGHT, rgbFrame, "image");
	

	
  
  	//if (Result==0)
    		//printf("Write frame to out.ppm\n");
    
	int fd = open(receive_fifo_path, O_RDONLY);
	if (fd == -1) {
	    perror("open");
	    return 1;
	}
	ssize_t bytesRead = read(fd, buffer, sizeof(buffer));

	buffer[bytesRead] = '\0';

	//std::cout << "C++ program received message: " << buffer << std::endl;

	//SHARED MEMORY STORING
	//string path = "/home/nitro/pixy2/build/get_raw_frame/image.ppm";
	//ifstream ppm_file(path, ios::binary);
	//cout<<path<<endl;

	/*if (!ppm_file) {
	    cerr << "Failed to open .ppm file." << endl;
	    return 1;
	}*/

	//printf("Key of shared memory is %d\n",shmid);
	shared_memory=shmat(shmid,NULL,0);
	char *writeptr = (char*)shared_memory;
	//printf("Process attached at %p\n",shared_memory);
	//int memorie=shm_open(shared_memory,O_RDWR,0);
	//ppm_file.read(static_cast<char*>(shared_memory), 1000000);		//TODO elimina discul
	  int latime, inaltime;
		//incercare de evitare fisier
	  //fprintf(shared_memory, "P6\n%d %d\n255\n", PIXY2_RAW_FRAME_WIDTH, PIXY2_RAW_FRAME_HEIGHT);
	const char header_ppm[] = "P6 316 208 255 ";
	for(int i=0;i<sizeof(header_ppm);i++){
		//*((char*)(shared_memory)+i) = *((char*)header_ppm+i);
		*(writeptr++) =*(header_ppm+i);
	}
	  for (inaltime=0; inaltime<208/*PIXY2_RAW_FRAME_HEIGHT*/; inaltime++)
	  {
	    for (latime=0; latime<316/*PIXY2_RAW_FRAME_WIDTH*/; latime++) {
	      //fwrite((char *)(rgbFrame + j*PIXY2_RAW_FRAME_WIDTH + i), 1, 3, (const char*)shared_memory);
		//brg
		*(writeptr++)=*((char*)(rgbFrame + inaltime*316+latime) + 1);//r
		*(writeptr++)=*((char*)(rgbFrame + inaltime*316+latime) + 2);//g
		*(writeptr++)=*((char*)(rgbFrame + inaltime*316+latime) + 0);//b
		}
	  }

	close(fd);

	// Open the named pipe for writing
	fd = open(send_fifo_path, O_WRONLY);
	if (fd == -1) {
	    perror("open");
	    return 1;
	}

	// Message to send
	std::string message = "DISPLAY THE IMAGE!";

	// Write the message to the named pipe
	ssize_t bytesWritten = write(fd, message.c_str(), message.size());
	if (bytesWritten == -1) {
	    perror("write");
	    close(fd);
	    return 1;
	}

	// Close the named pipe
	close(fd);

	//std::cout << "C++ program has sent a message to the named pipe." << std::endl;

	if(i==10)
	    i=0;

        
        //pixy.m_link.resume();
        
        /*if(pixy.line.numVectors > 0)
        	pixy.line.vectors[0].print();*/
        	
        auto end_time = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
start_time=end_time;
	if(divizor++>30){
		std::cout << i << ": " << duration.count() << " ms" << std::endl;
		divizor=0;
	}


	}
  
  // Call resume() to resume the current program, otherwise Pixy will be left
  // in "paused" state.  
  
  }
  


























