package dev.sinoka.entity;

import dev.sinoka.utility.MatUtil;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Matrix4f;
import org.joml.Matrix4fc;
import org.joml.Quaternionf;
import org.joml.Vector3f;

import static dev.sinoka.utility.MatUtil.transformMatrixToVector;

public class BoxCollision {
    private Vector3f position; // 객체의 위치
    private Vector3f size;     // 충돌 박스의 크기
    private Quaternionf rotation; // 회전
    private boolean isSolid;   // 충돌 가능한지 여부
    private static final Logger logger = LogManager.getLogger(BoxCollision.class);

    public BoxCollision(Vector3f position, Vector3f size) {
        this.position = position;
        this.size = size;
        this.rotation = new Quaternionf(0, 0, 0, 1); // 기본 회전값 (회전 없음)
        this.isSolid = true; // 기본값
    }

    // AABB 충돌 검사
    public boolean legacyIntersects(BoxCollision other) {
        if (!this.isSolid || !other.isSolid) {
            return false; // 둘 중 하나라도 비단단한 경우 충돌하지 않음
        }

        // AABB 충돌 검사 (축 정렬된 방식)
        boolean overlapX = this.position.x + this.size.x / 2 > other.position.x - other.size.x / 2 &&
                this.position.x - this.size.x / 2 < other.position.x + other.size.x / 2;

        boolean overlapY = this.position.y + this.size.y / 2 > other.position.y - other.size.y / 2 &&
                this.position.y - this.size.y / 2 < other.position.y + other.size.y / 2;

        boolean overlapZ = this.position.z + this.size.z / 2 > other.position.z - other.size.z / 2 &&
                this.position.z - this.size.z / 2 < other.position.z + other.size.z / 2;

        // X, Y, Z 축 모두 겹치면 충돌
        return overlapX && overlapY && overlapZ;
    }

    // 회전된 박스에 대한 충돌 검사
    public boolean intersects(BoxCollision other) {
        // 각 박스의 회전된 축을 계산
        Vector3f[] axesA = getAxes(); // 현재 박스의 축 벡터
        Vector3f[] axesB = other.getAxes(); // 다른 박스의 축 벡터

        // Y축에 대해 겹침이 발생한 경우 먼저 처리
        if (!overlapOnAxis(other, axesA[1])) {
            return false; // Y축에서 겹침이 없다면 충돌하지 않음
        }

        // X축, Z축에 대해 겹침을 검사
        for (Vector3f axis : axesA) {
            if (!overlapOnAxis(other, axis)) {
                return false; // 겹치지 않으면 충돌하지 않음
            }
        }

        for (Vector3f axis : axesB) {
            if (!overlapOnAxis(other, axis)) {
                return false; // 겹치지 않으면 충돌하지 않음
            }
        }

        // 박스들이 서로 겹치면 충돌하는 것
        return true;
    }

    // 주어진 축에 대해 두 박스가 겹치는지 확인
    private boolean overlapOnAxis(BoxCollision other, Vector3f axis) {
        // 각 박스의 최솟값과 최댓값을 구하고 겹치는지 확인
        float[] projectionA = projectOnAxis(axis); // 현재 박스를 축으로 투영
        float[] projectionB = other.projectOnAxis(axis); // 다른 박스를 축으로 투영

        // 겹치는지 여부를 확인 (두 투영 범위가 겹치면 겹침)
        return !(projectionA[1] < projectionB[0] || projectionB[1] < projectionA[0]);
    }

    // 박스를 주어진 축에 투영한 결과를 반환
    private float[] projectOnAxis(Vector3f axis) {
        // 3개의 꼭짓점을 축으로 투영하여 최솟값과 최댓값 구하기
        Vector3f[] vertices = getVertices(); // 박스의 8개의 꼭짓점 계산
        float min = axis.dot(vertices[0]);
        float max = min;

        for (Vector3f vertex : vertices) {
            float projection = axis.dot(vertex);
            if (projection < min) {
                min = projection;
            }
            if (projection > max) {
                max = projection;
            }
        }

        return new float[]{min, max};
    }

