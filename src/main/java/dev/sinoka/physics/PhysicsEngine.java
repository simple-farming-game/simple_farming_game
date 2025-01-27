package dev.sinoka.physics;

import dev.sinoka.entity.Player;
import dev.sinoka.utility.Camera;
import dev.sinoka.world.World;
import org.joml.Vector3f;

import static org.lwjgl.glfw.GLFW.*;

public class PhysicsEngine {
    private static final float GRAVITY = -9.8f;
    private final World world;

    public PhysicsEngine(World world) {
        this.world = world;
    }

    /**
     * 🎮 키 입력을 받아 다음 위치를 계산하는 함수
     */
    public Vector3f computeNextPosition(
            Player player, Camera camera, float deltaTime, float playerSpeed, float jumpForce,
            boolean forward, boolean backward, boolean left, boolean rightMove, boolean jump) {

        Vector3f position = new Vector3f(player.getPos()); // 현재 위치 복사
        Vector3f velocity = new Vector3f(player.getVelocity()); // 현재 속도 복사

        // ✅ 카메라 방향 기반 이동 (XZ 평면에서 이동)
        Vector3f front = new Vector3f(camera.getFront().x, 0, camera.getFront().z).normalize();
        Vector3f right = new Vector3f(camera.getRight().x, 0, camera.getRight().z).normalize();

        Vector3f moveVector = new Vector3f();

        // ✅ 이동 방향 계산
        if (forward && left) {
            moveVector.add(front).sub(right);
        } else if (forward && rightMove) {
            moveVector.add(front).add(right);
        } else if (backward && left) {
            moveVector.sub(front).sub(right);
        } else if (backward && rightMove) {
            moveVector.sub(front).add(right);
        } else if (forward) {
            moveVector.add(front);
        } else if (backward) {
            moveVector.sub(front);
        } else if (left) {
            moveVector.sub(right);
        } else if (rightMove) {
            moveVector.add(right);
        }

        // ✅ 이동 벡터 정규화 및 속도 적용
        if (moveVector.lengthSquared() != 0) {
            moveVector.normalize().mul(playerSpeed * deltaTime);
            position.add(moveVector); // 🎯 새로운 위치 계산
        }

        // ✅ 점프 처리 (중력 계산은 아래에서)
        if (jump && isOnGround(position)) {
            velocity.y = jumpForce;
        }

        // ✅ 중력 적용
        if (!isOnGround(position)) {
            velocity.y += GRAVITY * deltaTime;
        } else {
            velocity.y = 0;
        }

        // ✅ 새로운 위치 반영 (y축 적용)
        position.y += velocity.y * deltaTime;

        System.out.printf("📍 Vel: (%.3f, %.3f, %.3f)\n", velocity.x,velocity.y, velocity.z);

        return position;
    }

    /**
     * 🚀 플레이어가 땅에 있는지 확인하는 함수
     */
    public boolean isOnGround(Vector3f position) {
        Vector3f feetPos = new Vector3f(position.x, position.y - 0.1f, position.z);
        return world.getBlockAt(feetPos) != null;
    }
}
