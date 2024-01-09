#include <SDL2/SDL.h>
#include <stdlib.h>
#include <stdio.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600
#define HELICOPTER_WIDTH 50
#define HELICOPTER_HEIGHT 30
#define HELICOPTER_SPEED 5

SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
SDL_Texture *helicopterTexture = NULL;
SDL_Rect helicopterRect;

void initializeSDL() {
    SDL_Init(SDL_INIT_VIDEO);
    window = SDL_CreateWindow("Choplifter", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);
}

void loadMedia() {
    SDL_Surface *helicopterSurface = SDL_LoadBMP("helicopter.bmp");
    helicopterTexture = SDL_CreateTextureFromSurface(renderer, helicopterSurface);
    SDL_FreeSurface(helicopterSurface);

    helicopterRect.x = SCREEN_WIDTH / 2 - HELICOPTER_WIDTH / 2;
    helicopterRect.y = SCREEN_HEIGHT / 2 - HELICOPTER_HEIGHT / 2;
    helicopterRect.w = HELICOPTER_WIDTH;
    helicopterRect.h = HELICOPTER_HEIGHT;
}

void closeSDL() {
    SDL_DestroyTexture(helicopterTexture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}

int main(int argc, char *argv[]) {
    initializeSDL();
    loadMedia();

    SDL_Event e;
    int quit = 0;

    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = 1;
            }
            else if (e.type == SDL_KEYDOWN) {
                switch (e.key.keysym.sym) {
                    case SDLK_UP:
                        helicopterRect.y -= HELICOPTER_SPEED;
                        break;
                    case SDLK_DOWN:
                        helicopterRect.y += HELICOPTER_SPEED;
                        break;
                    case SDLK_LEFT:
                        helicopterRect.x -= HELICOPTER_SPEED;
                        break;
                    case SDLK_RIGHT:
                        helicopterRect.x += HELICOPTER_SPEED;
                        break;
                }
            }
        }

        SDL_RenderClear(renderer);
        SDL_RenderCopy(renderer, helicopterTexture, NULL, &helicopterRect);
        SDL_RenderPresent(renderer);
    }

    closeSDL();

    return 0;
}
