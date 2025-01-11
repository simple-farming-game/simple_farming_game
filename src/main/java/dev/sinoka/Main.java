package dev.sinoka;

import dev.sinoka.utility.Camera;
import dev.sinoka.utility.Shader;
import dev.sinoka.utility.JsonFileReader;

import org.joml.Math;
import org.json.JSONArray;
import org.lwjgl.opengl.*;

import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import java.util.*;

import org.joml.*;
import org.lwjgl.stb.STBImage;
import org.lwjgl.system.MemoryStack;

import static org.lwjgl.glfw.Callbacks.*;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.*;
import static org.lwjgl.system.MemoryUtil.*;

public class Main {

    // Window settings
    private long window;
    private final int SCR_WIDTH = 800;
    private final int SCR_HEIGHT = 600;

    // Camera settings
    private Camera camera = new Camera(new Vector3f(0.0f, 0.0f, 3.0f));
    private float lastX = SCR_WIDTH / 2.0f;
    private float lastY = SCR_HEIGHT / 2.0f;
    private boolean firstMouse = true;

    // Timing
    private float deltaTime = 0.0f;
    private float lastFrame = 0.0f;

    // Lighting
    private Vector3f lightPos = new Vector3f(1.2f, 1.0f, 2.0f);


// OpenGL resource handles
    private int cubeVAO;
    private int lightCubeVAO;
    private int diffuseMap;


    public static void main(String[] args) {
        new Main().run();
    }

