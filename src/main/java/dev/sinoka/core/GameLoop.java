package dev.sinoka.core;

// 중요!:
// drawTexture 를 사용하여 화면에 2d 를 그리는경우
// 절대적 크기를 사용하면 안됩니다.(상대적 크기를 사용해야합니다.)
// 예를들어 화면 크기의 몇배, 화면 꼭대기에서 옆으로 몇픽셀 식입니다.

import dev.sinoka.block.Block;
import dev.sinoka.entity.CompoundCollision;
import dev.sinoka.entity.Player;
import dev.sinoka.input.InputManager;
import dev.sinoka.renderer.ModelRenderer;
import dev.sinoka.renderer.TextureRenderer;
import dev.sinoka.utility.*;
import dev.sinoka.world.World;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.joml.Vector4f;
import org.lwjgl.BufferUtils;
import org.w3c.dom.Text;

import java.nio.IntBuffer;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.glEnableVertexAttribArray;
import static org.lwjgl.opengl.GL20.glVertexAttribPointer;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

class GameLoop {
    private final WindowManager windowManager;
    private final Camera camera;
    private final Player player;
    private final World world;
    private final InputManager inputManager;
    private final BitmapFont bitmapFont;

    private float deltaTime = 0.0f;
    private float lastFrame = 0.0f;
    private boolean isPause;
    private boolean escPressed = false;
    private long window;

    private Texture selectTexture = new Texture(new Vector4f(1,1,1, 0.5f));
    private Texture crosshairTexture = new Texture(ResourceUtil.getAbsolutePath("resources/image/ui/crosshair.png"));

    private int VAO;
    private int VBO;
    private int EBO;

    private float playerSpeed = 5.0f;
    private final float jumpForce = 5.0f;
    private static final float GRAVITY = -9.8f;

    private String wolrdName = "testing";

    private static final Logger logger = LogManager.getLogger(GameLoop.class);

    public GameLoop(WindowManager windowManager, Camera camera, Player player, World world) {
        this.windowManager = windowManager;
        this.camera = camera;
        this.player = player;
        this.world = world;
        this.inputManager = new InputManager(windowManager.getWindow());
        JsonFileReader bitmapFontJFR = new JsonFileReader(ResourceUtil.getAbsolutePath("resources/font/galmuri.json"));
        this.bitmapFont = new BitmapFont(ShaderManager.getInstance().getShader("text"), bitmapFontJFR);
    }

