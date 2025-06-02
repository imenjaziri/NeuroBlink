#include <gui/screen1_screen/Screen1View.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
Screen1View::Screen1View()
{

}

void Screen1View::setupScreen()
{
    Screen1ViewBase::setupScreen();
    Unicode::strncpy(textArea1Buffer, "", TEXTAREA1_SIZE);
    textArea1.setWildcard(textArea1Buffer);
}

void Screen1View::tearDownScreen()
{
    Screen1ViewBase::tearDownScreen();
}
void Screen1View::uart_Data(char *data)
	{
	    int currentLength = Unicode::strlen(textArea1Buffer);
	    Unicode::strncpy(textArea1Buffer + currentLength, data, TEXTAREA1_SIZE - currentLength - 1);
	    textArea1Buffer[TEXTAREA1_SIZE - 1] = '\0';

	    textArea1.invalidate();
	}
