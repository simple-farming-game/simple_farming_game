package dev.sinoka;

import dev.sinoka.utility.*;

import org.lwjgl.opengl.*;

import org.joml.Math;
import org.json.JSONArray;
import org.json.JSONObject;
import org.lwjgl.BufferUtils;

import java.nio.IntBuffer;
import java.util.*;

import org.joml.*;
import org.lwjgl.stb.STBImage;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.*;
import static org.lwjgl.system.MemoryUtil.*;

public class Main {

    // Window settings
    private long window;
    private final int SCR_WIDTH = 800;
    private final int SCR_HEIGHT = 600;

    private int currentScreenWidth = SCR_WIDTH;
    private int currentScreenHeight = SCR_HEIGHT;


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

    private boolean isPause = true;

    private float blockSize = 0.5f;


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

        // Load OpenGL
        GL.createCapabilities();

        // Configure OpenGL
        glEnable(GL_DEPTH_TEST);

        // Configure STB
        STBImage.stbi_set_flip_vertically_on_load(true);


        // Load shaders
        Shader lightingShader = new Shader(ResourceUtil.getAbsolutePath("shader/vertex.glsl"), ResourceUtil.getAbsolutePath("shader/fragment.glsl"));
        Shader lightCubeShader = new Shader(ResourceUtil.getAbsolutePath("shader/lightv.glsl"), ResourceUtil.getAbsolutePath("shader/lightf.glsl"));
        JsonFileReader BlockJFR = new JsonFileReader(ResourceUtil.getAbsolutePath("model/json/block.json"));


        JSONObject blockData = BlockJFR.readJson();
        JSONArray cubeVerticesArray = blockData.getJSONArray("vertices");
        JSONArray cubeIndicesArray = blockData.getJSONArray("indices");

        // cube
        float[] cubeVertices = new float[cubeVerticesArray.length()];
        for (int i = 0; i < cubeVerticesArray.length(); i++) {
            cubeVertices[i] = cubeVerticesArray.getFloat(i);
        }

        // cubeIndices 배열 읽기
        int[] cubeIndices = new int[cubeIndicesArray.length()]; // int[]로 선언
        for (int i = 0; i < cubeIndicesArray.length(); i++) {
            cubeIndices[i] = cubeIndicesArray.getInt(i); // getInt()로 정수값 읽기
        }

        int cubeVAO = glGenVertexArrays();
        int cubeVBO = glGenBuffers();
        int cubeEBO = glGenBuffers();

        glBindVertexArray(cubeVAO);

        glBindBuffer(GL_ARRAY_BUFFER, cubeVBO);
        glBufferData(GL_ARRAY_BUFFER, cubeVertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cubeEBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, cubeIndices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, 3, GL_FLOAT, false, 8 * Float.BYTES, 3 * Float.BYTES);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, 2, GL_FLOAT, false, 8 * Float.BYTES, 6 * Float.BYTES);
        glEnableVertexAttribArray(2);

        // Prepare light VAO
        int lightCubeVAO = glGenVertexArrays();
        glBindVertexArray(lightCubeVAO);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        // Load textures
        int grassTexture = TextureManager.getInstance().loadTexture(ResourceUtil.getAbsolutePath("image/grass.png"));

        // shader configuration
        lightingShader.use();
        lightingShader.setInt("material.diffuse", 0);

        // Text
        JsonFileReader fontJFR = new JsonFileReader(ResourceUtil.getAbsolutePath("font/galmuri.json"));
        Shader textShader = new Shader(ResourceUtil.getAbsolutePath("shader/textVertex.glsl"), ResourceUtil.getAbsolutePath("shader/textFragment.glsl"));

        float[] textVertices = createRectangle(1, 100);

        int[] textIndices = {
                1, 2, 0, // 첫 번째 삼각형 (왼쪽 아래, 오른쪽 아래, 왼쪽 위)
                0, 3, 2  // 두 번째 삼각형 (왼쪽 위, 오른쪽 위, 오른쪽 아래)
        };
        String fontPath = fontJFR.readJson().getString("fontPath");
        System.out.println(fontPath);
        int textTexture = TextureManager.getInstance().loadTexture(ResourceUtil.getAbsolutePath(fontPath));

        int[] textMesh = createVAO(textVertices, textIndices, 2);

        BitmapFont font = new BitmapFont(textMesh[0], textTexture, textShader, fontJFR, SCR_WIDTH, SCR_HEIGHT);

        glBindVertexArray(0);

        // 창 크기 변경시 변수 업데이트
        glfwSetWindowSizeCallback(window, (window, w, h) -> {
            this.currentScreenWidth = w;
            this.currentScreenHeight = h;
        });

        while (!glfwWindowShouldClose(window)) {
            float currentFrame = (float) glfwGetTime();
            deltaTime = currentFrame - lastFrame;
            lastFrame = currentFrame;

            /*IntBuffer w = BufferUtils.createIntBuffer(1);
            IntBuffer h = BufferUtils.createIntBuffer(1);
            glfwGetWindowSize(window, w, h);
            int width = w.get(0);
            int height = h.get(0);*/

            processInput(window);
            if (isPause) {
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
            } else {
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
            }

            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_BLEND);

            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, grassTexture);

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
            Matrix4f view = camera.getViewMatrix();
            Matrix4f projection = new Matrix4f().perspective(
                    (float) Math.toRadians(camera.getZoom()),  // 카메라 줌 (FOV)
                    (float) currentScreenWidth / (float) currentScreenHeight,   // 화면의 종횡비
                    0.01f, 1000.0f // near와 far 클리핑 평면
            );
            lightingShader.setMat4("projection", projection);

            lightingShader.setMat4("view", view);

            // World transformation
            Matrix4f model = new Matrix4f();
            lightingShader.setMat4("model", model);

            // Render containers
            glBindVertexArray(cubeVAO);

            // First cube
            model.identity().translate(0.0f, 0.0f, 0.0f).scale(blockSize);
            lightingShader.setMat4("model", model);
            glDrawElements(GL_TRIANGLES, cubeIndices.length, GL_UNSIGNED_INT, 0);

            // Second cube
            model.identity().translate(2.0f, 0.0f, 2.0f).scale(blockSize);
            lightingShader.setMat4("model", model);
            glDrawElements(GL_TRIANGLES, cubeIndices.length, GL_UNSIGNED_INT, 0);

            // 텍스트 렌더링

            // 셰이더 프로그램 활성화 및 유니폼 설정
            textShader.use();

            // 프로젝션 행렬 설정
            projection = new Matrix4f().setOrtho2D(0.0f, currentScreenWidth, 0.0f, currentScreenHeight);
            textShader.setMat4("projection", projection);


            // 뷰 행렬 설정
            view = new Matrix4f().identity();
            textShader.setMat4("view", view);

            font.renderString("SFG by sinoka", new Vector2f(180, currentScreenHeight-40), 0.3f);

            if (isPause) {
                font.renderString("Pause", new Vector2f(40, currentScreenHeight-40), 0.5f);
            }

            font.setScreenSize(new Vector2f(currentScreenWidth, currentScreenHeight));

            // Swap buffers and poll events
            glfwSwapBuffers(window);
            glfwPollEvents();
        }

        // Unbind VAO and VBO
        // Bind to default VAO (unbind any active VAO)
        glBindVertexArray(0);

        // Delete cube VAO and associated VBO/EBO
        glDeleteBuffers(cubeEBO); // Delete EBO first
        glDeleteBuffers(cubeVBO); // Then delete VBO
        glDeleteVertexArrays(cubeVAO); // Finally delete VAO

        // Delete text VAO and VBO
        glDeleteBuffers(textMesh[2]); // Delete EBO first
        glDeleteBuffers(textMesh[1]); // Delete VBO
        glDeleteVertexArrays(textMesh[0]); // Then delete VAO

        // Unbind and delete textures
        glBindTexture(GL_TEXTURE_2D, 0); // Unbind textures
        glDeleteTextures(textTexture);
        glDeleteTextures(grassTexture);

