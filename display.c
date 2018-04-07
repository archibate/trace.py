#include <GL/glut.h>
#include <math.h>
#include <memory.h>
#include "camera.h"

extern void UpdateRendering(void);

Camera camera;

unsigned int *pixels;
int width = 640;
int height = 480;

void UpdateCamera(void) {
	vsub(camera.dir, camera.target, camera.orig);
	vnorm(camera.dir);

	const Vec up = {0.f, 1.f, 0.f};
	const float fov = (M_PI / 180.f) * 45.f;
	vxcross(camera.x, camera.dir, up);
	vnorm(camera.x);
	vsmul(camera.x, width * fov / height, camera.x);

	vxcross(camera.y, camera.x, camera.dir);
	vnorm(camera.y);
	vsmul(camera.y, fov, camera.y);
}

void idleFunc(void) {
	UpdateRendering();
	glutPostRedisplay();
}

void displayFunc(void) {
	glClear(GL_COLOR_BUFFER_BIT);
	glRasterPos2i(0, 0);
	memset(pixels, 0, width * height * 4);
	glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
}

void ReInit() {
	free(pixels);
	pixels = (unsigned int *) malloc(width * height * 4);
	UpdateCamera();
	UpdateRendering();
}

void reshapeFunc(int newWidth, int newHeight) {
	width = newWidth;
	height = newHeight;

	glViewport(0, 0, width, height);
	glLoadIdentity();
	glOrtho(0.f, width - 1.f, 0.f, height - 1.f, -1.f, 1.f);

	ReInit();

	glutPostRedisplay();
}

void InitGlut(char *windowTittle) {
	glutInitWindowSize(width, height);
	glutInitWindowPosition(0,0);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE);

	glutCreateWindow(windowTittle);

	glutReshapeFunc(reshapeFunc);
	glutDisplayFunc(displayFunc);
	glutIdleFunc(idleFunc);
}

int main(int argc, char **argv) {
	glutInit(&argc, argv);
	InitGlut("OpenGL/FreeGLUT Window");
	ReInit();
	glutMainLoop();
}
