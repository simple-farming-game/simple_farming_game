package dev.sinoka;

import dev.sinoka.block.Block;
import dev.sinoka.block.BlockBuilder;
import dev.sinoka.registry.BlockRegister;
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
    private int SCR_WIDTH = 800;
    private int SCR_HEIGHT = 600;

    // Player
    private Vector3f playerPos = new Vector3f(0, 5.0f, 0); // 시작 위치 높게 설정 (낙하 확인)
    private float playerSpeed = 3.5f;
    private float gravity = -9.81f; // 중력 값
    private float verticalVelocity = 0.0f; // 현재 수직 속도
    private float groundLevel = 0.5f; // 플레이어가 착지할 수 있는 바닥 높이
    private boolean isJumping = false; // 점프 여부 확인
    private float jumpForce = 5.0f; // 점프 힘


    // Camera settings
    private Camera camera = new Camera(new Vector3f(playerPos.x, playerPos.y + 1f, playerPos.z));
    private float lastX = SCR_WIDTH / 2.0f;
    private float lastY = SCR_HEIGHT / 2.0f;
    private boolean firstMouse = true;

    // Timing
    private float deltaTime = 0.0f;
    private float lastFrame = 0.0f;

    // Lighting
    private Vector3f lightPos = new Vector3f(1.2f, 1.0f, 2.0f);

    private boolean isPause = true;

    List<Vector3f> map = new ArrayList<Vector3f>();

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
        ShaderManager shaderManager = ShaderManager.getInstance();
        Shader lightCubeShader = new Shader(ResourceUtil.getAbsolutePath("shader/lightv.glsl"), ResourceUtil.getAbsolutePath("shader/lightf.glsl"));

        // Prepare light VAO
        int lightCubeVAO = glGenVertexArrays();
        glBindVertexArray(lightCubeVAO);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        // Load textures
        Texture grassTexture = new Texture(ResourceUtil.getAbsolutePath("image/grass.png"));

        // block
        Block grassBlock = new BlockBuilder().setBlockID("grass").setBreakable(true).setTextureID(grassTexture).setStrength(0.5f).build();

        // shader configuration
        shaderManager.useDefaultShader();
        shaderManager.getDefaultShader().setInt("material.diffuse", 0);

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
        Texture textTexture = new Texture(ResourceUtil.getAbsolutePath(fontPath));

        int[] textMesh = createVAO(textVertices, textIndices, 2);

        BitmapFont font = new BitmapFont(textMesh[0], textTexture, textShader, fontJFR, SCR_WIDTH, SCR_HEIGHT);

        glBindVertexArray(0);

        for (int i = 0; i < 50; i++) {
            for (int j = 0; j < 50; j++) {
                map.add(new Vector3f(i*0.5f,0,j*0.5f));
            }
        }

        while (!glfwWindowShouldClose(window)) {
            float currentFrame = (float) glfwGetTime();
            deltaTime = currentFrame - lastFrame;
            lastFrame = currentFrame;

            IntBuffer w = BufferUtils.createIntBuffer(1);
            IntBuffer h = BufferUtils.createIntBuffer(1);
            glfwGetWindowSize(window, w, h);
            int width = w.get(0);
            int height = h.get(0);

            processInput(window);
            if (isPause) {
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
            } else {
                glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
            }

            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_BLEND);

            glActiveTexture(GL_TEXTURE0);
            grassTexture.bind();

            glClearColor(0.5f, 0.5f, 0.5f, 0.5f);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

            // be sure to activate shader when setting uniforms/drawing objects
            shaderManager.getDefaultShader().use();
            shaderManager.getDefaultShader().setVec3("viewPos", camera.getPosition());
            shaderManager.getDefaultShader().setFloat("material.shininess", 32.0f);

            // use light
            shaderManager.getDefaultShader().setBool("useDirLight", false);
            shaderManager.getDefaultShader().setBool("usePointLights", false);
            shaderManager.getDefaultShader().setBool("useSpotLight", false);
            shaderManager.getDefaultShader().setBool("useAmbientLight", true);

            // ambient light
            shaderManager.getDefaultShader().setVec3("ambientLightColor", new Vector3f(0.2f, 0.2f, 0.2f));
            shaderManager.getDefaultShader().setFloat("ambientIntensity", 5.0f);

            // dir light
            shaderManager.getDefaultShader().setVec3("dirLight.direction", new Vector3f(-0.2f, -1.0f, -0.5f));
            shaderManager.getDefaultShader().setVec3("dirLight.ambient", new Vector3f(0.05f, 0.05f, 0.05f));
            shaderManager.getDefaultShader().setVec3("dirLight.diffuse", new Vector3f(1.4f, 1.4f, 1.4f));
            shaderManager.getDefaultShader().setVec3("dirLight.specular", new Vector3f(0.5f, 0.5f, 0.5f));


            // View/projection transformations
            Matrix4f view = camera.getViewMatrix();
            Matrix4f projection = new Matrix4f().perspective(
                    (float) Math.toRadians(camera.getZoom()),  // 카메라 줌 (FOV)
                    (float) width / (float) height,   // 화면의 종횡비
                    0.01f, 1000.0f // near와 far 클리핑 평면
            );
            shaderManager.getDefaultShader().setMat4("projection", projection);

            shaderManager.getDefaultShader().setMat4("view", view);

            // World transformation
            Matrix4f model = new Matrix4f();
            shaderManager.getDefaultShader().setMat4("model", model);

            for (Vector3f blockPos : map.toArray(map.toArray(new Vector3f[map.size()]))) {
                grassBlock.render(blockPos);
            }

            // 텍스트 렌더링
            // 셰이더 프로그램 활성화 및 유니폼 설정
            textShader.use();

            // 프로젝션 행렬 설정
            projection = new Matrix4f().setOrtho2D(0.0f, width, 0.0f, height);
            textShader.setMat4("projection", projection);


            // 뷰 행렬 설정
            view = new Matrix4f().identity();
            textShader.setMat4("view", view);

            font.renderString("SFG by sinoka", new Vector2f(180, height-40), 0.3f);

            if (isPause) {
                font.renderString("Pause", new Vector2f(40, height-40), 0.5f);
            }

            font.setScreenSize(new Vector2f(width, height));

            // Swap buffers and poll events
            glfwSwapBuffers(window);
            glfwPollEvents();
        }

        // Unbind VAO and VBO
        // Bind to default VAO (unbind any active VAO)
        glBindVertexArray(0);

        // Delete text VAO and VBO
        glDeleteBuffers(textMesh[2]); // Delete EBO first
        glDeleteBuffers(textMesh[1]); // Delete VBO
        glDeleteVertexArrays(textMesh[0]); // Then delete VAO

        grassBlock.delete();

        // Unbind and delete textures
        glBindTexture(GL_TEXTURE_2D, 0); // Unbind textures
        textTexture.delete();
        grassTexture.delete();

