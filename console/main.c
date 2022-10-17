#include <stdio.h>

void gotoxy(int x, int y){
	COORD pos = {x,y};
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);
}

int main(){

    gotoxy(100, 100);
    printf("hello \n");

    return 0;
}