    // 박스의 8개 꼭짓점 계산
    private Vector3f[] getVertices() {
        Vector3f[] vertices = new Vector3f[8];

        // 각 꼭짓점 계산 (박스 크기와 위치, 회전을 고려)
        Vector3f[] halfExtents = new Vector3f[]{
                new Vector3f(size.x / 2, size.y / 2, size.z / 2),
                new Vector3f(-size.x / 2, size.y / 2, size.z / 2),
                new Vector3f(size.x / 2, -size.y / 2, size.z / 2),
                new Vector3f(size.x / 2, size.y / 2, -size.z / 2),
                new Vector3f(-size.x / 2, -size.y / 2, size.z / 2),
                new Vector3f(-size.x / 2, size.y / 2, -size.z / 2),
                new Vector3f(size.x / 2, -size.y / 2, -size.z / 2),
                new Vector3f(-size.x / 2, -size.y / 2, -size.z / 2)
        };

        Matrix4f rotationMatrix = new Matrix4f().rotation(rotation);
        for (int i = 0; i < 8; i++) {
            // 8개의 정점에 대해 rotationMatrix를 적용하여 위치를 변환
            vertices[i] = transformMatrixToVector(rotationMatrix, new Vector3f(halfExtents[i])).add(position);
        }

        return vertices;
    }

    // 회전값 적용된 BoxCollision의 축 벡터들 반환
    private Vector3f[] getAxes() {
        Matrix4f rotationMatrix = new Matrix4f().rotation(rotation);

        // X, Y, Z 축에 대한 회전된 축 벡터 계산
        Vector3f[] axes = new Vector3f[3];
        axes[0] = transformMatrixToVector(rotationMatrix, new Vector3f(1, 0, 0));
        axes[1] = transformMatrixToVector(rotationMatrix, new Vector3f(0, 1, 0));
        axes[2] = transformMatrixToVector(rotationMatrix, new Vector3f(0, 0, 1));
        return axes;
    }

    // 회전된 박스에 점이 내부에 있는지 확인하는 함수
    public boolean isPointInside(Vector3f point) {
        // 점을 로컬 좌표계로 변환하기 위한 변환 행렬 생성
        Matrix4f rotationMatrix = new Matrix4f().rotation(rotation);

        // 점을 박스의 중심으로 이동시킨 후
        Vector3f localPoint = new Vector3f(point).sub(position);

        // 로컬 좌표계로 변환 (역행렬을 적용)
        localPoint = transformMatrixToVector(rotationMatrix.invert(new Matrix4f()), localPoint);

        // 로컬 좌표계에서 점이 박스의 크기 범위 내에 있는지 검사
        return (localPoint.x >= -size.x / 2 && localPoint.x <= size.x / 2 &&
                localPoint.y >= -size.y / 2 && localPoint.y <= size.y / 2 &&
                localPoint.z >= -size.z / 2 && localPoint.z <= size.z / 2);
    }

    // yaw (수평 회전)을 이용하여 박스를 회전시키는 함수
    public void rotate(float yaw) {
        // yaw (수평 회전)을 적용한 쿼터니언 생성
        this.rotation = new Quaternionf().rotationY((float)Math.toRadians(yaw));
    }



    // Getter 및 Setter
    public Vector3f getPosition() {
        return position;
    }

    public Vector3f getSize() {
        return size;
    }

    public Quaternionf getRotation() {
        return rotation;
    }

    public boolean isSolid() {
        return isSolid;
    }

    public void setPosition(Vector3f position) {
        this.position = position;
    }

    public void setSize(Vector3f size) {
        this.size = size;
    }

    public void setRotation(Quaternionf rotation) {
        this.rotation = rotation;
    }

    public void setSolid(boolean solid) {
        isSolid = solid;
    }
}
