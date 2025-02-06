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

    private int windowWidth;  // 화면 너비
    private int windowHeight; // 화면 높이

    private Matrix4f projectionMatrix = new Matrix4f(); // 투영 행렬 저장
    private Matrix4f viewMatrix = new Matrix4f();       // 뷰 행렬 저장

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
        return viewMatrix;
    }

    public void updateMatrices() {
        // 투영 행렬 업데이트
        float aspectRatio = (float) windowWidth / (float) windowHeight;
        projectionMatrix.identity().perspective((float) Math.toRadians(zoom), aspectRatio, 0.01f, 1000.0f);

        // 뷰 행렬 업데이트
        viewMatrix.identity().lookAt(position, new Vector3f(position).add(front), up);
    }

    public Vector3f screenToWorld(float screenX, float screenY, float depth) {
        // 스크린 좌표 → NDC 좌표 변환
        float ndcX = (2.0f * screenX / windowWidth) - 1.0f;
        float ndcY = 1.0f - (2.0f * screenY / windowHeight);
        Vector4f ndcPos = new Vector4f(ndcX, ndcY, depth, 1.0f);

        // 역투영 행렬 계산 (Projection * View 역행렬)
        Matrix4f invPV = new Matrix4f();
        projectionMatrix.mul(viewMatrix, invPV).invert();

        // NDC → 월드 좌표 변환
        Vector4f worldPos = new Vector4f();
        ndcPos.mul(invPV, worldPos);
        worldPos.div(worldPos.w); // 정규화

        return new Vector3f(worldPos.x, worldPos.y, worldPos.z);
    }


    public Matrix4f getProjectionMatrix() {
        return projectionMatrix;
    }

    public void setWindowSize(int width, int height) {
        this.windowWidth = width;
        this.windowHeight = height;
    }

    public int getWindowWidth() {
        return windowWidth;
    }

    public int getWindowHeight() {
        return windowHeight;
    }

    private float time = 0.0f; // 누적 시간 (프레임마다 증가)
    private float frequency = 10.0f; // 흔들림 주기 (기본값)
    private float amplitude = 0.04f; // 흔들림 강도 (기본값)

    private Vector3f previousPlayerPos = new Vector3f(); // 이전 프레임 플레이어 위치
    private Vector3f velocity = new Vector3f(); // 속도

    public void setPlayerPos(Vector3f playerPos, float dt) {
        // Y 좌표가 바뀌었는지 확인
        boolean yChanged = previousPlayerPos.y != playerPos.y;

        // 카메라 위치 설정 및 머리 높이 조정
        position.set(playerPos);
        position.y += 1.8f;

        // 이동 거리 및 속도 계산
        float distance = previousPlayerPos.distance(playerPos);
        float speed = distance / dt;

        // 속도가 0일 때는 흔들림 효과를 적용하지 않음
        if (speed > 0.0f && !yChanged) {
            frequency = Math.max(5.0f, Math.min(15.0f, 10.0f + speed * 0.5f)); // 빠를수록 높은 주기
            time += dt; // 시간 누적 (Y 좌표가 바뀌지 않았을 때만)
        }

        // 흔들림 효과 적용 (Y 좌표가 바뀌지 않았을 때만, 속도가 0이 아닐 때)
        if (speed > 0.0f && !yChanged) {
            float yOffset = Math.sin(time * frequency) * amplitude;
            position.y += yOffset;
        }

        // 이전 플레이어 위치 업데이트
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

    public Vector3f getDirectionVector() {
        // yaw와 pitch 값으로 카메라가 보는 방향을 계산
        Vector3f direction = new Vector3f();

        // Pitch가 90도 또는 -90도일 경우, 앞/뒤 방향을 정확히 설정
        if (pitch == 90.0f) {
            direction.set(0, 1, 0); // 위쪽
        } else if (pitch == -90.0f) {
            direction.set(0, -1, 0); // 아래쪽
        } else {
            direction.x = (float) Math.cos(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
            direction.y = (float) Math.sin(Math.toRadians(pitch));
            direction.z = (float) Math.sin(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        }

        // 단위벡터로 정규화
        direction.normalize();

        return direction;
    }
}