// Reset OpenGL state
        glDisable(GL_BLEND);
        glUseProgram(0);

// Terminate GLFW
        glfwTerminate();

        Objects.requireNonNull(glfwSetErrorCallback(null)).free();
    }


    private boolean escPressed = false; // ESC 키 상태를 관리

    private boolean isOnGround(Vector3f playerPos) {
        float blockSize = 0.5f; // 블록 크기
        float closestGround = -Float.MAX_VALUE; // 가장 낮은 값으로 초기화
        boolean foundGround = false;

        for (Vector3f blockPos : map) {
            // 플레이어의 x, z 좌표가 블록의 x, z 중심에서 ±0.5f 이내인지 확인
            if (Math.abs(playerPos.x - blockPos.x) < blockSize && Math.abs(playerPos.z - blockPos.z) < blockSize) {
                // 플레이어보다 높은 블록은 무시 (아래에 있는 블록만 고려)
                if (blockPos.y + blockSize <= playerPos.y && blockPos.y + blockSize > closestGround) {
                    closestGround = blockPos.y + blockSize;
                    foundGround = true;
                }
            }
        }

        if (foundGround) {
            groundLevel = closestGround;
            return true;
        } else {
            // 허공이면 기본 groundLevel 설정 (플레이어가 떨어지도록)
            groundLevel = -Float.MAX_VALUE;
            return false;
        }
    }

    private void plyerMove(long window) {
        // 플레이 상태에서만 키보드 입력 처리
        boolean forward = glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS;
        boolean backward = glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS;
        boolean left = glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS;
        boolean right = glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS;
        boolean jump = glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS;

        // 이동 속도 계산
        float velocity = playerSpeed * deltaTime; // `playerSpeed`는 플레이어 이동 속도 변수

        // 이동 벡터 초기화
        Vector3f moveVector = new Vector3f();

        // 방향별 이동 벡터 추가
        if (forward && left) {
            moveVector.add(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
            moveVector.sub(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        } else if (forward && right) {
            moveVector.add(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
            moveVector.add(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        } else if (backward && left) {
            moveVector.sub(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
            moveVector.sub(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        } else if (backward && right) {
            moveVector.sub(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
            moveVector.add(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        } else if (forward) {
            moveVector.add(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
        } else if (backward) {
            moveVector.sub(new Vector3f(camera.getFront().x, 0, camera.getFront().z));
        } else if (left) {
            moveVector.sub(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        } else if (right) {
            moveVector.add(new Vector3f(camera.getRight().x, 0, camera.getRight().z));
        }

        // 이동 벡터 정규화 및 적용
        if (moveVector.lengthSquared() != 0) {
            moveVector.normalize().mul(velocity);
            playerPos.add(moveVector);
        }

        // 점프 기능
        if (jump && playerPos.y <= groundLevel + 0.01f) { // 바닥에 있을 때만 점프 가능
            verticalVelocity = jumpForce; // 점프 시 위로 상승
            isJumping = true;
        }

        // 중력 적용 (항상 중력 가속도 적용)
        verticalVelocity += gravity * deltaTime;

        // y축 업데이트
        playerPos.y += verticalVelocity * deltaTime;

        // 바닥 충돌 감지
        if (playerPos.y < groundLevel) {
            playerPos.y = groundLevel;
            verticalVelocity = 0; // 착지 후 중력 중지
            isJumping = false;
        }

        // 카메라 위치 업데이트 (플레이어 머리 높이 설정)
        camera.setPlayerPos(playerPos, deltaTime);
        System.out.println(isOnGround(playerPos));
    }

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

        plyerMove(window);
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