package dev.sinoka.utility;

import org.joml.*;
import org.joml.Math;

public class Camera {
    public enum Movement {
        FORWARD, BACKWARD, LEFT, RIGHT,
        LEFT_FORWARD, LEFT_BACKWARD, RIGHT_FORWARD, RIGHT_BACKWARD // 대각선 이동 추가
    }

    private Vector3f position;
    private Vector3f defaultPos;
    private Vector3f front;
    private Vector3f up;
    private Vector3f right;
    private Vector3f worldUp;

    private float yaw;
    private float pitch;

    private float movementSpeed;
    private float mouseSensitivity;
    private float zoom;

    public Camera(Vector3f position) {
        this.position = position;
        this.defaultPos = new Vector3f(position); // 기본 위치 복사
        this.front = new Vector3f(0.0f, 0.0f, -1.0f);
        this.worldUp = new Vector3f(0.0f, 1.0f, 0.0f);
        this.yaw = -90.0f;
        this.pitch = 0.0f;
        this.movementSpeed = 2.5f;
        this.mouseSensitivity = 0.1f;
        this.zoom = 45.0f;
        updateCameraVectors();
    }

    public Matrix4f getViewMatrix() {
        return new Matrix4f().lookAt(position, new Vector3f(position).add(front), up);
    }

    private float time = 0.0f; // 누적 시간 (프레임마다 증가)
    private float frequency = 50.0f; // 흔들림 주기
    private float amplitude = 0.007f; // 흔들림 강도

    public void processKeyboard(Movement direction, float deltaTime) {
        float velocity = movementSpeed * deltaTime;
        Vector3f moveVector = new Vector3f();

        // 방향별 벡터 추가 (대각선 포함)
        switch (direction) {
            case FORWARD:
                moveVector.add(new Vector3f(front.x, 0, front.z));
                break;
            case BACKWARD:
                moveVector.sub(new Vector3f(front.x, 0, front.z));
                break;
            case LEFT:
                moveVector.sub(new Vector3f(right.x, 0, right.z));
                break;
            case RIGHT:
                moveVector.add(new Vector3f(right.x, 0, right.z));
                break;
            case LEFT_FORWARD:
                moveVector.add(new Vector3f(front.x, 0, front.z));
                moveVector.sub(new Vector3f(right.x, 0, right.z));
                break;
            case LEFT_BACKWARD:
                moveVector.sub(new Vector3f(front.x, 0, front.z));
                moveVector.sub(new Vector3f(right.x, 0, right.z));
                break;
            case RIGHT_FORWARD:
                moveVector.add(new Vector3f(front.x, 0, front.z));
                moveVector.add(new Vector3f(right.x, 0, right.z));
                break;
            case RIGHT_BACKWARD:
                moveVector.sub(new Vector3f(front.x, 0, front.z));
                moveVector.add(new Vector3f(right.x, 0, right.z));
                break;
        }

        // 대각선 이동 시 속도 일정하게 유지 (정규화)
        if (moveVector.lengthSquared() != 0) {
            moveVector.normalize().mul(velocity);
            position.add(moveVector);
        }

        // 시간 증가
        time += deltaTime;

        // 흔들림 효과 추가 (사인 함수 적용)
        float yOffset = (float) Math.sin(time * frequency) * amplitude;

        // 사용자 위치를 ground level(xz 평면)에 고정하면서 흔들림 적용
        position.y = defaultPos.y + yOffset;
    }

    private Vector3f previousPlayerPos = new Vector3f(); // 이전 프레임 플레이어 위치

    public void setPlayerPos(Vector3f playerPos, float dt) {
        position.set(playerPos);
        position.y += 1.8f; // 머리 높이로 조정

        if (!previousPlayerPos.equals(playerPos)) {
            time += dt;
        }

        float yOffset = (float) Math.sin(time * frequency) * amplitude;
        position.y += yOffset;

        previousPlayerPos.set(playerPos);
    }



    public void processMouseMovement(float xoffset, float yoffset, boolean constrainPitch) {
        xoffset *= mouseSensitivity;
        yoffset *= mouseSensitivity;

        yaw += xoffset;
        pitch += yoffset;

        if (constrainPitch) {
            if (pitch > 89.0f) {
                pitch = 89.0f;
            }
            if (pitch < -89.0f) {
                pitch = -89.0f;
            }
        }

        updateCameraVectors();
    }

    public void processMouseScroll(float yoffset) {
        zoom -= yoffset;
        if (zoom < 1.0f) {
            zoom = 1.0f;
        }
        if (zoom > 45.0f) {
            zoom = 45.0f;
        }
    }

    public float getZoom() {
        return zoom;
    }

    public Vector3f getPosition() {
        return position;
    }

    private void updateCameraVectors() {
        Vector3f newFront = new Vector3f();
        newFront.x = (float) Math.cos(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        newFront.y = (float) Math.sin(Math.toRadians(pitch));
        newFront.z = (float) Math.sin(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        front.set(newFront).normalize();

        right = new Vector3f(front).cross(worldUp).normalize();
        up = new Vector3f(right).cross(front).normalize();
    }

    public Vector3f getFront() {
        return new Vector3f(front); // 원본 front 벡터의 복사본 반환
    }

    public Vector3f getRight() {
        return new Vector3f(right); // 원본 right 벡터의 복사본 반환
    }

    public Vector3f getUp() {
        return new Vector3f(up); // 원본 up 벡터의 복사본 반환
    }

    public void setPosition(Vector3f position) {
        this.position = position;
    }
}
