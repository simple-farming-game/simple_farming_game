package dev.sinoka.core;

import dev.sinoka.block.Block;
import dev.sinoka.entity.Player;
import dev.sinoka.input.InputManager;
import dev.sinoka.physics.PhysicsEngine;
import dev.sinoka.utility.Camera;
import dev.sinoka.utility.Shader;
import dev.sinoka.utility.ShaderManager;
import dev.sinoka.world.World;
import org.joml.Matrix4f;
import org.joml.Vector3f;
import org.lwjgl.BufferUtils;

import java.nio.IntBuffer;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

class GameLoop {
    private final WindowManager windowManager;
    private final Camera camera;
    private final Player player;
    private final World world;
    private final InputManager inputManager;
    private final PhysicsEngine physicsEngine;

    private float deltaTime = 0.0f;
    private float lastFrame = 0.0f;
    private boolean isPause;
    private boolean escPressed = false;
    private long window;

    private final float playerSpeed = 5.0f;
    private final float jumpForce = 5.0f;
    private static final float GRAVITY = -9.8f;

    public GameLoop(WindowManager windowManager, Camera camera, Player player, World world) {
        this.windowManager = windowManager;
        this.camera = camera;
        this.player = player;
        this.world = world;
        this.inputManager = new InputManager(windowManager.getWindow());
        this.physicsEngine = new PhysicsEngine(world);
    }

    private static final float FIXED_TIMESTEP = 1.0f / 60.0f; // 60FPS 기준
    private float accumulator = 0.0f;

    public void start() {
        while (!glfwWindowShouldClose(this.windowManager.getWindow())) {
            float startTime = (float) glfwGetTime();
            deltaTime = startTime - lastFrame;
            lastFrame = startTime;

            window = this.windowManager.getWindow();
            isPause = windowManager.getPause();

            // 🎮 키 입력 처리
            processInput();
            handleMouseMode();

            // 🎨 화면 초기화
            glClearColor(0.5f, 0.8f, 1f, 1f);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glEnable(GL_BLEND);
            glEnable(GL_DEPTH_TEST);

            // 🔆 셰이더 설정
            Shader shader = ShaderManager.getInstance().getDefaultShader();
            shader.use();
            configureShader(shader);

            // 🏞️ 장면 렌더링
            renderScene();

            // 📢 FPS 디버깅
            System.out.printf("⏳ DeltaTime: %.6f | FPS: %.2f\n", deltaTime, 1.0f / deltaTime);

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
        Matrix4f projection = new Matrix4f().perspective(
                (float) Math.toRadians(camera.getZoom()),
                (float) w.get(0) / (float) h.get(0),
                0.01f, 1000.0f
        );

        shader.setMat4("projection", projection);
        shader.setMat4("view", camera.getViewMatrix());
    }

    private void renderScene() {
        world.render("testing");
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
        if (!isOnGround(playerPos)) {
            velocity.y += GRAVITY * deltaTime;
        } else {
            velocity.y = 0; // 바닥에 있을 경우 중력 초기화
        }

        // ✅ 점프 처리
        if (jump && isOnGround(playerPos)) {
            velocity.y = jumpForce; // 직접 점프 적용
        }

        // ✅ 최종 위치 반영
        playerPos.y += velocity.y * deltaTime;
        player.setPos(playerPos);
        player.setVelocity(velocity);

        // ✅ 카메라 위치 업데이트 (플레이어 머리 위치로)
        camera.setPlayerPos(player.getPos(), deltaTime);

        // ✅ 디버깅 로그 출력
        System.out.printf("🎮 Input: W:%b S:%b A:%b D:%b JUMP:%b | 🚀 OnGround: %b\n",
                forward, backward, left, rightMove, jump, isOnGround(playerPos));
        System.out.printf("📍 Position: (%.3f, %.3f, %.3f) | ➡ MoveVector: (%.3f, %.3f, %.3f) | PlayerSpeed: %.2f\n",
                playerPos.x, playerPos.y, playerPos.z, moveVector.x, moveVector.y, moveVector.z, playerSpeed);
    }

    public boolean isOnGround(Vector3f position) {
        Vector3f feetPos = new Vector3f(position.x, position.y - 0.1f, position.z);
        return world.getBlockAt(feetPos) != null;
    }

    private void resetPlayer() {
        Vector3f resetPosition = new Vector3f(0, 5f, 0);
        player.setPos(resetPosition);
        player.setVelocity(new Vector3f(0, 0, 0));
    }

    private void cleanup() {
        System.out.println("🚀 Cleaning up resources...");
        ShaderManager.getInstance().cleanup();
        world.cleanup();
        glfwDestroyWindow(windowManager.getWindow());
        glfwTerminate();
        System.out.println("✅ Cleanup completed!");
    }
}