    public void start() {

        createMesh();

        while (!glfwWindowShouldClose(this.windowManager.getWindow())) {
            float startTime = (float) glfwGetTime();
            deltaTime = startTime - lastFrame;
            lastFrame = startTime;
            Block selectBlock = player.getSelectBlock(world, camera, this.wolrdName);
            Vector3f selectBlockPos = player.getSelectBlockPos(world, camera, this.wolrdName);
//
            window = this.windowManager.getWindow();
            isPause = windowManager.getPause();
            int screenWidth = windowManager.getScrWidth();
            int screenHeight = windowManager.getScrHeight();
            float screenHeightPercent = screenHeight * 0.01f;
            TextureRenderer.getInstance().setScreenSize(screenWidth,screenHeight);
            camera.setWindowSize(screenWidth,screenHeight);

            camera.updateMatrices();

            // 🎮 키 입력 처리
            processInput();
            handleMouseMode();

            // 🎨 화면 초기화
            glClearColor(0.5f, 0.8f, 1f, 1f);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glEnable(GL_BLEND);
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_DEPTH_TEST);

            // 🔆 셰이더 설정
            Shader shader = ShaderManager.getInstance().getDefaultShader();
            shader.use();
            configureShader(shader);

            // 🏞️ 장면 렌더링
            renderScene();

            glDepthFunc(GL_LEQUAL);
            logger.debug(selectBlockPos);
            if (selectBlock != null) {
                ModelRenderer.getInstance().render(selectBlock.getModel(), selectTexture, selectBlockPos.floor(), 1, false);
            }
            glDepthFunc(GL_LESS);

            // UI 렌더링
            glDisable(GL_DEPTH_TEST);
            Shader textShader = ShaderManager.getInstance().getShader("text");
            textShader.use();

            Matrix4f projection = new Matrix4f().setOrtho2D(0, windowManager.getScrWidth(), 0.0f, windowManager.getScrHeight());
            textShader.setMat4("projection", projection);

            // 뷰 행렬 설정
            Matrix4f view = new Matrix4f().identity();
            textShader.setMat4("view", view);

            // 텍스트 렌더링
            bitmapFont.renderString(wolrdName+" 월드입니다. Hello, World! 안녕, 세상!", new Vector2f(40, windowManager.getScrHeight()-40), 0.2f);

            if (windowManager.getPause()) {
                bitmapFont.renderString("일시정지 Pause", new Vector2f(40, windowManager.getScrHeight()-80), 0.2f);
            }

            float screenRatio = screenWidth / screenHeight;

            // TextureRenderer.getInstance().drawTexture(
            //         crosshairTexture,
            //         new Vector2f(0, 0),         // UV 좌표 (왼쪽 상단)
            //         new Vector2f(8, 8),         // UV 크기 (텍스처에서 사용할 영역)
            //         VAO,
            //         ShaderManager.getInstance().getShader("text"),
            //         new Vector2f(screenWidth/2+(8*(screenHeightPercent*3*screenRatio))/2, screenHeight/2+(8*(screenHeightPercent*3))/2),
            //         new Vector2f(screenHeightPercent*3, screenHeightPercent*3)
            // );

            // 🎮 이벤트 처리
            glfwSwapBuffers(window);
            glfwPollEvents();
        }
        cleanup();
    }



    private void handleMouseMode() {
        glfwSetInputMode(window, GLFW_CURSOR, isPause ? GLFW_CURSOR_NORMAL : GLFW_CURSOR_DISABLED);
    }

    private void configureShader(Shader shader) {
        shader.setBool("useDirLight", false);
        shader.setBool("usePointLights", false);
        shader.setBool("useSpotLight", false);
        shader.setBool("useAmbientLight", true);
        shader.setVec3("viewPos", camera.getPosition());
        shader.setFloat("material.shininess", 32.0f);
        shader.setVec3("ambientLightColor", new Vector3f(0.2f, 0.2f, 0.2f));
        shader.setFloat("ambientIntensity", 5.0f);

        IntBuffer w = BufferUtils.createIntBuffer(1);
        IntBuffer h = BufferUtils.createIntBuffer(1);
        glfwGetWindowSize(window, w, h);


        shader.setMat4("projection", camera.getProjectionMatrix());
        shader.setMat4("view", camera.getViewMatrix());
    }

    private void renderScene() {
        world.render(wolrdName);
    }

    private void processInput() {
        inputManager.update(); // ✅ 키 입력 업데이트

        // ✅ ESC 키 감지 (연속 입력 방지)
        if (inputManager.isKeyHeld(GLFW_KEY_ESCAPE)) {
            if (!escPressed) {
                escPressed = true; // ✅ ESC 키가 눌렸을 때 플래그 설정
                isPause = !isPause;
                windowManager.setPause(isPause);
                handleMouseMode();
            }
        } else {
            escPressed = false; // ✅ ESC 키를 떼면 플래그 초기화
        }

        if (!isPause) {
            if (inputManager.isKeyPressed(GLFW_KEY_R)) {
                resetPlayer();
            }
            handlePlayerMovement(window);
        }
    }


    private void handlePlayerMovement(long window) {
        Vector3f moveVector = new Vector3f();
        Vector3f playerPos = new Vector3f(player.getPos()); // 플레이어 위치 복사
        Vector3f velocity = new Vector3f(player.getVelocity()); // 현재 속도 복사

        // ✅ 카메라 방향 기반 이동 (XZ 평면에서 이동)
        Vector3f front = new Vector3f(camera.getFront().x, 0, camera.getFront().z).normalize();
        Vector3f right = new Vector3f(camera.getRight().x, 0, camera.getRight().z).normalize();

        boolean forward = glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS;
        boolean backward = glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS;
        boolean left = glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS;
        boolean rightMove = glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS;
        boolean jump = glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS;

        // ✅ 이동 벡터 계산
        if (forward) moveVector.add(front);
        if (backward) moveVector.sub(front);
        if (left) moveVector.sub(right);
        if (rightMove) moveVector.add(right);

        if (moveVector.lengthSquared() > 0) {
            moveVector.normalize().mul(playerSpeed * deltaTime);
            playerPos.add(moveVector);
        }

        // ✅ 중력 적용 (이제 피직스 엔진이 없으므로 직접 적용)
        if (!isOnGround(player)) {
            velocity.y += GRAVITY * deltaTime;
        } else {
            velocity.y = 0; // 바닥에 있을 경우 중력 초기화
        }

        // ✅ 점프 처리
        if (jump && isOnGround(player)) {
            velocity.y = jumpForce; // 직접 점프 적용
        }


        // ✅ 최종 위치 반영
        playerPos.y += velocity.y * deltaTime;
        player.setPos(playerPos);
        player.setVelocity(velocity);

        // ✅ 카메라 위치 업데이트 (플레이어 머리 위치로)
        camera.setPlayerPos(player.getPos(), deltaTime);
    }

    public boolean isOnGround(Player aPlayer) {
        CompoundCollision compoundCollision = world.getCompoundCollision(wolrdName);
        if (compoundCollision == null) {
            System.err.println("❌ CompoundCollision for map '"+wolrdName+"' is null!");
            return false; // 기본값 false 반환 (또는 원하는 동작 수행)
        }

        return compoundCollision.intersects(aPlayer.getCollision());
    }


    private void resetPlayer() {
        Vector3f resetPosition = new Vector3f(0, 5f, 0);
        player.setPos(resetPosition);
        player.setVelocity(new Vector3f(0, 0, 0));
    }

    private void cleanup() {
        logger.debug("🚀 Cleaning up resources...");
        ShaderManager.getInstance().cleanup();
        bitmapFont.cleanup();
        world.cleanup();
        glfwDestroyWindow(windowManager.getWindow());
        glfwTerminate();
        logger.debug("✅ Cleanup completed!");
    }

    private static final float[] VERTICES = {
            -4.0f,  4.0f,  // 왼쪽 위 (-470/2, +470/2)
            -4.0f, -4.0f,  // 왼쪽 아래 (-470/2, -470/2)
            4.0f, -4.0f,   // 오른쪽 아래 (+470/2, -470/2)
            4.0f,  4.0f    // 오른쪽 위 (+470/2, +470/2)
    };

    private static final int[] INDICES = {1, 2, 0, 0, 3, 2};

    private void createMesh() {
        int attributeSize = 2;
        int stride = attributeSize * Float.BYTES;

        VAO = glGenVertexArrays();  // Generate VAO_EN
        VBO = glGenBuffers();
        EBO = glGenBuffers();

        glBindVertexArray(VAO);
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, VERTICES, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, INDICES, GL_STATIC_DRAW);

        glVertexAttribPointer(0, attributeSize, GL_FLOAT, false, stride, 0);
        glEnableVertexAttribArray(0);
        glBindVertexArray(0); // Unbind int VAO
    }
}