    public void run() {

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

        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

        // Load OpenGL
        GL.createCapabilities();

        // Configure OpenGL
        glEnable(GL_DEPTH_TEST);

        // Configure STB
        // STBImage.stbi_set_flip_vertically_on_load(true);

        // Load shaders
        Shader lightingShader = new Shader("assets/shader/vertex.glsl", "assets/shader/fragment.glsl");
        Shader lightCubeShader = new Shader("assets/shader/lightv.glsl", "assets/shader/lightf.glsl");

        JsonFileReader BlockJFR = new JsonFileReader("assets/model/json/block.json");

        JSONArray verticesArray = BlockJFR.readJson().getJSONArray("vertices");
        float[] vertices = new float[verticesArray.length()];
        for (int i = 0; i < verticesArray.length(); i++) {
            vertices[i] = verticesArray.getFloat(i);
        }

        // indices 배열 읽기
        JSONArray indicesArray = BlockJFR.readJson().getJSONArray("indices");
        int[] indices = new int[indicesArray.length()]; // int[]로 선언
        for (int i = 0; i < indicesArray.length(); i++) {
            indices[i] = indicesArray.getInt(i); // getInt()로 정수값 읽기
        }

        cubeVAO = glGenVertexArrays();
        int VBO = glGenBuffers();
        int EBO = glGenBuffers();

        glBindVertexArray(cubeVAO);

        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, 3, GL_FLOAT, false, 8 * Float.BYTES, 3 * Float.BYTES);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, 2, GL_FLOAT, false, 8 * Float.BYTES, 6 * Float.BYTES);
        glEnableVertexAttribArray(2);

        // Prepare light VAO
        lightCubeVAO = glGenVertexArrays();
        glBindVertexArray(lightCubeVAO);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        // Load textures
        diffuseMap = loadTexture("assets/image/grass.png");

        // shader configuration
        lightingShader.use();
        lightingShader.setInt("material.diffuse", 0);
        lightingShader.setInt("material.specular", 1);

        while (!glfwWindowShouldClose(window)) {
            float currentFrame = (float) glfwGetTime();
            deltaTime = currentFrame - lastFrame;
            lastFrame = currentFrame;

            processInput(window);

            glClearColor(0.5f, 0.5f, 0.5f, 0.5f);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

            // be sure to activate shader when setting uniforms/drawing objects
            lightingShader.use();
            lightingShader.setVec3("viewPos", camera.getPosition());
            lightingShader.setFloat("material.shininess", 32.0f);

            // use light
            lightingShader.setBool("useDirLight", false);
            lightingShader.setBool("usePointLights", false);
            lightingShader.setBool("useSpotLight", false);
            lightingShader.setBool("useAmbientLight", true);

            // ambient light
            lightingShader.setVec3("ambientLightColor", new Vector3f(0.2f, 0.2f, 0.2f));
            lightingShader.setFloat("ambientIntensity", 5.0f);

            // dir light
            lightingShader.setVec3("dirLight.direction", new Vector3f(-0.2f, -1.0f, -0.5f));
            lightingShader.setVec3("dirLight.ambient", new Vector3f(0.05f, 0.05f, 0.05f));
            lightingShader.setVec3("dirLight.diffuse", new Vector3f(1.4f, 1.4f, 1.4f));
            lightingShader.setVec3("dirLight.specular", new Vector3f(0.5f, 0.5f, 0.5f));

            // View/projection transformations
            Matrix4f projection = new Matrix4f().perspective((float) Math.toRadians(camera.getZoom()), (float) SCR_WIDTH / (float) SCR_HEIGHT, 0.1f, 100.0f);
            Matrix4f view = camera.getViewMatrix();
            lightingShader.setMat4("projection", projection);
            lightingShader.setMat4("view", view);

            // World transformation
            Matrix4f model = new Matrix4f();
            lightingShader.setMat4("model", model);

            // Bind diffuse map
            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, diffuseMap);

            // Render containers
            glBindVertexArray(cubeVAO);

            // First cube
            model.identity().translate(0.0f, 0.0f, 0.0f);
            lightingShader.setMat4("model", model);
            glDrawElements(GL_TRIANGLES, indices.length, GL_UNSIGNED_INT, 0);

            // Second cube
            model.identity().translate(2.0f, 0.0f, 2.0f).scale(1.0f);
            lightingShader.setMat4("model", model);
            glDrawElements(GL_TRIANGLES, indices.length, GL_UNSIGNED_INT, 0);

            // Swap buffers and poll events
            glfwSwapBuffers(window);
            glfwPollEvents();
        }

        // Free resources
        glfwFreeCallbacks(window);
        glfwDestroyWindow(window);

        glfwTerminate();
        Objects.requireNonNull(glfwSetErrorCallback(null)).free();
    }


    private void processInput(long window) {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            glfwSetWindowShouldClose(window, true);
        }

        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
            camera.processKeyboard(Camera.Movement.FORWARD, deltaTime);
        }
        if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
            camera.processKeyboard(Camera.Movement.BACKWARD, deltaTime);
        }
        if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
            camera.processKeyboard(Camera.Movement.LEFT, deltaTime);
        }
        if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
            camera.processKeyboard(Camera.Movement.RIGHT, deltaTime);
        }
    }

    public int loadTexture(String path) {
        int textureID = glGenTextures();

        try (MemoryStack stack = MemoryStack.stackPush()) {
            IntBuffer width = stack.mallocInt(1);
            IntBuffer height = stack.mallocInt(1);
            IntBuffer nrComponents = stack.mallocInt(1);

            // Load image using STBImage
            ByteBuffer data = STBImage.stbi_load(path, width, height, nrComponents, 0);
            if (data != null) {
                int format;
                if (nrComponents.get(0) == 1) {
                    format = GL_RED;
                } else if (nrComponents.get(0) == 3) {
                    format = GL_RGB;
                } else if (nrComponents.get(0) == 4) {
                    format = GL_RGBA;
                } else {
                    throw new RuntimeException("Unsupported number of components: " + nrComponents.get(0));
                }

                glBindTexture(GL_TEXTURE_2D, textureID);
                glTexImage2D(GL_TEXTURE_2D, 0, format, width.get(0), height.get(0), 0, format, GL_UNSIGNED_BYTE, data);
                glGenerateMipmap(GL_TEXTURE_2D);

                // Set texture wrapping and filtering
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

                STBImage.stbi_image_free(data);
            } else {
                System.err.println("Failed to load texture: " + path);
                STBImage.stbi_image_free(data);
            }
        }

        return textureID;
    }


    private void framebufferSizeCallback(long window, int width, int height) {
        glViewport(0, 0, width, height);
    }

    private void mouseCallback(long window, double xpos, double ypos) {
        float x = (float) xpos;
        float y = (float) ypos;

        if (firstMouse) {
            lastX = x;
            lastY = y;
            firstMouse = false;
        }

        float xoffset = x - lastX;
        float yoffset = lastY - y;
        lastX = x;
        lastY = y;

        camera.processMouseMovement(xoffset, yoffset, true);
    }

    private void scrollCallback(long window, double xoffset, double yoffset) {
        camera.processMouseScroll((float) yoffset);
    }
}