// Reset OpenGL state
        glDisable(GL_BLEND);
        glUseProgram(0);

// Terminate GLFW
        glfwTerminate();

        Objects.requireNonNull(glfwSetErrorCallback(null)).free();
    }


    private boolean escPressed = false; // ESC 키 상태를 관리

    private void processInput(long window) {
        // ESC 키로 정지 상태를 토글
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS && !escPressed) {
            escPressed = true; // ESC 키가 눌렸음을 표시

            if (isPause) {
                isPause = false; // 정지 해제
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED); // 마우스 커서 비활성화
                firstMouse = true; // 마우스 위치를 초기화하도록 설정
            } else {
                isPause = true; // 정지 상태로 전환
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL); // 마우스 커서 활성화
            }
        }

        // ESC 키가 떼어질 때 상태 초기화
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_RELEASE) {
            escPressed = false;
        }

        // 정지 상태에서는 입력 처리하지 않음
        if (isPause) {
            return;
        }

        // 플레이 상태에서만 키보드 입력 처리
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


    private float[] createRectangle(float ratio, float baseWidth) {
        // 기본 너비를 사용하여 높이 계산
        float width = baseWidth;
        float height = baseWidth / ratio;

        // 반환되는 배열은 꼭짓점 좌표 (X, Y)로만 구성
        return new float[] {
                // X, Y
                -width / 2,  height / 2, // Top-left
                -width / 2, -height / 2, // Bottom-left
                 width / 2, -height / 2, // Bottom-right
                 width / 2,  height / 2  // Top-right
        };
    }



    public int[] createVAO(float[] vertices, int[] indices, int attributeSize) {
        int VAO = glGenVertexArrays();
        int VBO = glGenBuffers();
        int EBO = glGenBuffers();

        glBindVertexArray(VAO);

        // VBO 설정
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        // EBO 설정
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        // 정점 속성 지정
        int stride = attributeSize * Float.BYTES;
        glVertexAttribPointer(0, attributeSize, GL_FLOAT, false, stride, 0);
        glEnableVertexAttribArray(0);

        glBindVertexArray(0); // Unbind VAO

        return new int[]{VAO, VBO, EBO};
    }






    private void framebufferSizeCallback(long window, int width, int height) {
        glViewport(0, 0, width, height);
    }

    private void mouseCallback(long window, double xpos, double ypos) {
        if (isPause) {
            lastX = (float) xpos; // 정지 해제 시 마우스 위치를 초기화
            lastY = (float) ypos;
            return; // 정지 상태에서는 마우스 입력 무시
        }

        float x = (float) xpos;
        float y = (float) ypos;

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
}