package dev.sinoka.core;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.lwjgl.glfw.GLFW;
import org.lwjgl.opengl.GL;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryUtil.*;
import dev.sinoka.utility.Camera;
import org.lwjgl.stb.STBImage;

class WindowManager {
    private long window;
    private static final int SCR_WIDTH = 800;
    private static final int SCR_HEIGHT = 600;

    private boolean isPause = true;

    private float lastX = SCR_WIDTH / 2.0f;
    private float lastY = SCR_HEIGHT / 2.0f;
    private boolean firstMouse = true;

    private Camera camera;
    private static final Logger logger = LogManager.getLogger(WindowManager.class);

    public WindowManager(Camera camera) {
        this.camera = camera;
    }

    public void init() {
        // Initialize GLFW
        if (!glfwInit()) {
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

        // Create window
        window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Simple Farming Game beta", NULL, NULL);
        if (window == NULL) {
            throw new RuntimeException("Failed to create GLFW window");
        }

        glfwMakeContextCurrent(window);
        glfwSetFramebufferSizeCallback(window, this::framebufferSizeCallback);
        glfwSetCursorPosCallback(window, this::mouseCallback);
        glfwSetScrollCallback(window, this::scrollCallback);

        // Load OpenGL
        GL.createCapabilities();

        STBImage.stbi_set_flip_vertically_on_load(true);

        // Configure OpenGL
        glEnable(GL_DEPTH_TEST);
    }

    private void framebufferSizeCallback(long window, int width, int height) {
        glViewport(0, 0, width, height);
    }

    private void mouseCallback(long window, double xpos, double ypos) {
        float x = (float) xpos;
        float y = (float) ypos;

        if (isPause) {
            lastX = x;
            lastY = y;
            firstMouse = true;  // 정지 해제 시 마우스 위치를 새롭게 설정하도록 변경
            return; // 정지 상태에서는 마우스 입력 무시
        }

        if (firstMouse) {
            lastX = x;
            lastY = y;
            firstMouse = false;
        }

        float xoffset = x - lastX;
        float yoffset = lastY - y; // y축은 반대 방향
        lastX = x;
        lastY = y;

        camera.processMouseMovement(xoffset, yoffset, true);
    }

    private void scrollCallback(long window, double xoffset, double yoffset) {
        camera.processMouseScroll((float) yoffset);
    }

    public long getWindow() {
        return window;
    }

    public boolean getPause() {
        return isPause;
    }

    public void setPause(boolean pause) {
        isPause = pause;
    }
}
